from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load artifacts
model = pickle.load(open("model/churn_model.pkl", "rb"))
scaler = pickle.load(open("model/scaler.pkl", "rb"))
threshold = pickle.load(open("model/threshold.pkl", "rb"))
model_columns = pickle.load(open("model/model_columns.pkl", "rb"))

def preprocess_input(data):
    df = pd.DataFrame([data])

    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    df = pd.get_dummies(df, drop_first=True)

    # Add missing columns
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[model_columns]

    return df

@app.route("/")
def home():
    return "Customer Churn Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    df_processed = preprocess_input(data)

    df_scaled = scaler.transform(df_processed)

    prob = model.predict_proba(df_scaled)[:,1][0]
    prediction = int(prob > threshold)

    return jsonify({
        "churn_probability": round(float(prob), 3),
        "churn_prediction": prediction
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)