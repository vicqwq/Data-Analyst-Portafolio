# EV Purchase Prediction — Pipeline Documentation

## 📌 Project Overview

This project builds a machine learning pipeline to predict the likelihood that a customer will purchase an electric vehicle (EV). It answers the business question: **which customer attributes predict EV purchase likelihood?** The pipeline follows a medallion architecture — raw data flows through cleaning, feature engineering, model training, and prediction steps, each tracked in a dedicated data layer. The final model outputs a probability score (0–1) per customer, not a simple yes/no label.

**Target audience:** data scientists and analysts who need to understand, extend, or reproduce the work; business stakeholders who want to understand what drives the model's predictions.

---

## 📁 Folder Structure

```
manual/
├── data/
│   ├── Bronze layer/               ← Raw, unmodified source files — never edit these
│   │   ├── train.csv               ← Labelled training data (~668k rows)
│   │   ├── test.csv                ← Unlabelled test data (~286k rows)
│   │   └── sample_submission.csv   ← Expected submission format (id + probability)
│   ├── Silver layer/               ← Cleaned and standardised data
│   │   ├── train_cleaned.csv       ← Cleaned train set (scaled numerics, encoded categoricals)
│   │   ├── test_cleaned.csv        ← Cleaned test set using the same fitted scalers
│   │   └── train_interactions.csv  ← Intermediate interaction features for the train set
│   ├── Gold layer/                 ← Feature-engineered data ready for modelling
│   │   ├── train_engineered.csv    ← Train set with all 10 engineered interaction features added
│   │   └── test_engineered.csv     ← Test set with the same features applied
│   └── model_output/               ← Final prediction files per model
│       ├── test_LogReg_output.csv          ← Logistic Regression probabilities on test set
│       ├── test_XGBoost_output.csv         ← XGBoost probabilities on test set (winning model)
│       └── train_XGBoost_output.csv        ← XGBoost probabilities on train set
└── main_scripts/                   ← Executable notebooks and all saved artifacts
    ├── 1.eda_data_cleaning.ipynb           ← EDA, IV analysis, Silver + Gold transformations
    ├── 2.model_training.ipynb              ← Model training, tuning, evaluation, artifact saving
    ├── 3.pipeline_model_evaluation.ipynb   ← Applies pipeline to new data and generates predictions
    ├── catboost_info/                      ← CatBoost training logs (auto-generated)
    ├── pipeline_artifacts/                 ← Fitted transformer parameters and trained model
    │   ├── best_model.pkl          ← Serialised winning model (XGBoost, tuned)
    │   ├── encoder_params.json     ← Fitted encoder mappings for categorical columns
    │   ├── model_metadata.json     ← AUC-ROC, hyperparameters, feature list, training date
    │   └── scaler_params.json      ← Fitted scaler parameters for numeric columns
    └── Reports/                    ← Analysis reports, charts, and model comparison
        ├── feature_selection/      ← IV analysis outputs (Excel + Markdown)
        ├── features_interactions/  ← SHAP interaction analysis (CSV + PNG)
        ├── figures/                ← ROC curves, PR curves, confusion matrices, feature importance
        └── model_comparison_report.md  ← Full CV and held-out metrics across all models
```

---

## 🔄 Pipeline Flow

```
Raw Data (Bronze layer)
    ↓  [1.eda_data_cleaning.ipynb — EDA + Silver transformation]
    Performs exploratory analysis and IV scoring to identify predictive features,
    then standardises numerics and encodes categoricals, fitting scaler and
    encoder parameters that are saved to pipeline_artifacts/.

    ↓  [1.eda_data_cleaning.ipynb — Gold transformation]
    Adds 14 engineered interaction features (e.g. env × subsidy flags, income
    segments, exact income/commute encodings, EV propensity score) derived from
    SHAP interaction analysis.

Engineered Data (Gold layer)
    ↓  [2.model_training.ipynb]
    Runs stratified 5-fold cross-validation on 5 classifiers (Logistic Regression,
    Random Forest, LightGBM, XGBoost, CatBoost) across Silver and Gold feature
    sets, then tunes the best model with Optuna (150 trials) and evaluates it on
    a 20% held-out split, saving best_model.pkl and model_metadata.json.

Trained Model + Artifacts (pipeline_artifacts/)
    ↓  [3.pipeline_model_evaluation.ipynb]
    Loads new raw data, applies the saved Silver and Gold transformations using
    fitted artifacts, then scores it with best_model.pkl and writes probability
    outputs to model_output/.

Predictions + Reports (model_output/ + Reports/)
```

