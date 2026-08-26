from typing import List, Annotated
from pydantic import BaseModel, conint, field_validator

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
