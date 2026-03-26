from fastapi import FastAPI
import numpy as np

app = FastAPI()

@app.get("/")
def home():
    dictt = {"pi": float(np.pi), "message":"wake up, daddy's home"}
    return dictt