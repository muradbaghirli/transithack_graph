from pydantic import BaseModel, Field
from typing import Annotated


Latitude = Annotated[float, Field(40.37636612143278, ge=-90, le=90, description="Latitude value")]
Longitude = Annotated[float, Field(49.83615036825379, ge=-180, le=180, description="Longitude value")]

class CoordinateModel(BaseModel):
    lat: Latitude
    long: Longitude


class RouteModel(BaseModel):
    begin: CoordinateModel = Field(..., description="The beginning of the route")
    dest: CoordinateModel = Field(..., description="The destination of the route")


