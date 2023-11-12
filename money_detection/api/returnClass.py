from pydantic import BaseModel

# Coordenadas dos pontos de uma bounding box
class Point(BaseModel):
    x: int
    y: int

# Coordenadas de uma bounding box
class BoundingBoxCoordinate(BaseModel):
    top_left: Point
    bottom_right: Point

# Item retornado pela API
class Item(BaseModel):
    bb_coordinates: BoundingBoxCoordinate
    label: str
    prediction: str