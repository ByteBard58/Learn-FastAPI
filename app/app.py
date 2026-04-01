from fastapi import FastAPI, Query, HTTPException,Path, Depends
import numpy as np
from Data.product import process_data, add_data, delete_data, update_data as ud_p
from .schema.product_rule import Item, Item_put
from uuid import UUID, uuid4

app = FastAPI()

@app.get("/",response_model=dict)
def home():
    dictt = {"pi": float(np.pi), "message":"wake up, daddy's home"}
    return dictt

@app.get("/product/{id}",response_model=list[dict])
def products(
    id:UUID = Path(
        description="UUID of the product",
        examples="0005a4ea-ce3f-4dd7-bee0-f4ccc70fea6a"
    ), dep = Depends(process_data)
) -> list[dict]:
    whole_list = dep
    dickt:list[dict] = [r for r in whole_list if r["id"] == str(id)]
    if not dickt:
        raise HTTPException(status_code=404, detail=f"Product of id = {str(id)} not found")
    else:
        return dickt

@app.get("/product",response_model=dict)
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
  ), dep = Depends(process_data)
  ) -> dict:

    results = dep
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

@app.post("/product",status_code=201,response_model=dict)
def create_product(product:Item) -> dict:
    product = product.model_dump(mode="json")
    try:
        add_data(product)
        return {
            "message":"product added successfully",
            "product":product
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/product/{sku}",response_model=dict)
def remove_product(sku:str = Path(
    ..., max_length= 14, min_length=12, 
    pattern=r"^[A-Z]+-\d+GB-\d+$",
    description="SKU (stock keeping unit) of the product",
    examples=["HP-156GB-100","SONY-374GB-087","XIAO-359GB-991"]
)) -> dict:
    try:
        to_r = delete_data(sku)
        return to_r
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@app.put("/product/{id}", response_model=dict)
def update_data(value:Item_put, id:UUID = Path(
    ..., description="UUID of the product (required)"
), dep = Depends(process_data)) -> dict:
    whole_list = dep
    existing = [w for w in whole_list if w["id"] == str(id)]
    if not existing:
        raise HTTPException(status_code=404,
            detail=f"Unable to find id = {id} in the database. Update unsuccessful.")
    existing = Item.model_validate(existing[0])
    incoming_update = value.model_dump(exclude_unset=True, mode="json")
    updated_item = existing.model_copy(update=incoming_update)
    try:
        msg:dict = ud_p(id=id,value=updated_item.model_dump(mode="json"))
        return msg 
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))