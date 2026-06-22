import os
import xgboost as xgb
import pandas as pd
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from app.schemas import PricingRequest, PricingResponse
from prometheus_client import Histogram

app = FastAPI(title="Dynamic Pricing Engine API")

# Custom Prometheus metric for model predictions
PREDICTED_PRICE = Histogram(
    "predicted_price",
    "Histogram of predicted prices",
    buckets=[10, 15, 20, 25, 30, 40, 50, 75, 100]
)

# Load model
MODEL_PATH = os.getenv("MODEL_PATH", "model/xgboost_pricing_model.json")
model = None

@app.on_event("startup")
async def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = xgb.XGBRegressor()
        model.load_model(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    else:
        print(f"Warning: Model not found at {MODEL_PATH}")

Instrumentator().instrument(app).expose(app)

@app.post("/predict", response_model=PricingResponse)
async def predict_price(request: PricingRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    
    # Create feature dataframe
    features = pd.DataFrame([{
        "time_of_day": request.time_of_day,
        "weather_condition": request.weather_condition,
        "demand_multiplier": request.demand_multiplier,
        "base_price": request.base_price
    }])
    
    try:
        prediction = model.predict(features)[0]
        # Ensure price doesn't go below base price (business logic)
        final_price = max(request.base_price, float(prediction))
        
        # Observe the metric
        PREDICTED_PRICE.observe(final_price)
        
        return PricingResponse(optimal_price=round(final_price, 2), version="1.0.0")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
