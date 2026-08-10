#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler


class MLP(nn.Module):
    def __init__(self, input_dim, hidden_sizes, num_classes):
        super().__init__()
        h1, h2 = hidden_sizes
        self.fc1 = nn.Linear(input_dim, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, num_classes)

    def forward(self, x, return_activations=False):
        h1 = F.relu(self.fc1(x))
        h2 = F.relu(self.fc2(h1))
        logits = self.out(h2)
        if return_activations:
            return logits, h1, h2
        return logits


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def stable_seed(base, *parts):
    payload = "::".join([str(base), *map(str, parts)]).encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big") % (2**32 - 1)


def state_dict_clone(model):
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}


def load_state(model, state):
    model.load_state_dict({k: v.clone() for k, v in state.items()})


def flatten_parameters(model):
    return torch.cat([p.detach().reshape(-1).cpu() for p in model.parameters()]).numpy().astype(np.float64)


def make_model(cfg, input_dim):
    return MLP(
        input_dim=input_dim,
        hidden_sizes=cfg["model"]["hidden_sizes"],
        num_classes=int(cfg["model"]["num_classes"]),
    )


def make_optimizer(model, cfg):
    return torch.optim.SGD(
        model.parameters(),
        lr=float(cfg["model"]["learning_rate"]),
        momentum=float(cfg["model"]["momentum"]),
        weight_decay=float(cfg["model"]["weight_decay"]),
    )


def load_real_mnist(cfg):
    from torchvision.datasets import MNIST

    root = cfg["dataset"]["root"]
    download = bool(cfg["dataset"].get("download", False))
    train = MNIST(root=root, train=True, download=download)
    test = MNIST(root=root, train=False, download=download)
    x_train = train.data.reshape(len(train), -1).float() / 255.0
    y_train = train.targets.long()
    x_test = test.data.reshape(len(test), -1).float() / 255.0
    y_test = test.targets.long()
    return x_train, y_train, x_test, y_test


def make_synthetic_smoke(seed, input_dim=784, n_train=2048, n_test=512, num_classes=10):
    rng = np.random.default_rng(seed)
    teacher = rng.normal(size=(input_dim, num_classes)).astype(np.float32)
    x_train = rng.normal(size=(n_train, input_dim)).astype(np.float32)
    x_test = rng.normal(size=(n_test, input_dim)).astype(np.float32)
    y_train = np.argmax(x_train @ teacher + 0.1 * rng.normal(size=(n_train, num_classes)), axis=1)
    y_test = np.argmax(x_test @ teacher + 0.1 * rng.normal(size=(n_test, num_classes)), axis=1)
    x_train = 1.0 / (1.0 + np.exp(-x_train))
    x_test = 1.0 / (1.0 + np.exp(-x_test))
    return (
        torch.from_numpy(x_train),
        torch.from_numpy(y_train.astype(np.int64)),
        torch.from_numpy(x_test),
        torch.from_numpy(y_test.astype(np.int64)),
    )


def choose_subsets(x_train, y_train, x_test, y_test, cfg, smoke):
    rng = np.random.default_rng(int(cfg["dataset"]["subset_seed"]))
    train_n = int(cfg["dataset"]["task_train_size"])
    test_n = int(cfg["dataset"]["task_test_size"])
    if smoke:
        train_n = min(512, len(x_train))
        test_n = min(256, len(x_test))
    train_idx = rng.choice(len(x_train), size=train_n, replace=False)
    test_idx = rng.choice(len(x_test), size=test_n, replace=False)
    return x_train[train_idx], y_train[train_idx], x_test[test_idx], y_test[test_idx]


def random_permutation(input_dim, seed):
    rng = np.random.default_rng(seed)
    return torch.from_numpy(rng.permutation(input_dim).astype(np.int64))


def batch_order(n, seed):
    rng = np.random.default_rng(seed)
    return torch.from_numpy(rng.permutation(n).astype(np.int64))


def evaluate(model, x, y, perm, batch_size):
    model.eval()
    total_loss = 0.0
    total_correct = 0
    with torch.no_grad():
        for start in range(0, len(x), batch_size):
            idx = slice(start, min(start + batch_size, len(x)))
            xb = x[idx][:, perm]
            yb = y[idx]
            logits = model(xb)
            total_loss += float(F.cross_entropy(logits, yb, reduction="sum"))
            total_correct += int((logits.argmax(dim=1) == yb).sum())
    return {
        "loss": total_loss / len(x),
        "accuracy": total_correct / len(x),
    }


