#!/usr/bin/env python3
import argparse
import itertools
import json
from pathlib import Path

import numpy as np

SYSTEMS = ("N", "A")


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def vec(x):
    return np.asarray(x, dtype=float)


def transition_matrix(theta, cfg):
    base = np.asarray(cfg["dynamics"]["base_matrix"], dtype=float)
    m1 = np.asarray(cfg["dynamics"]["theta_matrix_1"], dtype=float)
    m2 = np.asarray(cfg["dynamics"]["theta_matrix_2"], dtype=float)
    return base + theta[0] * m1 + theta[1] * m2


def true_step(system, x, theta, e, t, cfg):
    control = np.asarray(cfg["dynamics"]["control_matrix"], dtype=float)
    x_next = np.tanh(transition_matrix(theta, cfg) @ x + control @ e)

    rho = float(cfg["adaptation"]["rho"])
    eta = float(cfg["adaptation"]["eta"])
    if system == "N":
        schedule = cfg["adaptation"]["exogenous_driver_schedule"]
        driver = vec(schedule[t % len(schedule)])
    elif system == "A":
        driver = e
    else:
        raise ValueError(system)

    theta_next = rho * theta + eta * driver
    return x_next, theta_next


def sample_pair_bank(sequences, n_per_sequence, rng, cfg):
    x_scale = float(cfg["sampling"]["x0_scale"])
    theta_scale = float(cfg["sampling"]["theta0_scale"])
    out = {}
    for seq in sequences:
        out[seq] = {
            "x0": rng.uniform(-x_scale, x_scale, size=(n_per_sequence, 2)),
            "theta0": rng.uniform(-theta_scale, theta_scale, size=(n_per_sequence, 2)),
        }
    return out


def raw_input(state, e, t):
    state = np.asarray(state, dtype=float)
    e = np.asarray(e, dtype=float)
    if state.ndim == 1:
        time = np.zeros(2, dtype=float)
        time[int(t)] = 1.0
        return np.concatenate([state, e, time])

    n = len(state)
    e_rows = np.broadcast_to(e, (n, 2))
    time = np.zeros((n, 2), dtype=float)
    time[:, int(t)] = 1.0
    return np.column_stack([state, e_rows, time])


def monomial_powers(n_variables, degree):
    powers = [()]
    for d in range(1, degree + 1):
        powers.extend(itertools.combinations_with_replacement(range(n_variables), d))
    return powers


def polynomial_features(raw, powers):
    raw = np.asarray(raw, dtype=float)
    if raw.ndim == 1:
        raw = raw[None, :]
    phi = np.empty((len(raw), len(powers)), dtype=float)
    for j, combo in enumerate(powers):
        if not combo:
            phi[:, j] = 1.0
            continue
        col = np.ones(len(raw), dtype=float)
        for index in combo:
            col *= raw[:, index]
        phi[:, j] = col
    return phi


def build_transition_bank(system, pair_bank, sequences, cfg):
    bank = {}
    for seq in sequences:
        x0 = pair_bank[seq]["x0"]
        theta0 = pair_bank[seq]["theta0"]
        n = len(x0)
        raws = np.empty((n, 2, 8), dtype=float)
        next_states = np.empty((n, 2, 4), dtype=float)

        for i in range(n):
            x = x0[i].copy()
            theta = theta0[i].copy()
            for t, intervention_name in enumerate(seq):
                e = vec(cfg["interventions"][intervention_name])
                state = np.concatenate([x, theta])
                raws[i, t] = raw_input(state, e, t)
                x, theta = true_step(system, x, theta, e, t, cfg)
                next_states[i, t] = np.concatenate([x, theta])

        bank[seq] = {"raw": raws, "next_state": next_states}
    return bank


def build_truth(system, pair_bank, sequences, cfg):
    rows = []
    for seq in sequences:
        x0 = pair_bank[seq]["x0"]
        theta0 = pair_bank[seq]["theta0"]
        for i in range(len(x0)):
            x = x0[i].copy()
            theta = theta0[i].copy()
            trajectory = []
            for t, intervention_name in enumerate(seq):
                e = vec(cfg["interventions"][intervention_name])
                x, theta = true_step(system, x, theta, e, t, cfg)
                trajectory.extend(x.tolist())
            rows.append(
                {
                    "x0": x0[i],
                    "theta0": theta0[i],
                    "sequence": seq,
                    "target": np.asarray(trajectory, dtype=float),
                }
            )
    return rows


