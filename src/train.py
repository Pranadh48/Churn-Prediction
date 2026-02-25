import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def train_model():

    # Load data
    df = pd.read_csv("data/Customer_Churn_Dataset.csv")

    # Preprocessing
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna()
    df = df.drop(columns=['customerID'])
    df['Churn'] = df['Churn'].map({'Yes':1,'No':0})

    X = df.drop('Churn', axis=1)
    y = df['Churn']

    X = pd.get_dummies(X, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    model = LogisticRegression(
        class_weight='balanced',
        max_iter=1000
    )

    model.fit(X_train, y_train)

    # Save artifacts
    pickle.dump(model, open("model/churn_model.pkl", "wb"))
    pickle.dump(scaler, open("model/scaler.pkl", "wb"))
    pickle.dump(0.4, open("model/threshold.pkl", "wb"))

    print("Model trained and saved successfully!")

if __name__ == "__main__":
    train_model()