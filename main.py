import random
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

items_db = []

@app.get("/")
def home():
    return {"message": "Welcome to the randomizer API"}

@app.get("/random/{max_value}")
def get_random_number(max_value: int):
    return {
        "max": max_value,
        "random_number": random.randint(1, max_value)
    }

@app.get("/random-beween")
def get_random_number_between(
        min_value: Annotated[int, Query(
            title="Minimum Value",
            description="The minimum randon number",
            ge=1,
            le=1000
        )] = 1,
        max_value: Annotated[int, Query(
            title="Maximum Value",
            description="The maximum randon number",
            ge=1,
            le=1000
        )] = 99
):
    if min_value > max_value:
        raise HTTPException(status_code=400, detail="min_value can't be greater than max_value")
    
    return {
        "min": min_value,
        "max": max_value,
        "random_number": random.randint(min_value, max_value),
    }

@app.post("/items")
def add_item(body: dict):
    item_name = body.get("name")

    if not item_name: 
        raise HTTPException(status_code=400, detail="'name' is required")
    
    if item_name in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    items_db.append(item_name)
    return {"message": "Item added successfully", "item": item_name}

@app.get("/items")
def get_randomized_items():
    randomized = items_db.copy()
    random.shuffle(randomized)
    return {
        "original_order": items_db,
        "randomized_order": randomized,
        "count": len(items_db)
    }

@app.put("/items/{update_item_name}")
def update_item(update_item_name: str, body: dict):
    if update_item_name not in items_db: 
        raise HTTPException(status_code=404, detail="Item not found")
    
    new_name = body.get("name")
    if not new_name:
        raise HTTPException(
            status_code=400,
            detail="'name' field is required in request body"
        )
    
    if new_name in items_db:
        raise HTTPException(
            status_code=409,
            detail="AN item with that name already exists"
        )
    
    index = items_db.index(update_item_name)
    items_db[index] = new_name

    return {
        "message": "Item updated successfully",
        "old_item": update_item_name,
        "new_item": new_name
    }

@app.delete("/items/{item}")
def delete_item(item: str):
    if item not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db.remove(item)

    return {
        "message": "Item deleted successfully",
        "deleted_item": item,
        "remaining_items_count": len(items_db)
    }




