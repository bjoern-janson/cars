#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np

SYSTEMS = ("F", "N", "A")


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


def step(system, x, theta, e, t, cfg):
    control = np.asarray(cfg["dynamics"]["control_matrix"], dtype=float)
    x_next = np.tanh(transition_matrix(theta, cfg) @ x + control @ e)

    if system == "F":
        theta_next = theta.copy()
    else:
        rho = float(cfg["adaptation"]["rho"])
        eta = float(cfg["adaptation"]["eta"])
        if system == "A":
            driver = e
        elif system == "N":
            schedule = cfg["adaptation"]["exogenous_driver_schedule"]
            driver = vec(schedule[t % len(schedule)])
        else:
            raise ValueError(system)
        theta_next = rho * theta + eta * driver

    return x_next, theta_next


def rollout(system, x0, theta0, seq, interventions, cfg):
    x = x0.copy()
    theta = theta0.copy()
    ys = []

    for t, name in enumerate(seq):
        e = interventions[name]
        x, theta = step(system, x, theta, e, t, cfg)
        ys.append(x.copy())

    return np.concatenate(ys)


def sample_initial(rng, n, cfg):
    x_scale = float(cfg["sampling"]["x0_scale"])
    theta_scale = float(cfg["sampling"]["theta0_scale"])
    x0 = rng.uniform(-x_scale, x_scale, size=(n, 2))
    theta0 = rng.uniform(-theta_scale, theta_scale, size=(n, 2))
    return x0, theta0


def build_dataset(system, sequences, n_per_sequence, rng, cfg):
    interventions = {k: vec(v) for k, v in cfg["interventions"].items()}
    rows = []

    for seq_text in sequences:
        seq = list(seq_text)
        x0, theta0 = sample_initial(rng, n_per_sequence, cfg)
        for i in range(n_per_sequence):
            y = rollout(system, x0[i], theta0[i], seq, interventions, cfg)
            eflat = np.concatenate([interventions[s] for s in seq])
            rows.append((x0[i], theta0[i], eflat, y, seq_text))

    return {
        "x0": np.stack([r[0] for r in rows]),
        "theta0": np.stack([r[1] for r in rows]),
        "eflat": np.stack([r[2] for r in rows]),
        "y": np.stack([r[3] for r in rows]),
        "labels": np.asarray([r[4] for r in rows]),
    }


def representation(data, name):
    x = data["x0"]
    theta = data["theta0"]

    if name == "x_only":
        return x
    if name == "x_theta_mean":
        return np.column_stack([x, theta.mean(axis=1)])
    if name == "full_state":
        return np.column_stack([x, theta])

    raise ValueError(name)


def features(z, eflat):
    n = len(z)
    ones = np.ones((n, 1))
    cross_ze = (z[:, :, None] * eflat[:, None, :]).reshape(n, -1)

    # Horizon is frozen at 2 in Pilot 1. Each intervention descriptor is 2-D.
    d_e = eflat.shape[1] // 2
    e1 = eflat[:, :d_e]
    e2 = eflat[:, d_e:]
    cross_e = (e1[:, :, None] * e2[:, None, :]).reshape(n, -1)

    return np.column_stack([ones, z, eflat, cross_ze, cross_e])


def fit_ridge(phi, y, alpha):
    p = phi.shape[1]
    reg = np.eye(p) * alpha
    reg[0, 0] = 0.0
    return np.linalg.solve(phi.T @ phi + reg, phi.T @ y)


def mse(y, pred):
    return float(np.mean((y - pred) ** 2))