def train_one_task(model, x, y, perm, order, cfg):
    model.train()
    opt = make_optimizer(model, cfg)
    bs = int(cfg["model"]["batch_size"])
    for start in range(0, len(order), bs):
        idx = order[start : min(start + bs, len(order))]
        xb = x[idx][:, perm]
        yb = y[idx]
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(xb), yb)
        loss.backward()
        opt.step()


def effective_rank_fraction(h):
    h = h.detach().float()
    h = h - h.mean(dim=0, keepdim=True)
    s = torch.linalg.svdvals(h)
    if len(s) == 0 or float((s * s).sum()) == 0.0:
        return 0.0
    erank = float((s.sum() ** 2 / (s.square().sum() + 1e-12)).item())
    return erank / float(min(h.shape[0], h.shape[1]))


def checkpoint_measurements(model, init_flat, x_test, y_test, perm, cfg):
    bs = int(cfg["model"]["batch_size"])
    current = evaluate(model, x_test, y_test, perm, bs)

    probe_n = min(int(cfg["dataset"]["probe_size"]), len(x_test))
    xb = x_test[:probe_n][:, perm]
    yb = y_test[:probe_n]

    model.eval()
    model.zero_grad(set_to_none=True)
    logits, h1, h2 = model(xb, return_activations=True)
    loss = F.cross_entropy(logits, yb)
    loss.backward()
    grad_sq = 0.0
    for p in model.parameters():
        if p.grad is not None:
            grad_sq += float(torch.sum(p.grad.detach() ** 2))

    dead_h1 = (h1.detach().abs().sum(dim=0) == 0).float().sum().item()
    dead_h2 = (h2.detach().abs().sum(dim=0) == 0).float().sum().item()
    dead_frac = (dead_h1 + dead_h2) / float(h1.shape[1] + h2.shape[1])

    flat = flatten_parameters(model)
    return {
        "current_task_accuracy": float(current["accuracy"]),
        "current_task_loss": float(current["loss"]),
        "parameter_l2": float(np.linalg.norm(flat)),
        "mean_abs_parameter": float(np.mean(np.abs(flat))),
        "distance_from_initialization_l2": float(np.linalg.norm(flat - init_flat)),
        "gradient_l2_on_probe": float(math.sqrt(grad_sq)),
        "dead_relu_fraction": float(dead_frac),
        "activation_effective_rank_fraction": float(effective_rank_fraction(h2)),
        "activation_std": float(h2.detach().std().item()),
        "parameter_flat": flat,
    }


def make_projection(param_dim, sketch_dim, seed):
    rng = np.random.default_rng(seed)
    signs = rng.integers(0, 2, size=(param_dim, sketch_dim), dtype=np.int8)
    signs = (2 * signs - 1).astype(np.float32)
    return signs / math.sqrt(sketch_dim)


def build_checkpoints(cfg, x_train, y_train, x_test, y_test, smoke=False):
    torch.set_num_threads(1)
    input_dim = int(x_train.shape[1])
    torch.manual_seed(int(cfg["model"]["initialization_seed"]))
    base_model = make_model(cfg, input_dim)
    base_state = state_dict_clone(base_model)
    init_flat = flatten_parameters(base_model)

    sketch_cfg = cfg["checkpoint_measurements"]["rich_parameter_sketch"]
    projection = make_projection(
        len(init_flat), int(sketch_cfg["dimensions"]), int(sketch_cfg["seed"])
    )

    runs = int(cfg["history"]["runs"])
    max_tasks = int(cfg["history"]["max_tasks"])
    ages = list(map(int, cfg["history"]["checkpoint_task_ages"]))
    if smoke:
        runs = 4
        max_tasks = 4
        ages = [1, 2, 4]

    checkpoints = []
    for run in range(runs):
        model = make_model(cfg, input_dim)
        load_state(model, base_state)
        current_perm = None
        for age in range(1, max_tasks + 1):
            pseed = stable_seed(cfg["history"]["task_permutation_seed"], run, age)
            current_perm = random_permutation(input_dim, pseed)
            oseed = stable_seed(cfg["history"]["example_order_seed"], run, age)
            order = batch_order(len(x_train), oseed)
            train_one_task(model, x_train, y_train, current_perm, order, cfg)

            if age in ages:
                m = checkpoint_measurements(model, init_flat, x_test, y_test, current_perm, cfg)
                delta = m.pop("parameter_flat") - init_flat
                sketch = delta @ projection
                checkpoints.append(
                    {
                        "history_run": run,
                        "task_age": age,
                        **m,
                        "parameter_sketch": sketch.astype(np.float64),
                        "state_dict": state_dict_clone(model),
                    }
                )
    return checkpoints, base_state, input_dim


