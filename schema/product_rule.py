from pydantic import (BaseModel, Field, AnyUrl, 
        model_validator, field_validator, computed_field, EmailStr)
from typing import Annotated, Literal, List, Optional
from datetime import datetime, timezone
from uuid import UUID

class seller(BaseModel):
   seller_id: UUID
   name : Annotated[str,Field(
      ..., min_length=3,max_length=25,
      description="Name of the seller (required)", examples=["Asus Exclusive","Lenovo Store"]
   )]
   email : Annotated[EmailStr,Field(
      ..., description="Email address of the seller (required)"
   )]
   website : Annotated[AnyUrl,Field(
      ..., description="Website URL of the seller (required)"
   )]

class dimensions_cm(BaseModel):
  length : Annotated[float,Field(
     ..., description="Length of the product in cm unit (required)",
     gt=0
  )]
  width : Annotated[float,Field(
     ..., description="Width of the product in cm unit (required)",
     gt=0
  )]
  height : Annotated[float,Field(
     ..., description="Height of the product in cm unit (required)",
     gt=0
  )]

  @computed_field(return_type=float)
  @property
  def volume(self):
     volume = self.length * self.width * self.height
     return round(volume,2)

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
    max_length=10, 
    examples=[["gaming","chocolate"],["drinks","clothes"]]
  )] = None
  image_urls : Annotated[List[AnyUrl],Field(
    ..., min_length=1,
    description="URLs of images of the product (required)"
  )]
  dimensions_cm : dimensions_cm
  seller : seller
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  @field_validator("sku",mode="after")
  @classmethod
  def validate_sku(cls,value:str) -> str:
      last = str(value).strip().split("-")[-1]
      if not (len(last) == 3 and last.isdigit()):
        raise ValueError(f"SKU must end with a 3-digit sequence, like `-239`, got `-{last}` instead")
      return value
  
  @model_validator(mode="after")
  def validate_stock_is_active(self) -> "Item":
    if self.is_active and self.stock == 0:
        raise ValueError("`is_active` must be `False` when `stock` is 0, got `True` instead")
    return self
  
  @computed_field(return_type=float)
  @property
  def final_price(self):
    fp = self.price - (self.price * (self.discount_percent/100))
    return round(fp,2)
  
