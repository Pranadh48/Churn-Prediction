import pandas as pd
import pickle

def preprocess_input(df):

    # Load training columns
    model_columns = pickle.load(open("model/model_columns.pkl", "rb"))

    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    df = pd.get_dummies(df, drop_first=True)

    # Add missing columns
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0

    # Ensure same column order
    df = df[model_columns]

    return df