def curve_milestone_batches(total_batches, fractions):
    out = []
    for f in fractions:
        b = int(round(float(f) * total_batches))
        b = min(max(b, 0), total_batches)
        out.append(b)
    if out[0] != 0:
        raise ValueError("learning curve must include fraction 0")
    return out


def future_learning_curve(state, base_state, use_fresh, input_dim, x_train, y_train, x_test, y_test, perm, order, cfg):
    model = make_model(cfg, input_dim)
    load_state(model, base_state if use_fresh else state)
    opt = make_optimizer(model, cfg)
    bs = int(cfg["model"]["batch_size"])
    fractions = [float(x) for x in cfg["future_task"]["learning_curve_fractions"]]
    total_batches = math.ceil(len(order) / bs)
    milestones = curve_milestone_batches(total_batches, fractions)

    curve = []
    initial = evaluate(model, x_test, y_test, perm, bs)
    curve.append({"fraction": 0.0, "accuracy": initial["accuracy"], "loss": initial["loss"]})

    milestone_to_fraction = {b: f for b, f in zip(milestones[1:], fractions[1:])}
    model.train()
    for batch_idx, start in enumerate(range(0, len(order), bs), start=1):
        idx = order[start : min(start + bs, len(order))]
        xb = x_train[idx][:, perm]
        yb = y_train[idx]
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(xb), yb)
        loss.backward()
        opt.step()
        if batch_idx in milestone_to_fraction:
            ev = evaluate(model, x_test, y_test, perm, bs)
            curve.append(
                {
                    "fraction": float(milestone_to_fraction[batch_idx]),
                    "accuracy": ev["accuracy"],
                    "loss": ev["loss"],
                }
            )
    if len(curve) != len(fractions):
        raise RuntimeError(f"curve length mismatch: {len(curve)} vs {len(fractions)}")
    return curve


def auc_accuracy(curve):
    x = np.asarray([r["fraction"] for r in curve], dtype=float)
    y = np.asarray([r["accuracy"] for r in curve], dtype=float)
    return float(np.trapezoid(y, x))


def t90_fraction(curve, target, not_reached):
    for row in curve:
        if row["accuracy"] >= target:
            return float(row["fraction"])
    return float(not_reached)


def evaluate_futures(checkpoints, base_state, input_dim, cfg, x_train, y_train, x_test, y_test):
    rows = []
    for idx, cp in enumerate(checkpoints):
        pseed = stable_seed(cfg["future_task"]["future_permutation_seed"], idx)
        oseed = stable_seed(cfg["future_task"]["future_example_order_seed"], idx)
        perm = random_permutation(input_dim, pseed)
        order = batch_order(len(x_train), oseed)
        checkpoint_curve = future_learning_curve(
            cp["state_dict"], base_state, False, input_dim,
            x_train, y_train, x_test, y_test, perm, order, cfg
        )
        fresh_curve = future_learning_curve(
            cp["state_dict"], base_state, True, input_dim,
            x_train, y_train, x_test, y_test, perm, order, cfg
        )
        cp_auc = auc_accuracy(checkpoint_curve)
        fresh_auc = auc_accuracy(fresh_curve)
        fresh_final = float(fresh_curve[-1]["accuracy"])
        target = float(cfg["future_task"]["t_epsilon_fraction_of_fresh_final_accuracy"]) * fresh_final
        not_reached = float(cfg["future_task"]["not_reached_value"])
        cp_t90 = t90_fraction(checkpoint_curve, target, not_reached)
        fresh_t90 = t90_fraction(fresh_curve, target, not_reached)

        clean_cp = {k: v for k, v in cp.items() if k != "state_dict"}
        clean_cp["parameter_sketch"] = clean_cp["parameter_sketch"].tolist()
        rows.append(
            {
                **clean_cp,
                "future_task_index": idx,
                "delta_auc_accuracy": float(cp_auc - fresh_auc),
                "t90_gap_fraction": float(cp_t90 - fresh_t90),
                "checkpoint_auc": cp_auc,
                "fresh_auc": fresh_auc,
                "checkpoint_t90": cp_t90,
                "fresh_t90": fresh_t90,
                "fresh_final_accuracy": fresh_final,
                "checkpoint_curve": checkpoint_curve,
                "fresh_curve": fresh_curve,
            }
        )
    return rows