def fit_ridge(phi, y, alpha):
    p = phi.shape[1]
    regularizer = np.eye(p, dtype=float) * alpha
    regularizer[0, 0] = 0.0
    return np.linalg.solve(phi.T @ phi + regularizer, phi.T @ y)


def fit_identifier(transition_bank, cached_phi, selection_orders, per_sequence_n, alpha):
    phi_parts = []
    y_parts = []
    for seq in transition_bank:
        idx = selection_orders[seq][:per_sequence_n]
        phi_parts.append(cached_phi[seq][idx].reshape(-1, cached_phi[seq].shape[-1]))
        y_parts.append(transition_bank[seq]["next_state"][idx].reshape(-1, 4))
    phi = np.concatenate(phi_parts, axis=0)
    y = np.concatenate(y_parts, axis=0)
    beta = fit_ridge(phi, y, alpha)
    return beta, int(len(y)), int(phi.shape[1])


def predict_truth_rows(beta, truth_rows, powers, cfg):
    predictions = np.empty((len(truth_rows), 4), dtype=float)
    by_sequence = {}
    for i, row in enumerate(truth_rows):
        by_sequence.setdefault(row["sequence"], []).append(i)

    for seq, indices in by_sequence.items():
        states = np.column_stack(
            [
                np.stack([truth_rows[i]["x0"] for i in indices]),
                np.stack([truth_rows[i]["theta0"] for i in indices]),
            ]
        )
        trajectory = np.empty((len(indices), 4), dtype=float)

        for t, intervention_name in enumerate(seq):
            e = vec(cfg["interventions"][intervention_name])
            raw = raw_input(states, e, t)
            phi = polynomial_features(raw, powers)
            states = phi @ beta
            trajectory[:, 2 * t : 2 * t + 2] = states[:, :2]

        predictions[np.asarray(indices, dtype=int)] = trajectory

    return predictions


def distortion(truth_rows, predictions):
    target = np.stack([row["target"] for row in truth_rows])
    if not np.all(np.isfinite(predictions)):
        return {"mse": None, "nmse": None, "status": "NONFINITE_PREDICTION"}
    mse = float(np.mean((target - predictions) ** 2))
    variance = float(np.var(target))
    nmse = mse / variance if variance > 0 else None
    return {"mse": mse, "nmse": nmse, "status": "OK"}


def curve_summary(rows, degree, system, cfg):
    selected = sorted(
        [r for r in rows if r["degree"] == degree and r["system"] == system],
        key=lambda r: r["train_trajectories"],
    )
    finite = [r for r in selected if r["structural_nmse"] is not None and r["structural_nmse"] > 0]
    if len(finite) != len(selected):
        return {
            "system": system,
            "degree": degree,
            "log_curve_score": None,
            "high_n_loglog_slope": None,
            "tolerance_crossings": {},
            "status": "INCOMPLETE_NONFINITE_CURVE",
        }

    x = np.log10([r["train_trajectories"] for r in finite])
    y = np.log10([r["structural_nmse"] for r in finite])
    log_curve_score = float(np.trapz(y, x) / (x[-1] - x[0]))

    slope_min = int(cfg["readouts"]["slope_min_total_train_trajectories"])
    high = [r for r in finite if r["train_trajectories"] >= slope_min]
    if len(high) >= 2:
        hx = np.log10([r["train_trajectories"] for r in high])
        hy = np.log10([r["structural_nmse"] for r in high])
        slope = float(np.polyfit(hx, hy, deg=1)[0])
    else:
        slope = None

    crossings = {}
    for epsilon in cfg["readouts"]["tolerances"]:
        hit = next((r["train_trajectories"] for r in finite if r["structural_nmse"] <= epsilon), None)
        crossings[str(epsilon)] = hit if hit is not None else ">6000"

    return {
        "system": system,
        "degree": degree,
        "log_curve_score": log_curve_score,
        "high_n_loglog_slope": slope,
        "tolerance_crossings": crossings,
        "status": "OK",
    }


