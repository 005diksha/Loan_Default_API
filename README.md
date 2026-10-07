# Loan Default Prediction API

An end-to-end machine learning application that predicts whether a loan applicant is likely to default. The project includes a machine learning pipeline, FastAPI backend, and Streamlit web interface.

## 🚀 Live Application

**Frontend:**
[Loan Default Prediction App]
https://loandefaultapi-mqghusrvjqvarjq6zxiddn.streamlit.app/

**Backend API:**
 [FastAPI Backend]
https://loan-default-api-2.onrender.com

> Replace the frontend URL above with the exact Streamlit URL generated for your application.

---

## 📌 Project Overview

Loan default prediction is a binary classification problem where the objective is to identify whether a borrower is likely to default on a loan.

This project takes applicant and loan information as input and predicts:

* Default probability
* Default / No Default prediction
* Risk level

The application provides an easy-to-use web interface for making predictions.

---

## 🏗️ Project Architecture

```text
User
  │
  ▼
Streamlit Frontend
  │
  │ HTTP POST Request
  ▼
FastAPI Backend
  │
  ▼
Machine Learning Pipeline
  │
  ▼
Prediction
  │
  ├── Default Probability
  ├── Prediction
  └── Risk Level
```

---

## 🛠️ Technologies Used

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib

### Backend

* FastAPI
* Uvicorn
* REST API

### Frontend

* Streamlit
* Requests

### Deployment

* Render
* Streamlit Community Cloud
* GitHub

---

## 📊 Input Features

The model uses the following features:

1. Loan Amount
2. Funded Amount
3. Loan Term
4. Interest Rate
5. Installment
6. Grade
7. Sub Grade
8. Employment Length
9. Home Ownership
10. Annual Income
11. Verification Status
12. Debt-to-Income Ratio
13. Address State
14. FICO Score
15. Revolving Balance
16. Total Accounts
17. Application Type
18. Open Accounts
19. Inquiries in Last 6 Months
20. Delinquencies in Last 2 Years
21. Public Records

---

## 🔮 Prediction Output

The API returns three important results:

### Default Probability

The estimated probability that the borrower will default.

### Prediction

The final classification:

* `Default`
* `No Default`

### Risk Level

A simplified risk category such as:

* Low
* Medium
* High

---

## 🌐 API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Prediction

```http
POST /predict
```

Example request:

```json
{
  "loan_amnt": 15000,
  "funded_amnt": 15000,
  "term": "36 months",
  "int_rate": 12.5,
  "installment": 500,
  "grade": "B",
  "sub_grade": "B3",
  "emp_length": "5 years",
  "home_ownership": "RENT",
  "annual_inc": 60000,
  "verification_status": "Verified",
  "dti": 18.5,
  "addr_state": "CA",
  "fico_score": 700,
  "revol_bal": 8000,
  "total_acc": 20,
  "application_type": "Individual",
  "open_acc": 10,
  "inq_last_6mths": 1,
  "delinq_2yrs": 0,
  "pub_rec": 0
}
```

Example response:

```json
{
  "default_probability": 0.1137,
  "prediction": "No Default",
  "risk_level": "Low"
}
```

---

## 📁 Project Structure

```text
Loan_Default_API/
│
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── .gitignore
├── .python-version
│
├── data/
│   └── loan.csv
│
├── model/
│   └── loan_default_pipeline.pkl
│
└── frontend/
    ├── app.py
    └── requirements.txt
```

---

## ⚙️ Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/005diksha/Loan_Default_API.git
cd Loan_Default_API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI server

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 6. Run the Streamlit frontend

Open another terminal:

```bash
cd frontend
streamlit run app.py
```

The frontend will be available at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

### Backend

The FastAPI backend is deployed using Render.

### Frontend

The Streamlit application is deployed using Streamlit Community Cloud.

The frontend communicates with the deployed FastAPI backend through HTTP requests.

---

## 🎯 Key Features

* Machine learning based loan default prediction
* Probability-based risk assessment
* FastAPI REST API
* Interactive Streamlit interface
* Cloud deployment
* Clean separation between frontend and backend
* Real-time prediction through API requests

---

## 🔐 Important Note

This project is intended for educational and demonstration purposes. Predictions should not be used as the sole basis for real-world lending decisions.

---

## 👩‍💻 Author

**Diksha**

Loan Default Prediction API — Machine Learning & API Deployment Project
