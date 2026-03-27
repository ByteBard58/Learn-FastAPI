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

@app.get("/product")
def product_query(
  name:str = Query(default=None, 
       min_length=1,
       max_length=50,
       description="Search By Product Name"),
  price_min:float = Query(
      default=None, 
      description="Provide the MINIMUM price of the product that you want to see"
  ),
  price_max:float = Query(
      default=None,
      description="Provide the MAXIMUM price of the product that you want to see"
  )
  ) -> dict:

    results = process_data()
    if name is not None:
        name_mod:str = name.strip().lower()
        results = [r for r in results if name_mod in r["name"].lower()]
    if price_min is not None:
        results = [r for r in results if r["price"] >= price_min]
    if price_max is not None:
        results = [r for r in results if r["price"] <= price_max]

    if not results :
        raise HTTPException(status_code=404, detail="No item found")
    
    return {"total":len(results),"items":results}