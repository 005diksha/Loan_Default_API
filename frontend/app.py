import streamlit as st
import requests


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }

        .result-box {
            padding: 25px;
            border-radius: 12px;
            margin-top: 20px;
            text-align: center;
        }

        .success-box {
            background-color: #e8f5e9;
            border: 1px solid #81c784;
        }

        .danger-box {
            background-color: #ffebee;
            border: 1px solid #e57373;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# API URL
# --------------------------------------------------

API_URL = "https://loan-default-api-2.onrender.com/predict"


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">💰 Loan Default Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Enter the applicant and loan details to estimate default risk.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------

with st.form("loan_form"):

    st.subheader("Loan Information")

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------
    # COLUMN 1
    # --------------------------------------------------

    with col1:

        loan_amnt = st.number_input(
            "Loan Amount ($)",
            min_value=0.0,
            value=15000.0,
            step=500.0
        )

        funded_amnt = st.number_input(
            "Funded Amount ($)",
            min_value=0.0,
            value=15000.0,
            step=500.0
        )

        term = st.selectbox(
            "Loan Term",
            ["36 months", "60 months"]
        )

        int_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=12.5,
            step=0.1
        )

        installment = st.number_input(
            "Monthly Installment ($)",
            min_value=0.0,
            value=500.0,
            step=10.0
        )

    # --------------------------------------------------
    # COLUMN 2
    # --------------------------------------------------

    with col2:

        grade = st.selectbox(
            "Loan Grade",
            ["A", "B", "C", "D", "E", "F", "G"]
        )

        sub_grade = st.selectbox(
            "Sub Grade",
            [
                "A1", "A2", "A3", "A4", "A5",
                "B1", "B2", "B3", "B4", "B5",
                "C1", "C2", "C3", "C4", "C5",
                "D1", "D2", "D3", "D4", "D5",
                "E1", "E2", "E3", "E4", "E5",
                "F1", "F2", "F3", "F4", "F5",
                "G1", "G2", "G3", "G4", "G5"
            ]
        )

        emp_length = st.selectbox(
            "Employment Length",
            [
                "< 1 year",
                "1 year",
                "2 years",
                "3 years",
                "4 years",
                "5 years",
                "6 years",
                "7 years",
                "8 years",
                "9 years",
                "10+ years"
            ]
        )

        home_ownership = st.selectbox(
            "Home Ownership",
            ["RENT", "OWN", "MORTGAGE", "OTHER"]
        )

        annual_inc = st.number_input(
            "Annual Income ($)",
            min_value=0.0,
            value=60000.0,
            step=1000.0
        )

        verification_status = st.selectbox(
            "Verification Status",
            ["Verified", "Source Verified", "Not Verified"]
        )

    # --------------------------------------------------
    # COLUMN 3
    # --------------------------------------------------

    with col3:

        dti = st.number_input(
            "Debt-to-Income Ratio",
            min_value=0.0,
            max_value=100.0,
            value=18.5,
            step=0.1
        )

        addr_state = st.text_input(
            "State",
            value="CA",
            max_chars=2
        ).upper()

        fico_score = st.number_input(
            "FICO Score",
            min_value=300,
            max_value=850,
            value=700,
            step=1
        )

        revol_bal = st.number_input(
            "Revolving Balance ($)",
            min_value=0.0,
            value=8000.0,
            step=100.0
        )

        total_acc = st.number_input(
            "Total Accounts",
            min_value=0,
            value=20,
            step=1
        )

    # --------------------------------------------------
    # CREDIT INFORMATION
    # --------------------------------------------------

    st.subheader("Credit Information")

    col4, col5, col6 = st.columns(3)

    with col4:

        application_type = st.selectbox(
            "Application Type",
            ["Individual", "Joint App"]
        )

    with col5:

        open_acc = st.number_input(
            "Open Accounts",
            min_value=0,
            value=10,
            step=1
        )

    with col6:

        inq_last_6mths = st.number_input(
            "Inquiries in Last 6 Months",
            min_value=0,
            value=1,
            step=1
        )

    col7, col8 = st.columns(2)

    with col7:

        delinq_2yrs = st.number_input(
            "Delinquencies in Last 2 Years",
            min_value=0,
            value=0,
            step=1
        )

    with col8:

        pub_rec = st.number_input(
            "Public Records",
            min_value=0,
            value=0,
            step=1
        )

    st.markdown("---")

    submitted = st.form_submit_button(
        "🔮 Predict Default Risk",
        use_container_width=True
    )


