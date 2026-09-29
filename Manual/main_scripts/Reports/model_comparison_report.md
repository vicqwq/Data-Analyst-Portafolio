# Model Comparison Report — EV Purchase Prediction
**Generated:** 2026-09-21 22:17  |  **Seed:** 40  |  **CV folds:** 5  |  **Optuna trials:** 150

---

## Phase 1 — Cross-Validation Results

### SILVER features — 5-Fold CV

| Model | AUC-ROC | AUC-PR | F1 | Precision | Recall | Brier ↓ | KS |
|---|---|---|---|---|---|---|---|
| LogReg | 0.6350 ±0.0017 | 0.2642 ±0.0015 | 0.3380 ±0.0009 | 0.2202 ±0.0006 | 0.7268 ±0.0027 | 0.2580 ±0.0002 | 0.1982 ±0.0029 |
| RandomForest | 0.9378 ±0.0003 | 0.7420 ±0.0021 | 0.7077 ±0.0010 | 0.6134 ±0.0009 | 0.8363 ±0.0013 | 0.0836 ±0.0004 | 0.7500 ±0.0017 |
| LightGBM | 0.9421 ±0.0004 | 0.7585 ±0.0025 | 0.6909 ±0.0006 | 0.5568 ±0.0005 | 0.9102 ±0.0018 | 0.0989 ±0.0003 | 0.7574 ±0.0015 |
| XGBoost | 0.9424 ±0.0003 | 0.7596 ±0.0024 | 0.6898 ±0.0010 | 0.5548 ±0.0008 | 0.9117 ±0.0022 | 0.0995 ±0.0002 | 0.7577 ±0.0016 |
| CatBoost | 0.9418 ±0.0003 | 0.7563 ±0.0022 | 0.6856 ±0.0006 | 0.5480 ±0.0006 | 0.9156 ±0.0017 | 0.1013 ±0.0002 | 0.7563 ±0.0017 |

### GOLD features — 5-Fold CV

| Model | AUC-ROC | AUC-PR | F1 | Precision | Recall | Brier ↓ | KS |
|---|---|---|---|---|---|---|---|
| LogReg | 0.6504 ±0.0017 | 0.2804 ±0.0017 | 0.3457 ±0.0008 | 0.2259 ±0.0005 | 0.7363 ±0.0026 | 0.2557 ±0.0002 | 0.2198 ±0.0030 |
| RandomForest | 0.9376 ±0.0003 | 0.7411 ±0.0021 | 0.7070 ±0.0009 | 0.6137 ±0.0012 | 0.8339 ±0.0015 | 0.0837 ±0.0004 | 0.7501 ±0.0017 |
| LightGBM | 0.9421 ±0.0004 | 0.7585 ±0.0027 | 0.6907 ±0.0005 | 0.5562 ±0.0002 | 0.9110 ±0.0014 | 0.0989 ±0.0002 | 0.7576 ±0.0014 |
| XGBoost | 0.9424 ±0.0003 | 0.7596 ±0.0026 | 0.6890 ±0.0007 | 0.5536 ±0.0005 | 0.9123 ±0.0022 | 0.0996 ±0.0002 | 0.7576 ±0.0016 |
| CatBoost | 0.9418 ±0.0003 | 0.7564 ±0.0024 | 0.6859 ±0.0011 | 0.5483 ±0.0010 | 0.9155 ±0.0018 | 0.1013 ±0.0002 | 0.7563 ±0.0019 |

---

## Phase 2 — Best Model & Optuna Tuning

Best Phase-1 model: **XGBoost** on **GOLD** features

Optuna best AUC-ROC (3-fold, 150 trials): **0.9426**

**Tuned hyperparameters:**

```json
{
  "n_estimators": 1422,
  "learning_rate": 0.09800155540717399,
  "max_depth": 3,
  "min_child_weight": 7,
  "subsample": 0.8507948030287987,
  "colsample_bytree": 0.6261385095155073,
  "gamma": 2.5122029905565992,
  "reg_alpha": 5.24425726106788e-08,
  "reg_lambda": 7.210495303924496e-07,
  "scale_pos_weight": 4.72590106097843,
  "eval_metric": "auc",
  "n_jobs": -1,
  "random_state": 40,
  "verbosity": 0
}
```

---

## Held-Out Evaluation (20%)

### SILVER features — Held-Out (20%)

| Model | AUC-ROC | AUC-PR | F1 | Precision | Recall | Brier ↓ | KS | Opt. Threshold |
|---|---|---|---|---|---|---|---|---|
| LogReg | 0.6390 | 0.2693 | 0.3397 | 0.2227 | 0.7159 | 0.2564 | 0.2023 | 0.530 |
| RandomForest | 0.9380 | 0.7443 | 0.7048 | 0.6060 | 0.8422 | 0.0849 | 0.7474 | 0.574 |
| LightGBM | 0.9421 | 0.7574 | 0.6879 | 0.5534 | 0.9087 | 0.0995 | 0.7543 | 0.713 |
| XGBoost | 0.9424 | 0.7597 | 0.6878 | 0.5530 | 0.9094 | 0.0999 | 0.7543 | 0.718 |
| CatBoost | 0.9417 | 0.7560 | 0.6838 | 0.5464 | 0.9133 | 0.1017 | 0.7536 | 0.733 |

### GOLD features — Held-Out (20%)

| Model | AUC-ROC | AUC-PR | F1 | Precision | Recall | Brier ↓ | KS | Opt. Threshold |
|---|---|---|---|---|---|---|---|---|
| LogReg | 0.6568 | 0.2888 | 0.3491 | 0.2296 | 0.7279 | 0.2535 | 0.2242 | 0.559 |
| RandomForest | 0.9379 | 0.7425 | 0.7048 | 0.6059 | 0.8422 | 0.0849 | 0.7474 | 0.564 |
| LightGBM | 0.9420 | 0.7574 | 0.6885 | 0.5539 | 0.9094 | 0.0995 | 0.7545 | 0.738 |
| XGBoost | 0.9427 | 0.7603 | 0.6884 | 0.5533 | 0.9106 | 0.1001 | 0.7555 | 0.713 |
| CatBoost | 0.9418 | 0.7563 | 0.6839 | 0.5466 | 0.9134 | 0.1016 | 0.7535 | 0.733 |

---

## Figures

| File | Description |
|---|---|
| `figures/roc_curves_silver.png` | ROC curves — Silver feature set |
| `figures/roc_curves_gold.png` | ROC curves — Gold feature set |
| `figures/pr_curves_silver.png` | PR curves — Silver feature set |
| `figures/pr_curves_gold.png` | PR curves — Gold feature set |
| `figures/feature_importance.png` | Feature importances — best tuned model |
| `figures/confusion_matrix_default.png` | Confusion matrix at threshold 0.50 |
| `figures/confusion_matrix_optimal.png` | Confusion matrix at optimal F1 threshold |
| `figures/optuna_history.png` | Optuna trial history |