def run(cfg, smoke=False):
    seed = int(cfg["development_seed"] if smoke else cfg["confirmatory_seed"])
    local_cfg = json.loads(json.dumps(cfg))

    if smoke:
        local_cfg["sampling"]["train_per_sequence_pool"] = 24
        local_cfg["sampling"]["iid_test_per_sequence"] = 12
        local_cfg["sampling"]["structural_test_per_sequence"] = 12
        local_cfg["sampling"]["train_per_sequence_grid"] = [8, 16]

    rng_train = np.random.default_rng(seed + 1)
    rng_iid = np.random.default_rng(seed + 2)
    rng_struct = np.random.default_rng(seed + 3)

    train_sequences = local_cfg["sequences"]["train"]
    structural_sequences = local_cfg["sequences"]["structural_holdout"]

    train_pairs = sample_pair_bank(
        train_sequences,
        int(local_cfg["sampling"]["train_per_sequence_pool"]),
        rng_train,
        local_cfg,
    )
    iid_pairs = sample_pair_bank(
        train_sequences,
        int(local_cfg["sampling"]["iid_test_per_sequence"]),
        rng_iid,
        local_cfg,
    )
    structural_pairs = sample_pair_bank(
        structural_sequences,
        int(local_cfg["sampling"]["structural_test_per_sequence"]),
        rng_struct,
        local_cfg,
    )

    selection_rng = np.random.default_rng(seed + 100)
    selection_orders = {
        seq: selection_rng.permutation(len(train_pairs[seq]["x0"])) for seq in train_sequences
    }

    alpha = float(local_cfg["identifier"]["ridge_alpha"])
    degrees = [int(x) for x in local_cfg["identifier"]["degrees"]]
    per_sequence_grid = [int(x) for x in local_cfg["sampling"]["train_per_sequence_grid"]]

    rows = []

    for system in SYSTEMS:
        transition_bank = build_transition_bank(system, train_pairs, train_sequences, local_cfg)
        iid_truth = build_truth(system, iid_pairs, train_sequences, local_cfg)
        structural_truth = build_truth(system, structural_pairs, structural_sequences, local_cfg)

        for degree in degrees:
            powers = monomial_powers(8, degree)
            cached_phi = {
                seq: polynomial_features(
                    transition_bank[seq]["raw"].reshape(-1, 8), powers
                ).reshape(
                    transition_bank[seq]["raw"].shape[0],
                    2,
                    len(powers),
                )
                for seq in train_sequences
            }

            for per_sequence_n in per_sequence_grid:
                beta, transition_count, feature_dim = fit_identifier(
                    transition_bank,
                    cached_phi,
                    selection_orders,
                    per_sequence_n,
                    alpha,
                )

                pred_iid = predict_truth_rows(beta, iid_truth, powers, local_cfg)
                pred_struct = predict_truth_rows(beta, structural_truth, powers, local_cfg)
                iid_d = distortion(iid_truth, pred_iid)
                struct_d = distortion(structural_truth, pred_struct)

                total_trajectories = int(per_sequence_n * len(train_sequences))
                rows.append(
                    {
                        "system": system,
                        "degree": degree,
                        "train_trajectories": total_trajectories,
                        "train_transitions": transition_count,
                        "feature_dim": feature_dim,
                        "model_coefficients": int(feature_dim * 4),
                        "inference_multadds_per_step": int(feature_dim * 4),
                        "iid_mse": iid_d["mse"],
                        "iid_nmse": iid_d["nmse"],
                        "iid_status": iid_d["status"],
                        "structural_mse": struct_d["mse"],
                        "structural_nmse": struct_d["nmse"],
                        "structural_status": struct_d["status"],
                    }
                )

    summaries = []
    for degree in degrees:
        for system in SYSTEMS:
            summaries.append(curve_summary(rows, degree, system, local_cfg))

    contrasts = []
    for degree in degrees:
        for per_sequence_n in per_sequence_grid:
            total = int(per_sequence_n * len(train_sequences))
            matched = {
                r["system"]: r
                for r in rows
                if r["degree"] == degree and r["train_trajectories"] == total
            }
            if all(system in matched for system in SYSTEMS):
                a = matched["A"]["structural_nmse"]
                n = matched["N"]["structural_nmse"]
                contrasts.append(
                    {
                        "degree": degree,
                        "train_trajectories": total,
                        "A_minus_N_structural_nmse": None if a is None or n is None else float(a - n),
                    }
                )

    primary_degree = int(local_cfg["identifier"]["primary_degree"])
    max_total = int(max(per_sequence_grid) * len(train_sequences))
    primary_matches = [
        c
        for c in contrasts
        if c["degree"] == primary_degree and c["train_trajectories"] == max_total
    ]
    if smoke:
        primary_decision = None
    elif len(primary_matches) != 1 or primary_matches[0]["A_minus_N_structural_nmse"] is None:
        primary_decision = {
            "label": "PRIMARY_NOT_ADJUDICABLE",
            "A_minus_N_structural_nmse": None,
        }
    else:
        delta = float(primary_matches[0]["A_minus_N_structural_nmse"])
        primary_decision = {
            "degree": primary_degree,
            "train_trajectories": max_total,
            "A_minus_N_structural_nmse": delta,
            "label": "NO_HIGH_RESOURCE_A_EXCESS" if delta <= 0 else "DESCRIPTIVE_HIGH_RESOURCE_A_EXCESS",
        }

    primary_summaries = {
        s["system"]: s for s in summaries if s["degree"] == primary_degree
    }
    curve_contrast = None
    slope_contrast = None
    if all(system in primary_summaries for system in SYSTEMS):
        a_summary = primary_summaries["A"]
        n_summary = primary_summaries["N"]
        if a_summary["log_curve_score"] is not None and n_summary["log_curve_score"] is not None:
            curve_contrast = float(a_summary["log_curve_score"] - n_summary["log_curve_score"])
        if a_summary["high_n_loglog_slope"] is not None and n_summary["high_n_loglog_slope"] is not None:
            slope_contrast = float(
                a_summary["high_n_loglog_slope"] - n_summary["high_n_loglog_slope"]
            )

    return {
        "schema_version": 1,
        "study": local_cfg["study"],
        "status": "SMOKE_ONLY" if smoke else "PILOT1_ID1_SYNTHETIC_OUTCOME",
        "implementation_revision": "V2 vectorized evaluation only; no scientific settings changed",
        "seed": seed,
        "authority": local_cfg["authority"],
        "rows": rows,
        "curve_summaries": summaries,
        "contrasts": contrasts,
        "primary_decision": primary_decision,
        "primary_curve_A_minus_N_log_score": curve_contrast,
        "primary_slope_beta_A_minus_beta_N": slope_contrast,
        "known_dynamics_reference": {
            "source": "Pilot 1 Match1 exact-model oracle",
            "N_distortion": 0.0,
            "A_distortion": 0.0,
            "interpretation": "reference execution column only; ID1 measures finite-data identification plus prediction",
        },
        "guardrails": [
            "Observed ID1 curves are estimator-level upper bounds, not intrinsic sample-complexity minima.",
            "A-N under ID1 does not identify an adaptation-specific mechanism.",
            "A high-N difference that disappears under a stronger generic identifier is an estimator/model-class effect.",
            "A tolerance crossing is a coarse grid threshold, not minimax N*.",
            "A log-log slope on this finite grid is descriptive and is not an asymptotic scaling law.",
            "No ID1 outcome authorizes a new construct or theory.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    result = run(cfg, smoke=args.smoke)
    Path(args.json_out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "implementation_revision": result["implementation_revision"],
                "seed": result["seed"],
                "rows": len(result["rows"]),
                "primary_decision": result["primary_decision"],
                "primary_curve_A_minus_N_log_score": result["primary_curve_A_minus_N_log_score"],
                "primary_slope_beta_A_minus_beta_N": result["primary_slope_beta_A_minus_beta_N"],
                "out": args.json_out,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
