from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conint, conlist, field_validator
from typing import List, Annotated
import os

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
        </body>
    </html>
    """

# API Health Check Endpoint
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