BASE_CAPABILITY = ["task_age", "current_task_accuracy", "current_task_loss"]
PLASTICITY_EXTRA = [
    "parameter_l2",
    "mean_abs_parameter",
    "distance_from_initialization_l2",
    "gradient_l2_on_probe",
    "dead_relu_fraction",
    "activation_effective_rank_fraction",
    "activation_std",
]


def feature_matrix(rows, model_name):
    if model_name == "age_only":
        names = ["task_age"]
    elif model_name == "capability":
        names = BASE_CAPABILITY
    elif model_name == "plasticity":
        names = BASE_CAPABILITY + PLASTICITY_EXTRA
    elif model_name == "rich":
        names = BASE_CAPABILITY + PLASTICITY_EXTRA
    else:
        raise ValueError(model_name)

    x = np.asarray([[float(row[n]) for n in names] for row in rows], dtype=float)
    if model_name == "rich":
        sketch = np.asarray([row["parameter_sketch"] for row in rows], dtype=float)
        x = np.column_stack([x, sketch])
    return x


def choose_alpha(x, y, groups, alphas, inner_splits):
    unique_groups = np.unique(groups)
    n_splits = min(inner_splits, len(unique_groups))
    if n_splits < 2:
        return float(alphas[0])
    cv = GroupKFold(n_splits=n_splits)
    best_alpha = None
    best_mse = None
    for alpha in alphas:
        fold_losses = []
        for tr, va in cv.split(x, y, groups):
            scaler = StandardScaler().fit(x[tr])
            xt = scaler.transform(x[tr])
            xv = scaler.transform(x[va])
            model = Ridge(alpha=float(alpha)).fit(xt, y[tr])
            pred = model.predict(xv)
            fold_losses.append(mean_squared_error(y[va], pred))
        score = float(np.mean(fold_losses))
        if best_mse is None or score < best_mse:
            best_mse = score
            best_alpha = float(alpha)
    return best_alpha


def oof_predict(rows, outcome, model_name, cfg):
    y = np.asarray([float(r[outcome]) for r in rows], dtype=float)
    groups = np.asarray([int(r["history_run"]) for r in rows])
    x = feature_matrix(rows, model_name)
    unique_groups = np.unique(groups)
    outer_splits = min(int(cfg["forecast"]["outer_group_folds"]), len(unique_groups))
    outer = GroupKFold(n_splits=outer_splits)
    pred = np.full(len(rows), np.nan, dtype=float)
    null_pred = np.full(len(rows), np.nan, dtype=float)
    selected = []
    alphas = [float(a) for a in cfg["forecast"]["ridge_alphas"]]
    inner_splits = int(cfg["forecast"]["inner_group_folds"])
    for fold, (tr, te) in enumerate(outer.split(x, y, groups)):
        alpha = choose_alpha(x[tr], y[tr], groups[tr], alphas, inner_splits)
        scaler = StandardScaler().fit(x[tr])
        model = Ridge(alpha=alpha).fit(scaler.transform(x[tr]), y[tr])
        pred[te] = model.predict(scaler.transform(x[te]))
        null_pred[te] = float(np.mean(y[tr]))
        selected.append({"fold": fold, "alpha": alpha, "test_groups": sorted(map(int, np.unique(groups[te])))})
    return y, groups, pred, null_pred, selected


def metrics(y, pred):
    return {
        "rmse": float(math.sqrt(mean_squared_error(y, pred))),
        "mae": float(mean_absolute_error(y, pred)),
        "r2": float(r2_score(y, pred)),
    }


def bootstrap_rmse_difference(y, groups, pred_a, pred_b, n_boot, seed):
    rng = np.random.default_rng(seed)
    unique = np.unique(groups)
    diffs = []
    group_to_idx = {g: np.flatnonzero(groups == g) for g in unique}
    for _ in range(n_boot):
        sampled = rng.choice(unique, size=len(unique), replace=True)
        idx = np.concatenate([group_to_idx[g] for g in sampled])
        rmse_a = math.sqrt(mean_squared_error(y[idx], pred_a[idx]))
        rmse_b = math.sqrt(mean_squared_error(y[idx], pred_b[idx]))
        diffs.append(rmse_a - rmse_b)
    arr = np.asarray(diffs, dtype=float)
    return {
        "point": float(math.sqrt(mean_squared_error(y, pred_a)) - math.sqrt(mean_squared_error(y, pred_b))),
        "bootstrap_95": [float(np.quantile(arr, 0.025)), float(np.quantile(arr, 0.975))],
    }


