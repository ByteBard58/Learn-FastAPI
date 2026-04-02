import json
from pathlib import Path
from typing import List
from uuid import UUID
import os

TARGET = Path("Data","products.json")

def process_data(target = TARGET) -> List[dict]:
  if not os.path.exists(TARGET):
    return []
  else:
    with open(target,"r",encoding="utf-8") as file:
      return json.load(file)

def save_data(value:List[dict], target = TARGET) -> None:
  with open(target,"w",encoding="utf-8",) as f:
    json.dump(value,f,ensure_ascii=False,indent=2)

def add_data(value:dict) -> List[dict]:
  output = process_data()
  if any(p["sku"] == value["sku"] for p in output):
    raise ValueError(f"SKU={value["sku"]} already exists")
  output.append(value)
  save_data(output)
  return output

def delete_data(sku:str) -> dict:
  whole_list = process_data()
  target:list[dict] = [t for t in whole_list if str(t["sku"]) == sku]
  if not target:
    raise ValueError(f"Unable to find SKU = {sku} in the database. Deletion Unsuccessful.")
  whole_list = [r for r in whole_list if r not in target]
  save_data(whole_list)

  return {"message":"Deletion successful", "item_deleted":target}

def delete_data_by_dict(value:dict,prev_list:list[dict] = process_data()) -> None:
  prev_list = [p for p in prev_list if not p == value]
  save_data(prev_list)

def update_data(id:UUID,value:dict) -> dict:
  whole_list = process_data()
  target:list[dict] = [r for r in whole_list if r["id"] == str(id)]
  if not target:
    raise ValueError(f"Unable to find id = {id} in the database. Update unsuccessful.")
  target:dict = target[0]
  delete_data_by_dict(target,whole_list)

  add_data(value)
  return {"message":"Update successful", "item_updated_before":target,
          "item_updated_after":value}

def main() -> None:
  process_data()

if __name__=="__main__":
  main()