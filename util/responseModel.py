from typing import List
from models.itemModel import Item
from pydantic import BaseModel


class ResponseModel(BaseModel):
    data: List[Item]  
    message: str
