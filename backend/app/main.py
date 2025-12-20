import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

model = joblib.load("C:/Users/Nitro/PycharmProjects/PythonProject/backend/model/best_knn_model.joblib")

app = FastAPI(title="KNN Prediction API")


class InputData(BaseModel):
    features: list

@app.get("/")
def home():
    return {"message": "Simple KNN API is running!"}

class PredictionRequest(BaseModel):
    features: List[float]

from fastapi import HTTPException


@app.post("/predict")
async def predict(request: PredictionRequest):
    from fastapi import HTTPException

    # Convert features to numbers with validation
    try:
        features = [float(x) for x in request.features]  # convert to numbers
    except:
        raise HTTPException(status_code=400, detail="Features must be numeric")

    # Convert to numpy array with correct shape
    arr = np.array(features).reshape(1, -1)

    # Model prediction with error handling
    try:
        pred = model.predict(arr)[0]  # Get single value
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    return {"prediction": float(pred)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}



