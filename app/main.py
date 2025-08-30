from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

# def decrypt_access_token(access_token: str):
#     try:
#         if not access_token:
#             raise HTTPException(status_code=401, detail="Missing token")
        


@app.get("/")
def index():
    return {"message": "Hello!"}

@app.get("/items/{item_id}")
def read_item(item_id: str) -> dict:
    return {"item_id": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name is ModelName.resnet:
        return {"model name": model_name, "message": "LeCNN all the images!"}
    
    return {"model name": model_name, "message": "Have some residuals."}