def evaluate_system(system, cfg, seed):
    # Distinct deterministic random streams prevent accidental state reuse while
    # keeping the generation contract fixed across reruns.
    train_offset = {"F": 11, "N": 22, "A": 33}[system]
    test_offset = {"F": 111, "N": 222, "A": 333}[system]
    rng_train = np.random.default_rng(seed + train_offset)
    rng_test = np.random.default_rng(seed + test_offset)

    train = build_dataset(
        system,
        cfg["sequences"]["train"],
        cfg["sampling"]["train_per_sequence"],
        rng_train,
        cfg,
    )
    test_iid = build_dataset(
        system,
        cfg["sequences"]["train"],
        cfg["sampling"]["test_per_sequence"],
        rng_test,
        cfg,
    )
    test_struct = build_dataset(
        system,
        cfg["sequences"]["structural_holdout"],
        cfg["sampling"]["test_per_sequence"],
        rng_test,
        cfg,
    )

    results = []
    alpha = float(cfg["predictor"]["ridge_alpha"])
    train_grid = cfg["predictor"]["train_sample_grid"]
    reps = cfg["predictor"]["representations"]

    sub_rng = np.random.default_rng(seed + 909)
    train_indices = np.arange(len(train["y"]))
    sub_rng.shuffle(train_indices)

    for rep in reps:
        z_train_all = representation(train, rep)
        z_iid = representation(test_iid, rep)
        z_struct = representation(test_struct, rep)
        phi_iid = features(z_iid, test_iid["eflat"])
        phi_struct = features(z_struct, test_struct["eflat"])

        y_var_iid = float(np.var(test_iid["y"]))
        y_var_struct = float(np.var(test_struct["y"]))

        for n_train in train_grid:
            idx = train_indices[: min(int(n_train), len(train_indices))]
            phi_train = features(z_train_all[idx], train["eflat"][idx])
            beta = fit_ridge(phi_train, train["y"][idx], alpha)

            pred_iid = phi_iid @ beta
            pred_struct = phi_struct @ beta
            m_iid = mse(test_iid["y"], pred_iid)
            m_struct = mse(test_struct["y"], pred_struct)

            results.append(
                {
                    "system": system,
                    "representation": rep,
                    "representation_dim": int(z_train_all.shape[1]),
                    "train_samples": int(len(idx)),
                    "feature_dim": int(phi_train.shape[1]),
                    "output_dim": int(train["y"].shape[1]),
                    "inference_multadds": int(phi_train.shape[1] * train["y"].shape[1]),
                    "iid_mse": m_iid,
                    "iid_nmse": m_iid / y_var_iid if y_var_iid > 0 else None,
                    "structural_mse": m_struct,
                    "structural_nmse": m_struct / y_var_struct if y_var_struct > 0 else None,
                }
            )

    return results


def paired_contrasts(rows):
    by_key = {}
    for row in rows:
        key = (row["representation"], row["train_samples"])
        by_key.setdefault(key, {})[row["system"]] = row

    out = []
    for key, systems in sorted(by_key.items()):
        if all(system in systems for system in SYSTEMS):
            out.append(
                {
                    "representation": key[0],
                    "train_samples": key[1],
                    "A_minus_N_structural_nmse": systems["A"]["structural_nmse"]
                    - systems["N"]["structural_nmse"],
                    "A_minus_F_structural_nmse": systems["A"]["structural_nmse"]
                    - systems["F"]["structural_nmse"],
                    "N_minus_F_structural_nmse": systems["N"]["structural_nmse"]
                    - systems["F"]["structural_nmse"],
                }
            )

    return out


def primary_decision(cfg, contrasts):
    max_n = max(int(x) for x in cfg["predictor"]["train_sample_grid"])
    matches = [
        row
        for row in contrasts
        if row["representation"] == "full_state" and row["train_samples"] == max_n
    ]
    if len(matches) != 1:
        raise RuntimeError("primary full_state / max-N contrast is not uniquely defined")

    delta = matches[0]["A_minus_N_structural_nmse"]
    label = "A_NOT_HARDER_THAN_N" if delta <= 0 else "DESCRIPTIVE_A_EXCESS"
    return {
        "representation": "full_state",
        "train_samples": max_n,
        "A_minus_N_structural_nmse": delta,
        "label": label,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.smoke:
        cfg = json.loads(json.dumps(cfg))
        cfg["sampling"]["train_per_sequence"] = 16
        cfg["sampling"]["test_per_sequence"] = 8
        cfg["predictor"]["train_sample_grid"] = [32]

    seed = int(cfg["seed"])
    rows = []
    for system in SYSTEMS:
        rows.extend(evaluate_system(system, cfg, seed))

    contrasts = paired_contrasts(rows)
    decision = None if args.smoke else primary_decision(cfg, contrasts)

    result = {
        "schema_version": 1,
        "study": cfg["study"],
        "status": "SMOKE_ONLY" if args.smoke else "PILOT1_SYNTHETIC_OUTCOME",
        "authority": cfg["authority"],
        "rows": rows,
        "contrasts": contrasts,
        "primary_decision": decision,
        "guardrails": [
            "These curves are empirical upper bounds from one fixed predictor family, not intrinsic Pareto optima.",
            "A-N is descriptive under this toy construction; it is not a general causal effect of adaptation.",
            "Estimator scaling is not intrinsic scaling.",
            "A predictive-resource difference does not imply adaptive quality or a new construct.",
        ],
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "rows": len(rows),
                "primary_decision": decision,
                "out": args.json_out,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
