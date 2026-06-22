import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os

def train_model(data_file="data/historical_data.csv", model_output="model/xgboost_pricing_model.json"):
    if not os.path.exists(data_file):
        print(f"Data file {data_file} not found. Please run generate_data.py first.")
        return

    print(f"Loading data from {data_file}...")
    df = pd.read_csv(data_file)

    X = df[["time_of_day", "weather_condition", "demand_multiplier", "base_price"]]
    y = df["optimal_price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    print("Evaluating model...")
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    print(f"MSE: {mse:.4f}")
    print(f"MAE: {mae:.4f}")

    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    model.save_model(model_output)
    print(f"Model saved to {model_output}")

if __name__ == "__main__":
    train_model()
