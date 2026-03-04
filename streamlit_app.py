import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

API_URL = "https://churn-prediction-api-kfa4.onrender.com/predict"

st.set_page_config(page_title="Churn Predictor", layout="wide")

st.title("📊 Customer Churn Prediction Dashboard")

# ---- Layout Columns ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Customer Details")

    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    MonthlyCharges = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
    TotalCharges = st.number_input("Total Charges", 0.0, 10000.0, 840.0)

    gender = st.selectbox("Gender", ["Male", "Female"])
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])
    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
    MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No"])
    InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    OnlineSecurity = st.selectbox("Online Security", ["Yes", "No"])
    OnlineBackup = st.selectbox("Online Backup", ["Yes", "No"])
    DeviceProtection = st.selectbox("Device Protection", ["Yes", "No"])
    TechSupport = st.selectbox("Tech Support", ["Yes", "No"])
    StreamingTV = st.selectbox("Streaming TV", ["Yes", "No"])
    StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No"])
    Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
    PaymentMethod = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )

with col2:
    st.subheader("🔍 Prediction Result")

    if st.button("Predict Churn"):

        data = {
            "SeniorCitizen": SeniorCitizen,
            "tenure": tenure,
            "MonthlyCharges": MonthlyCharges,
            "TotalCharges": TotalCharges,
            "numAdminTickets": 1,
            "numTechTickets": 0,
            "gender": gender,
            "Partner": Partner,
            "Dependents": Dependents,
            "PhoneService": PhoneService,
            "MultipleLines": MultipleLines,
            "InternetService": InternetService,
            "OnlineSecurity": OnlineSecurity,
            "OnlineBackup": OnlineBackup,
            "DeviceProtection": DeviceProtection,
            "TechSupport": TechSupport,
            "StreamingTV": StreamingTV,
            "StreamingMovies": StreamingMovies,
            "Contract": Contract,
            "PaperlessBilling": PaperlessBilling,
            "PaymentMethod": PaymentMethod
        }

        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            result = response.json()
            
            

            top_pos = result["top_positive_factors"]
            top_neg = result["top_negative_factors"]

            # Combine factors into dataframe
            factors = {**top_pos, **top_neg}

            df = pd.DataFrame({
                "Feature": list(factors.keys()),
                "Contribution": list(factors.values())
            })

            df["Impact"] = df["Contribution"].apply(lambda x: "Increase Churn" if x > 0 else "Reduce Churn")
               
            fig = px.bar(
            df,
            x="Contribution",
            y="Feature",
            orientation="h",
            color="Impact",
            color_discrete_map={
                "Increase Churn": "red",
                "Reduce Churn": "green"
            },
            title="Feature Contribution to Prediction"
            )

            st.plotly_chart(fig, use_container_width=True)
                     
            probability = result["churn_probability"]
            prediction = result["churn_prediction"]
            prob_percent = round(probability * 100, 2)
            prob_percent = round(probability * 100, 2)

            st.write(f"### 📊 Churn Probability: {prob_percent}%")

            # ---- Risk Level Logic ----
            if prob_percent < 40:
                risk_level = "LOW RISK"
                st.success("🟢 LOW RISK: Customer is unlikely to churn.")
                st.info("💡 Recommendation: Maintain engagement. No immediate retention action required.")

            elif 40 <= prob_percent < 70:
                risk_level = "MEDIUM RISK"
                st.warning("🟡 MEDIUM RISK: Customer shows moderate churn risk.")
                st.info("💡 Recommendation: Consider targeted offers or loyalty incentives.")

            else:
                risk_level = "HIGH RISK"
                st.error("🔴 HIGH RISK: Customer is very likely to churn!")
                st.info("💡 Recommendation: Immediate retention strategy required (discount, contract upgrade, support call).")
            top_pos = result["top_positive_factors"]
            top_neg = result["top_negative_factors"]

            st.write("### 🔎 Why this prediction?")

            st.write("#### 🚨 Factors Increasing Churn Risk")
            for feature, value in top_pos.items():
                st.write(f"- {feature}")

            st.write("#### 🛡 Factors Reducing Churn Risk")
            for feature, value in top_neg.items():
                st.write(f"- {feature}")
                
            st.write("### 📊 Business Recommendation")

            if prediction == 1:
                
                if probability > 0.8:
                    st.error("🚨 Critical Risk: Immediate retention action required.")
                    st.write("Suggested actions:")
                    st.write("- Offer loyalty discount")
                    st.write("- Assign dedicated customer support")
                    st.write("- Offer contract upgrade incentives")

                elif probability > 0.5:
                    st.warning("⚠️ Medium Risk: Customer may churn.")
                    st.write("Suggested actions:")
                    st.write("- Provide promotional offers")
                    st.write("- Improve service support")
                    st.write("- Offer bundled services")

            else:
                st.success("✅ Customer appears stable.")
                st.write("Suggested actions:")
                st.write("- Maintain engagement")
                st.write("- Provide loyalty rewards")
                st.write("- Encourage long-term contract renewal")