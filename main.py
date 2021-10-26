import fastapi
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
#@app.get("/")
#def home():
    #return {"Data": "Testing"}
#@app.get("/about")
#def about():
    #return {"Data": "About"}

class Item(BaseModel):
    name: str
    price: float
    type: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    type: Optional[str] = None

inventory = {}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description='The ID of the item your looking for', gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item does not exist.")
    return inventory[item_id]

@app.get("/get-by-name/")
def get_item(name: str = Query(None, title="Name", descritption="Name of item", max_length=10, min_length=2)):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item does not exist.")

@app.post("/create=item/{item_id")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists.")

    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.type != None:
        inventory[item_id].type = item.type

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID for item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

    del inventory[item_id]
    return{"Success":"Item deleted!"}




