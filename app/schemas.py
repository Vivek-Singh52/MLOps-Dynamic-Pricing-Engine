from pydantic import BaseModel, Field

class PricingRequest(BaseModel):
    time_of_day: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    weather_condition: int = Field(..., ge=0, le=2, description="0: Clear, 1: Rain, 2: Snow")
    demand_multiplier: float = Field(..., ge=0.5, le=3.0, description="Current demand multiplier")
    base_price: float = Field(..., ge=5.0, description="Base price for the ride")

class PricingResponse(BaseModel):
    optimal_price: float
    version: str
