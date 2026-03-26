import json
from pathlib import Path
import os

TARGET = Path("Data","products.json")

def process_data(target = TARGET) -> list[dict]:
  if not os.path.exists(TARGET):
    return []
  with open(TARGET,"r",encoding="utf-8") as file:
    return json.load(file)

def main() -> None:
  process_data()

if __name__=="__main__":
  main()