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

    whole_list = process_data()
    to_return = []
    if name:
        name_mod:str = name.strip().lower()
        matches_1:list[dict] = [m for m in whole_list if name_mod in m["name"].lower()]
        if not matches_1:
            raise HTTPException(status_code=404,detail=f"No matches found for your search, '{name}'")
        to_return.extend(matches_1)
    
    if price_min:
        if to_return:
            matches_2:list[dict] = [m for m in to_return if m["price"] >= price_min]
            if not matches_2:
                raise HTTPException(status_code=404, detail=f"No matches found for your search, 'Minimum price = {price_min}' and 'Name = {name}'")
            to_return = [x for x in to_return if x in matches_2]
        else:
            matches_2:list[dict] = [m for m in whole_list if m["price"] >= price_min]
            if not matches_2:
                raise HTTPException(status_code=404,detail=f"No matches found for your search, 'Minimum price = {price_min}'")
            to_return.extend(matches_2)

    if price_max:
        if to_return:
            matches_3:list[dict] = [m for m in to_return if m["price"] <= price_max]
            if not matches_3:
                raise HTTPException(status_code=404, detail=f"No matches found for your search, 'Minimum price = {price_min}', 'Maximum price = {price_max}' and 'Name = {name}'")
            to_return = [x for x in to_return if x in matches_3]
        else:
            matches_3:list[dict] = [m for m in whole_list if m["price"] <= price_max]
            if not matches_3:
                raise HTTPException(status_code=404,detail=f"No matches found for your search, 'Maximum price = {price_max}'")
            to_return.extend(matches_3)

    if to_return:
        return {"total":len(to_return),"items":to_return}
    else: 
        return {"total":len(whole_list),"items":whole_list}