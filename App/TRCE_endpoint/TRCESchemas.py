from pydantic import BaseModel, Field

class TRCERequest(BaseModel):
    location_slug: str = Field(min_length=1, max_length=100)
    cart_value: int = Field(gt=0)
    user_lon: float = Field(gt=-181, lt=181)
    user_lat: float = Field(gt=-91, lt=91)