---

## 🚀 How to Reproduce

### Prerequisites

- Python 3.10+
- Required libraries:

```bash
pip install xgboost lightgbm catboost scikit-learn optuna shap pandas numpy openpyxl
```

### Execution order

Run the three notebooks **in this exact order**:

| Step | Notebook | What it does |
|---|---|---|
| 1 | `1.eda_data_cleaning.ipynb` | EDA, IV analysis, Silver + Gold transformations for training data. Saves `scaler_params.json` and `encoder_params.json`. |
| 2 | `2.model_training.ipynb` | Trains and tunes all models on the Gold training set. Saves `best_model.pkl` and `model_metadata.json`. |
| 3 | `3.pipeline_model_evaluation.ipynb` | Applies the full pipeline to test data and generates predictions. |

### Important dependencies between steps

- `scaler_params.json` and `encoder_params.json` are **fitted on `train.csv`** during Step 1. They must exist before running Step 3, which uses them to transform `test.csv` consistently.
- `best_model.pkl` must exist (created in Step 2) before Step 3 can score any data.

---

## 📊 Key Outputs

| Output | Location | What it contains |
|---|---|---|
| Model comparison report | `main_scripts/Reports/model_comparison_report.md` | Full CV and held-out metrics for all 5 models on Silver and Gold feature sets |
| Best model | `main_scripts/pipeline_artifacts/best_model.pkl` | Serialised, tuned XGBoost model ready for inference |
| Model metadata | `main_scripts/pipeline_artifacts/model_metadata.json` | AUC-ROC (0.9427), full hyperparameters, feature list, training timestamp |
| Test predictions (XGBoost) | `data/model_output/test_XGBoost_output.csv` | Final probability predictions on unseen test data |
| Figures and plots | `main_scripts/Reports/figures/` | ROC curves, PR curves, feature importance, SHAP beeswarm, confusion matrices, Optuna history |

### Best model performance (XGBoost — Gold features, 20% held-out split, trained 2026-09-21)

| Metric | Value | What it means |
|---|---|---|
| AUC-ROC | **0.9427** | Overall ranking ability across all thresholds — primary selection metric |
| AUC-PR | 0.7603 | Precision-Recall trade-off; relevant given class imbalance |
| F1 | 0.6884 | Harmonic mean of precision and recall at the optimal threshold |
| Precision | 0.5533 | Of customers predicted as buyers, 55% actually buy |
| Recall | 0.9106 | The model catches 91% of all actual buyers |
| Brier Score | 0.1001 | Mean squared error of the predicted probabilities (lower is better) |
| KS Statistic | 0.7555 | Maximum separation between buyer and non-buyer score distributions |

---

## ⚠️ Important Notes

- **Leakage flags:** `Environmental_Concern_Level` (IV = 2.26) and `Subsidy_Available` (IV = 1.82) were flagged during IV analysis as potential leakage features (IV > 1.5 is suspicious). They are present in the final model — treat their contribution with caution and verify whether they are available at prediction time in production.
- **Winning model:** XGBoost on the Gold feature set — AUC-ROC **0.9427** on the held-out 20% split. Selected as the best model across Phase 1 cross-validation.
- **Random seed:** All randomness is controlled via `RANDOM_SEED = 40` for full reproducibility.
- **Bronze layer is read-only:** Files in `data/Bronze layer/` are the raw source of truth. Never modify them — all transformations write to Silver or Gold layers.
