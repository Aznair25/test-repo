from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
app=FastAPI()
FILE="data.json"
class Item(BaseModel):
    name: Optional[str]=None
    id: Optional[int]=None
    email: Optional[str]=None
    age: Optional[int]=None
    skills: Optional[List[str]]=None
data={
    "name":"Aznair Manzoor",
    "id":25,
    "email":"aznairmanzoor1@gmail.com",
    "age":22,
    "skills":["ML","AI","Python"],
}

with open(FILE,"w") as json_file:
    json.dump([data],json_file, indent=4)

def read_data():
    try:
        with open(FILE,"r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []
def write_data(data):
    with open(FILE,"w") as json_file:
        return json.dump(data,json_file, indent=4)
@app.get("/items/",response_model=list[Item])
def get_items():
    return read_data()
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id:int):
    items= read_data()
    item=next((item for item in items if item["id"]==item_id),None)
    if item is None:
        raise HTTPException(status_code=404,detail="item not found")
    return item
@app.post("/create-item",response_model= Item)
def create_item(item:Item):
    items=read_data()
    items.append(item.model_dump())
    write_data(items)
    return item
@app.put("/update-item/{item_id}",response_model=Item)
def update_item(item_id:int, update_item:Item):
    items=read_data()
    item_index=next((index for index, item in enumerate(items) if item["id"]==item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404,detail="item not found")
    items[item_index]= update_item.model_dump()
    write_data(items)
    return update_item
@app.delete("/delete-item/{item_id}")
def delete_item(item_id:int):
    items=read_data()
    item_index = next((index for index, item in enumerate(items) if item["id"] == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="item not found")
    deleted_item=items.pop(item_index)

    write_data(items)
    return {"message":"item deleted","item":deleted_item}
@app.patch("/part_update/{item_id}",response_model=Item)
def partially_update(item_id:int, part_update:Item):
    items=read_data()
    item_index=next((index for index, item in enumerate(items) if item["id"]==item_id),None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="item not found")
    existing_item=items[item_index]
    updated_data = {**existing_item, **{k: v for k, v in part_update.model_dump().items() if v is not None}}
    items[item_index] = updated_data
    write_data(items)
    return updated_data