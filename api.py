from fastapi import FastAPI, Query
import json

application = FastAPI()

# Load JSON data
with open("data.json", "r") as file:
    data = json.load(file)

@application.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@application.get("/data")
def get_data(key: str = Query(None, description="Filter by a key")):
    """Returns the filtered JSON data if key is provided"""
    if key:
        return {key: data.get(key, "Key not found")}
    return data