# --------------------------------------------------
# SEND DATA TO API
# --------------------------------------------------

if submitted:

    payload = {
        "loan_amnt": loan_amnt,
        "funded_amnt": funded_amnt,
        "term": term,
        "int_rate": int_rate,
        "installment": installment,
        "grade": grade,
        "sub_grade": sub_grade,
        "emp_length": emp_length,
        "home_ownership": home_ownership,
        "annual_inc": annual_inc,
        "verification_status": verification_status,
        "dti": dti,
        "addr_state": addr_state,
        "fico_score": fico_score,
        "revol_bal": revol_bal,
        "total_acc": total_acc,
        "application_type": application_type,
        "open_acc": open_acc,
        "inq_last_6mths": inq_last_6mths,
        "delinq_2yrs": delinq_2yrs,
        "pub_rec": pub_rec
    }

    with st.spinner("Analyzing loan application..."):

        try:

            response = requests.post(
                API_URL,
                json=payload,
                timeout=60
            )

            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            if response.status_code == 200:

                result = response.json()

                prediction = result.get(
                    "prediction",
                    "Unknown"
                )

                probability = result.get(
                    "default_probability",
                    0
                )

                risk_level = result.get(
                    "risk_level",
                    "Unknown"
                )

                probability_percent = probability * 100

                st.markdown("---")

                st.subheader("📊 Prediction Result")

                # --------------------------------------------------
                # LOW RISK / NO DEFAULT
                # --------------------------------------------------

                if prediction == "No Default":

                    st.markdown(
                        f"""
                        <div class="result-box success-box">
                            <h2>🟢 Low Default Risk</h2>

                            <h3>
                                Prediction: {prediction}
                            </h3>

                            <p style="font-size: 20px;">
                                Default Probability:
                                <strong>
                                    {probability_percent:.2f}%
                                </strong>
                            </p>

                            <p style="font-size: 18px;">
                                Risk Level:
                                <strong>
                                    {risk_level}
                                </strong>
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.progress(probability)

                    st.info(
                        "The applicant is currently classified "
                        "as low risk based on the provided loan "
                        "and credit information."
                    )

                # --------------------------------------------------
                # HIGH RISK / DEFAULT
                # --------------------------------------------------

                else:

                    st.markdown(
                        f"""
                        <div class="result-box danger-box">
                            <h2>🔴 High Default Risk</h2>

                            <h3>
                                Prediction: {prediction}
                            </h3>

                            <p style="font-size: 20px;">
                                Default Probability:
                                <strong>
                                    {probability_percent:.2f}%
                                </strong>
                            </p>

                            <p style="font-size: 18px;">
                                Risk Level:
                                <strong>
                                    {risk_level}
                                </strong>
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.progress(probability)

                    st.warning(
                        "The applicant has been classified "
                        "as having a higher default risk based "
                        "on the provided information."
                    )

            # --------------------------------------------------
            # API ERROR
            # --------------------------------------------------

            else:

                st.error(
                    f"API returned an error: "
                    f"{response.status_code}"
                )

                st.code(response.text)

        # --------------------------------------------------
        # CONNECTION ERROR
        # --------------------------------------------------

        except requests.exceptions.RequestException as e:

            st.error(
                "Could not connect to the prediction API."
            )

            st.write(str(e))


