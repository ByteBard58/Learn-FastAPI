import json
from pathlib import Path
from typing import List
import os

TARGET = Path("Data","dummy.json")

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

def main() -> None:
  process_data()

if __name__=="__main__":
  main()