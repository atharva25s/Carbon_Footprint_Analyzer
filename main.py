from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel
import joblib
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, Prediction, init_db

# Initialize DB (Ensure tables exist)
init_db()

# Load the trained model
model = joblib.load("regmodel.pkl")

# Initialize FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Input Schema
class PredictionInput(BaseModel):
    activity_code: int
    duration: float  # Duration in hours

# Home route Health checking
@app.get("/")
def home():
    return {"message": "Welcome to Carbon Footprint API"}

# Prediction route
@app.post("/predict")
def predict_carbon_footprint(data: PredictionInput, db: Session = Depends(get_db)):
    # Convert input to DataFrame
    input_df = pd.DataFrame([data.model_dump()])

    # Make prediction
    prediction = model.predict(input_df)[0]

    # Store prediction in database
    db_prediction = Prediction(
        user_id = 1001,
        activity_code=data.activity_code,
        duration=data.duration,
        carbon_footprint=prediction
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return {"predicted_carbon_footprint": prediction}

@app.get("/history")
def get_prediction_history(user_id: int = None, db: Session = Depends(get_db)):
    # If user_id is provided, filter by user_id
    if user_id:
        history = db.query(Prediction).filter(Prediction.user_id == user_id).all()
    else:
        history = db.query(Prediction).all()

    return [
        {
            "trip_id": pred.trip_id,
            "user_id": pred.user_id,
            "activity_code": pred.activity_code,
            "duration": pred.duration,
            "carbon_footprint": pred.carbon_footprint
        }
        for pred in history
    ]


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)