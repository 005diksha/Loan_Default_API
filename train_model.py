import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score
)


# ============================================================
# 1. SETTINGS
# ============================================================

DATA_PATH = "data/loan.csv"
MODEL_PATH = "model/loan_default_pipeline.pkl"

# Set this to None if you want to train on all eligible rows.
# 300000 makes initial training faster on a normal laptop.
SAMPLE_SIZE = 300000

RANDOM_STATE = 42


# ============================================================
# 2. LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Original dataset shape:", df.shape)


# ============================================================
# 3. CHECK TARGET
# ============================================================

print("\nOriginal loan status distribution:")
print(df["loan_status"].value_counts(dropna=False))


# ============================================================
# 4. KEEP ONLY FINAL LOAN OUTCOMES
# ============================================================

df = df[
    df["loan_status"].isin(
        ["Fully Paid", "Charged Off"]
    )
].copy()

print("\nShape after selecting final loan outcomes:")
print(df.shape)


# ============================================================
# 5. CREATE TARGET VARIABLE
# ============================================================

# Fully Paid  -> 0
# Charged Off -> 1

df["default"] = (
    df["loan_status"] == "Charged Off"
).astype(int)

print("\nTarget distribution:")
print(df["default"].value_counts())

print("\nTarget percentage:")
print(df["default"].value_counts(normalize=True))


# ============================================================
# 6. SELECT FEATURES
# ============================================================

FEATURES = [
    "loan_amnt",
    "funded_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "annual_inc",
    "verification_status",
    "dti",
    "addr_state",
    "fico_score",
    "revol_bal",
    "total_acc",
    "application_type",
    "open_acc",
    "inq_last_6mths",
    "delinq_2yrs",
    "pub_rec"
]

TARGET = "default"


# ============================================================
# 7. CHECK THAT FEATURES EXIST
# ============================================================

missing_features = [
    column for column in FEATURES
    if column not in df.columns
]

if missing_features:
    raise ValueError(
        f"These features are missing from the dataset: "
        f"{missing_features}"
    )

print("\nSelected features:")
for feature in FEATURES:
    print("-", feature)


# ============================================================
# 8. SELECT X AND y
# ============================================================

X = df[FEATURES].copy()
y = df[TARGET].copy()


# ============================================================
# 9. OPTIONAL SAMPLE FOR FASTER LOCAL TRAINING
# ============================================================

if SAMPLE_SIZE is not None and len(X) > SAMPLE_SIZE:

    print(
        f"\nUsing stratified sample of "
        f"{SAMPLE_SIZE:,} rows for training."
    )

    X, _, y, _ = train_test_split(
        X,
        y,
        train_size=SAMPLE_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

print("\nFinal modeling dataset:", X.shape)


# ============================================================
# 10. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ============================================================
# 11. DEFINE NUMERICAL FEATURES
# ============================================================

NUMERICAL_FEATURES = [
    "loan_amnt",
    "funded_amnt",
    "int_rate",
    "installment",
    "annual_inc",
    "dti",
    "fico_score",
    "revol_bal",
    "total_acc",
    "open_acc",
    "inq_last_6mths",
    "delinq_2yrs",
    "pub_rec"
]


# ============================================================
# 12. DEFINE CATEGORICAL FEATURES
# ============================================================

CATEGORICAL_FEATURES = [
    "term",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "verification_status",
    "addr_state",
    "application_type"
]


# ============================================================
# 13. NUMERICAL PREPROCESSING
# ============================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)


# ============================================================
# 14. CATEGORICAL PREPROCESSING
# ============================================================

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


# ============================================================
# 15. COMBINE PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            NUMERICAL_FEATURES
        ),
        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_FEATURES
        )
    ]
)


# ============================================================
# 16. CREATE ML MODEL
# ============================================================

model = LogisticRegression(
    max_iter=1000,
    random_state=RANDOM_STATE
)


# ============================================================
# 17. CREATE COMPLETE PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# 18. TRAIN MODEL
# ============================================================

print("\nTraining Logistic Regression model...")

pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# 19. PREDICTIONS
# ============================================================

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(
    X_test
)[:, 1]


# ============================================================
# 20. EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n========================================")
print("MODEL PERFORMANCE")
print("========================================")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "No Default",
            "Default"
        ],
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# 21. CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(
    "model",
    exist_ok=True
)


# ============================================================
# 22. SAVE COMPLETE PIPELINE
# ============================================================

joblib.dump(
    pipeline,
    MODEL_PATH
)

print("\n========================================")
print("MODEL SAVED")
print("========================================")

print(
    f"Saved model to: {MODEL_PATH}"
)