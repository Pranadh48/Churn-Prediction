import pickle
import numpy as np

def predict_churn(input_data):

    model = pickle.load(open("model/churn_model.pkl", "rb"))
    scaler = pickle.load(open("model/scaler.pkl", "rb"))
    threshold = pickle.load(open("model/threshold.pkl", "rb"))

    input_scaled = scaler.transform(input_data)

    prob = model.predict_proba(input_scaled)[:,1]

    prediction = (prob > threshold).astype(int)

    return prediction, prob