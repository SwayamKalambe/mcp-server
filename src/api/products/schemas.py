from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

'''REQUESTS'''

class CreateProductRequest(BaseModel):
    product_name: str
    price: int
    description: str
    quantity : int = Field(gt=0)

'''RESPONSE'''

class ProductResponse(BaseModel):
    product_id: UUID
    product_name: str
    price: int
    description: str
    quantity: int


model_config = ConfigDict(from_attributes=True)