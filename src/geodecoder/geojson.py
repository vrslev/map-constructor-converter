from typing import Literal

from pydantic import BaseModel, Field


class Point(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[str, str]


Geometry = Point


class Properties(BaseModel):
    description: str
    iconCaption: str
    marker_color: str = Field(..., alias="marker-color")

    class Config:
        allow_population_by_field_name = True


class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    id: int
    geometry: Geometry
    properties: Properties


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Feature]
