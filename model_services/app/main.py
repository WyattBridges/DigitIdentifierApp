from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import json
import numpy as np

from app.image_28x28 import Image28x28
from app.prediction_response import PredictionResponse
from app.shape_inputs import *
from app.available_model import AvailableModel

model_registry_path = 'app/available_models.json'

@asynccontextmanager
async def loadModels(app: FastAPI):
    app.state.data = {}
    try:
        # attempt to load each model from the available models file
        j = None
        with open(model_registry_path) as f:
            j = json.load(f)
        for listing in j["models"]:
            name = listing["name"]
            extension = listing["endpoint_extension"]
            model_path = listing["model_path"]
            shaping_function = listing["input_shaping"]
            description = listing["description"] if listing["description"] else ""
            diagram_path = listing["diagram_path"] if listing["diagram_path"] else ""
            model = AvailableModel(name, extension, model_path, shaping_function, description, diagram_path)
            app.state.data[extension] = model

    except Exception as e:
        print(e)
        return
    
    yield

    # clear before ending
    app.state.data.clear()

app = FastAPI(lifespan=loadModels)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
            <p>Use /api/available_models to view which models are available.</p>
            <p>This endpoint will return a list of models in the following format:</p>
            <div>
            {
                "models": [
                    {
                        "Name": ...,
                        "Description": ...,
                        "Endpoint Extension": ...
                    }, ...
                ]
            }
            </div>
            <p>Send a POST request to /api/predict/{extension} to receive a prediction from the desired model.</p>
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

# API endpoint for acquiring information on available models
@app.get("/api/available_models")
def getAvailableModels():
    arr = []
    for model in app.state.data.values():
        arr.append(model.get_client_API_info())
    return JSONResponse(content={"models": arr})

# API endpoint for prediction with a dense model
@app.post("/api/predict/{extension}", response_model=PredictionResponse)
def predict(extension: str, image: Image28x28):
    if extension not in app.state.data:
        return PredictionResponse(values = [0] * 10)
    
    array = np.array(image.pixels, dtype=np.float32)
    model_out = app.state.data[extension].make_prediction(array)
    return PredictionResponse(values = model_out.reshape(10).tolist())
