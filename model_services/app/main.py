from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conint, conlist, field_validator
from typing import List, Annotated
import keras
import numpy as np
import os
from app.shape_inputs import *

dense_model_path = "app/models/dense_model.keras"
convolutional_model_path = "app/models/convolutional_model.keras"
dense_model = None
convolutional_model = None

# Function for loading deep-learning models from a path if the file exists
def load_if_exists(path):
    if os.path.exists(path):
        return keras.models.load_model(path)
    else:
        return None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Pixel = Annotated[int, conint(ge=0, le=255)]

class Image28x28(BaseModel):
    pixels: List[List[Pixel]]

    @field_validator("pixels")
    def check_shape(cls, v):
        if len(v) != 28:
            raise ValueError("Image must have 28 rows")
        for row in v:
            if len(row) != 28:
                raise ValueError("Each row must have 28 columns")
        return v

class PredictionResponse(BaseModel):
    values: List[float] = conlist(float, min_length = 10, max_length = 10)


# Main Application Endpoint
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Handwritten Digit Neural Network API</title>
        </head>
        <body>
            <h1>Welcome to the Handwritten Digit Neural Network API</h1>
            <p>This API provides access to neural networks for classifying handwritten digits.</p>
            <p>Check the /api/health endpoint for API status.</p>
            <p>Use /api/predict/dense to use a dense model for prediction.</p>
            <p>Use /api/predict/convolutional to use a convolutional model for prediction.</p>
            <p>When calling any prediction endpoint, use the following JSON structure:</p>
            <div>
                {
                    "pixels": [
                    [0, 0, 0, 255, ... 28 values],
                    ...
                    28 rows total
                    ]
                }
            </div>
            <p>All values should be integers with values between 0 and 255 (inclusive).</p>
            <p>Values will be returned as an array of 10 floating point numbers, representing the predicted probability for each digit in order.</p>
        </body>
    </html>
    """

# API Health Check Endpoint
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# API endpoint for prediction with a dense model
@app.post("/api/predict/dense", response_model=PredictionResponse)
def predict(image: Image28x28):
    global dense_model
    # Check if the dense model is available
    if dense_model is None:
        dense_model = load_if_exists(dense_model_path)

    # Convert to NumPy and reshape for processing
    array = np.array(image.pixels, dtype=np.float32)
    data = flatten_inputs(array)

    # Make a prediction
    model_out = dense_model.predict(data, verbose=0)
    return PredictionResponse(values = model_out.reshape(10).tolist())

# API endpoint for prediction with a dense model
@app.post("/api/predict/convolutional", response_model=PredictionResponse)
def predict(image: Image28x28):
    global convolutional_model
    # Check if the dense model is available
    if convolutional_model is None:
        convolutional_model = load_if_exists(convolutional_model_path)

    # Convert to NumPy and reshape for processing
    array = np.array(image.pixels, dtype=np.float32)
    data = inputs_as_square_32x32(array)

    # Make a prediction
    model_out = convolutional_model.predict(data, verbose=0)
    return PredictionResponse(values = model_out.reshape(10).tolist())
