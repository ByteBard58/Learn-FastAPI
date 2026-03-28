from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated, Literal, List, Optional
from datetime import datetime, timezone
from uuid import UUID

class Item(BaseModel):
  id : UUID
  sku : Annotated[str,Field(...,
    min_length= 4, max_length= 30,
    description= "Stock Keeping Unit (required)",
    examples=["XIAO-359GB-001","REAL-84GB-004"]
  )]
  name : Annotated[str, Field(...,
    min_length=3, max_length=40, 
    description="Name of the product (required)",
    examples=["Xiaomi Model Pro","Realme Model X"]
  )]
  description: Annotated[Optional[str],Field(
    min_length=5, max_length=100, 
    description="Description of the product (optional)"
  )] = None
  category: Annotated[str, Field(...,
    min_length=3, max_length=14, 
    description="Category of the product (required)",
    examples=["mobiles","laptops"]
  )]
  brand : Annotated[str,Field(
    ..., min_length=3, max_length=12, 
    description="Brand of the product (required)",
    examples=["Lenovo","Apple"]
  )]
  price : Annotated[float,Field(
    ..., gt=0, 
    description="Price of the product (required)",
    examples=[579.5,9999.0,374.5,34999.0]
  )]
  currency : Literal["INR"] = "INR"
  discount_percent : Annotated[float,Field(
    ge = 0, le = 100,
    description="Percentage of discount"
  )] = 0.00
  stock : Annotated[int,Field(
    ..., ge = 0,
    description="Amount of products in stock (required)", 
    examples=[123,10,23]
  )]
  is_active : Annotated[bool,Field(
    description="Activation Status in boolean (required)"
  )] = True
  rating : Annotated[Optional[float],Field(
    ge = 0, le = 5,
    description="Rating of the product (optional)"
  )] = None
  tags : Annotated[Optional[List[str]],Field(
    description="Tags assigned to the product (optional)",
    max_items=10, 
    examples=[["gaming","chocolate"],["drinks","clothes"]]
  )] = None
  image_urls : Annotated[List[AnyUrl],Field(
    ..., min_length=1,
    description="URLs of images of the product (required)"
  )]
  # dimensions_cm
  # seller
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
