from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from services.recipe_generator import generate_recipe_by_description, generate_recipe_by_images
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get('api-key')
    if api_key != 'jkhui':
        return Response(content="Unauthorized", status_code=401)
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par une liste d'origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Description(BaseModel):
    text: str
    language: str = "en"


class Images(BaseModel):
    images: list
    language: str = "en"


@app.get("/")
def root():
    return {"message": "Welcome to the Recipe Generator API!"}


@app.post("/gen_witch_text/")
def recipe_by_description(description: Description):
    string_json = description.model_dump_json()
    try:
        return generate_recipe_by_description(json.loads(string_json))
    except Exception as e:
        print(f"Error: {e}")
   
    
@app.post("/gen_witch_image/")
def recipe_by_images(images: Images):
    string_json = images.model_dump_json()
    try:
        return generate_recipe_by_images(json.loads(string_json))
    except Exception as e:
        return (f"Erro: {e}")