def forecast_analysis(rows, cfg):
    outcomes = list(cfg["outcomes"]["primary"])
    model_names = ["age_only", "capability", "plasticity", "rich"]
    analysis = {}
    for oi, outcome in enumerate(outcomes):
        model_data = {}
        null_metrics = None
        null_pred_ref = None
        y_ref = None
        groups_ref = None
        for model_name in model_names:
            y, groups, pred, null_pred, selected = oof_predict(rows, outcome, model_name, cfg)
            if y_ref is None:
                y_ref, groups_ref, null_pred_ref = y, groups, null_pred
                null_metrics = metrics(y, null_pred)
            model_data[model_name] = {
                "metrics": metrics(y, pred),
                "selected_alphas": selected,
                "predictions": pred,
            }

        comparisons = {
            "G0_null_vs_rich": (null_pred_ref, model_data["rich"]["predictions"]),
            "G1_age_vs_capability": (model_data["age_only"]["predictions"], model_data["capability"]["predictions"]),
            "G2_capability_vs_plasticity": (model_data["capability"]["predictions"], model_data["plasticity"]["predictions"]),
            "G3_plasticity_vs_rich": (model_data["plasticity"]["predictions"], model_data["rich"]["predictions"]),
        }
        comp_out = {}
        for ci, (name, (pa, pb)) in enumerate(comparisons.items()):
            comp_out[name] = bootstrap_rmse_difference(
                y_ref,
                groups_ref,
                pa,
                pb,
                int(cfg["forecast"]["bootstrap_history_resamples"]),
                stable_seed(cfg["forecast"]["bootstrap_seed"], oi, ci),
            )
        analysis[outcome] = {
            "null_metrics": null_metrics,
            "models": {
                name: {
                    "metrics": model_data[name]["metrics"],
                    "selected_alphas": model_data[name]["selected_alphas"],
                }
                for name in model_names
            },
            "comparisons": comp_out,
        }
    return analysis


def summarize_rows(rows):
    ages = sorted(set(int(r["task_age"]) for r in rows))
    out = {}
    for age in ages:
        rr = [r for r in rows if int(r["task_age"]) == age]
        out[str(age)] = {
            "n": len(rr),
            "delta_auc_accuracy_mean": float(np.mean([r["delta_auc_accuracy"] for r in rr])),
            "delta_auc_accuracy_sd": float(np.std([r["delta_auc_accuracy"] for r in rr], ddof=1)) if len(rr) > 1 else 0.0,
            "t90_gap_fraction_mean": float(np.mean([r["t90_gap_fraction"] for r in rr])),
            "current_task_accuracy_mean": float(np.mean([r["current_task_accuracy"] for r in rr])),
        }
    return out


def run(cfg, smoke=False):
    cfg = copy.deepcopy(cfg)
    torch.manual_seed(0)
    np.random.seed(0)
    if smoke:
        cfg["model"]["batch_size"] = 32
        x_train, y_train, x_test, y_test = make_synthetic_smoke(seed=20261999)
    else:
        x_train, y_train, x_test, y_test = load_real_mnist(cfg)
    x_train, y_train, x_test, y_test = choose_subsets(x_train, y_train, x_test, y_test, cfg, smoke)

    checkpoints, base_state, input_dim = build_checkpoints(
        cfg, x_train, y_train, x_test, y_test, smoke=smoke
    )
    rows = evaluate_futures(
        checkpoints, base_state, input_dim, cfg,
        x_train, y_train, x_test, y_test
    )
    analysis = forecast_analysis(rows, cfg)
    return {
        "schema_version": 1,
        "study": cfg["study"],
        "status": "SMOKE_ONLY" if smoke else "G0_G3_BENCHMARK_OUTCOME",
        "authority": cfg["authority"],
        "n_checkpoint_future_pairs": len(rows),
        "age_summary": summarize_rows(rows),
        "forecast_analysis": analysis,
        "rows": rows,
        "guardrails": [
            "Future task identity is not a checkpoint predictor input.",
            "Forecastability is predictive, not causal.",
            "The 32-D parameter sketch is a broad state adversary, not the full predictive state.",
            "Failure of G0-G3 does not prove future trainability is intrinsically unpredictable.",
            "G4-G6 are not authorized by this run.",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("config")
    p.add_argument("--json-out", required=True)
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()
    cfg = load_config(args.config)
    result = run(cfg, smoke=args.smoke)
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "n_checkpoint_future_pairs": result["n_checkpoint_future_pairs"],
        "age_summary": result["age_summary"],
        "out": args.json_out,
    }, indent=2))


if __name__ == "__main__":
    main()
