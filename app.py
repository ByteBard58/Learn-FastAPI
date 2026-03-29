from fastapi import FastAPI, Query, HTTPException,Path
import numpy as np
from product import process_data
from schema.product_rule import Item
from uuid import UUID

app = FastAPI()

@app.get("/")
def home():
    dictt = {"pi": float(np.pi), "message":"wake up, daddy's home"}
    return dictt

@app.get("/product/{id}")
def products(
    id:UUID = Path(
        description="UUID of the product",
        examples="0005a4ea-ce3f-4dd7-bee0-f4ccc70fea6a"
    )
):
    whole_list = process_data()
    dickt:list[dict] = [r for r in whole_list if r["id"] == str(id)]
    if not dickt:
        raise HTTPException(status_code=404, detail=f"Product of id = {str(id)} not found")
    else:
        return dickt

@app.get("/product")
def product_query(
  name:str = Query(default=None, 
       min_length=1,
       max_length=50,
       description="Search By Product Name"),
  price_min:float = Query(
      default=None, 
      description="Provide the MINIMUM price of the product that you want to see",
  ),
  price_max:float = Query(
      default=None,
      description="Provide the MAXIMUM price of the product that you want to see"
  ),
  sort:bool = Query(
      default=True,
      description="Sort the items according to price"
  ),
  order:int = Query(
      default=0,
      ge=0,
      le=1,
      description="0 for ascending, 1 for descending"
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
    if sort:
        if order not in [0,1]:
            raise HTTPException(status_code=422,detail=f"Only 0(ascending) and 1(descending) are accepted as order, got {order}")
        else:
            reverse = True if order == 1 else False
            results = sorted(results,key=lambda x: x.get("price"),reverse=reverse)
            return {"total":len(results),"items":results}
    
    return {"total":len(results),"items":results}

@app.post("/product",status_code=201)
def create_product(product:Item):
    return product