from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from typing import Optional , List
from models.itemModel import Item  
from util.responseModel import ResponseModel 
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI() 


client = MongoClient(os.getenv("MONODB_URI"))
db = client["demo"]
collection = db["users"]

class ResponseModel(BaseModel):
    data: List[Item]
    message: str

@app.get("/items", response_model=ResponseModel)
async def get_items():
    try:

        items = list(collection.find({}))  
        
        return {"data": items, "message": "Data retrieved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/items")
async def create_item(item: Item):
    result = collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

@app.put("/items/{item_id}")
async def update_item(item_id: str, updated_item: Item):
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item.dict()})
    return {"updated_count": result.modified_count}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    return {"deleted_count": result.deleted_count}


# @app.get("/hello")
# def hello_world():
#     return {"message": " Hello World "}

handler = Mangum(app)