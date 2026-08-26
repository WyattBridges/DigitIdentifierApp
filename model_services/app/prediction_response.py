from typing import List
from pydantic import BaseModel, conlist

class PredictionResponse(BaseModel):
    values: List[float] = conlist(float, min_length = 10, max_length = 10)
