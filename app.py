from fastapi import FastAPI, Query, HTTPException
import numpy as np
from product import process_data

app = FastAPI()

@app.get("/")
def home():
    dictt = {"pi": float(np.pi), "message":"wake up, daddy's home"}
    return dictt

@app.get("/product/{id}")
def products(id):
    whole_list = process_data()
    for dickt in whole_list:
        if id == dickt["id"]:
            return dickt

@app.get("/products")
def product_query(name:str = Query(default=None, 
  min_length=1,
  max_length=50,
  description="Search By Product Name"),
  price_min:float = Query(
      default=None, 
      min_length=1,
      max_length=8,
      description="Provide the MINIMUM price of the product that you want to see"
  ),
  price_max:float = Query(
      default=None,
      min_length=1,
      max_length=8,
      description="Provide the MAXIMUM price of the product that you want to see"
  )
  ) -> dict:

    whole_list = process_data()
    if name:
        name_mod:str = name.strip().lower()
        matches:list[dict] = [m for m in whole_list if name_mod in m["name"].lower()]
        if not matches:
            raise HTTPException(status_code=404,detail=f"No matches found for your search, '{name}'")
    
        to_return_name = {
            "total":len(matches), "items":matches
        }
    
    if price_min:
        matches = [m for m in whole_list if m["price"] >= price_min]
        if not matches:
            raise HTTPException(status_code=404,detail=f"No matches found for your search, 'Minimum price = {price_min}'")
        to_return_price_min = {
            "total":len(matches), "items":matches
        }
    if price_max:
        matches = [m for m in whole_list if m["price"] <= price_min]
        if not matches:
            raise HTTPException(status_code=404,detail=f"No matches found for your search, 'Maximum price = {price_max}'")
        to_return_price_max = {
            "total":len(matches), "items":matches
        }

    else: 
        return {"total":len(whole_list),"items":whole_list}