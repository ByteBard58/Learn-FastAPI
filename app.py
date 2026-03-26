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
  description="Search By Product Name")) -> dict:

    whole_list = process_data()
    if name:
        name_mod:str = name.strip().lower()
        matches:list[dict] = [m for m in whole_list if name_mod in m["name"].lower()]
        if not matches:
            raise HTTPException(status_code=404,detail=f"No matches found for your search, '{name}'")
    
        return {
            "total":len(matches), "items":matches
        }
    else: 
        return {"total":len(whole_list),"items":whole_list}