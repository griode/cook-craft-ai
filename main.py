from fastapi import FastAPI, Request
from pydantic import BaseModel
from services.recipe_generator import generate_recipe_by_description, generate_recipe_by_images
from utils.request_header_manager import handle_options_request, handle_post_request, handle_invalid_method
import json


app = FastAPI()


class Description(BaseModel):
    text: str
    language: str = "en"


class Images(BaseModel):
    images: list[str]
    language: str = "en"


@app.get("/")
async def root():
    return {"message": "Welcome to the Recipe Generator API!"}


@app.post("/gen_witch_text/")
async def recipe_by_description(description: Description, req: Request):
    if req.method == 'OPTIONS':
        return handle_options_request()
    elif req.method == "POST":
        string_json = description.model_dump_json()
        return handle_post_request(json.loads(string_json), generate_recipe_by_description)
    else:
        return handle_invalid_method()
    

@app.post("/gen_witch_image")
async def recipe_by_images(images: Images, req: Request):
    if req.method == 'OPTIONS':
        return handle_options_request()
    elif req.method == "POST":
        string_json = images.model_dump_json()
        return handle_post_request(json.loads(string_json), generate_recipe_by_images)
    else:
        return handle_invalid_method()