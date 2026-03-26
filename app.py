from fastapi import FastAPI
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
