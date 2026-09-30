from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import sqlite3
from datetime import datetime


# ============================================================
# 1. CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Loan Default Prediction API",
    description="ML API for predicting loan default risk",
    version="1.0"
)


# ============================================================
# 2. LOAD TRAINED MODEL
# ============================================================

MODEL_PATH = "model/loan_default_pipeline.pkl"

model = joblib.load(MODEL_PATH)


# ============================================================
# 3. DATABASE
# ============================================================

DATABASE = "predictions.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            loan_amnt REAL,
            annual_inc REAL,
            dti REAL,
            default_probability REAL,
            prediction TEXT,
            risk_level TEXT
        )
    """)

    connection.commit()
    connection.close()


# Create database when application starts
create_database()


# ============================================================
# 4. INPUT DATA MODEL
# ============================================================

class LoanInput(BaseModel):

    loan_amnt: float
    funded_amnt: float
    term: str
    int_rate: float
    installment: float
    grade: str
    sub_grade: str
    emp_length: str
    home_ownership: str
    annual_inc: float
    verification_status: str
    dti: float
    addr_state: str
    fico_score: float
    revol_bal: float
    total_acc: float
    application_type: str
    open_acc: float
    inq_last_6mths: float
    delinq_2yrs: float
    pub_rec: float


# ============================================================
# 5. HOME ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Loan Default Prediction API is running",
        "version": "1.0"
    }


# ============================================================
# 6. HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# 7. PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(loan: LoanInput):

    # Convert input into dictionary
    loan_data = loan.model_dump()

    # Convert dictionary into DataFrame
    data = pd.DataFrame(
        [loan_data]
    )

    # Calculate default probability
    probability = model.predict_proba(
        data
    )[0][1]

    # Classification threshold
    prediction_value = int(
        probability >= 0.50
    )

    # Convert prediction into text
    if prediction_value == 1:

        prediction = "Default"

    else:

        prediction = "No Default"


    # Determine risk level
    if probability >= 0.70:

        risk_level = "High"

    elif probability >= 0.40:

        risk_level = "Medium"

    else:

        risk_level = "Low"


    # ========================================================
    # SAVE PREDICTION TO DATABASE
    # ========================================================

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            timestamp,
            loan_amnt,
            annual_inc,
            dti,
            default_probability,
            prediction,
            risk_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(),
            loan.loan_amnt,
            loan.annual_inc,
            loan.dti,
            float(probability),
            prediction,
            risk_level
        )
    )

    connection.commit()
    connection.close()


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "default_probability":
            round(float(probability), 4),

        "prediction":
            prediction,

        "risk_level":
            risk_level
    }


# ============================================================
# 8. VIEW PREDICTION HISTORY
# ============================================================

@app.get("/predictions")
def get_predictions():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            timestamp,
            loan_amnt,
            annual_inc,
            dti,
            default_probability,
            prediction,
            risk_level
        FROM predictions
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()


    # Convert database rows to JSON
    results = []

    for row in rows:

        results.append({

            "id": row[0],
            "timestamp": row[1],
            "loan_amnt": row[2],
            "annual_inc": row[3],
            "dti": row[4],
            "default_probability": row[5],
            "prediction": row[6],
            "risk_level": row[7]

        })


    return {
        "count": len(results),
        "predictions": results
    }