import json
from datetime import datetime

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import config
from database.recipe_provider import RecipeProvider
from database.user_provider import UserProvider
from services.image_generator import text_to_image
from services.recipe_generator import generate_recipe_by_description, generate_recipe_by_images
from services.upload_url_image import save_image

app = FastAPI()

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get('api-key')
    if request.url.path == '/':
        return await call_next(request)
    
    if api_key != config.get('API_KEY'):
        return Response(content=json.dumps(
            {
            "code": "unauthorized",
            "message": "You are not authorized to access this service",
            "details": "Invalid API key"
        }
        ), status_code=401)
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

class ImageDescription(BaseModel):
    text: str


@app.get("/")
def root():
    return "Welcome to the Recipe Generator monorepo!, 😇 🥙"

@app.get("/server_info/")
def get_server_info(request: Request):
    server_info = {
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "server_timezone": datetime.now().astimezone().tzname(),
        "server_name": "Recipe Generator Server",
        "server_port": request.url.port,
    }
    return server_info


@app.post("/gen_witch_text/")
def recipe_by_description(description: Description):
    string_json = description.model_dump_json()
    try:
        return generate_recipe_by_description(json.loads(string_json))
    except Exception as e:
        return f"Error: {e}"
   
    
@app.post("/gen_witch_image/")
def recipe_by_images(images: Images):
    try:
        return generate_recipe_by_images(json.loads(images.model_dump_json()))
    except Exception as e:
        return f"Error: {e}"

class ImageUpload(BaseModel):
    url: str
@app.post("/upload_image_url/")
def upload_image_to_storage(image_upload: ImageUpload, res: Response):
    try:
        return save_image(url=image_upload.url, bucket="recipe-gen-images")
    except Exception as e:
        res.status_code = 500
        return {
            "status": "error",
            "message": f"Error: {e}",
        }


@app.post("/generate_image_text/")
def generate_image_text(image_description: ImageDescription, res: Response):
    try:
        return text_to_image(image_description.text)
    except Exception as e:
        res.status_code = 500
        return {
            "status": "error",
            "message": f"Error: {e}",
        }


# User data manager
class User(BaseModel):
    uid: str
    full_name: str
    created_at: datetime = datetime.now()
    photo_url: str
    status: bool = True
    email: str
    info_message: str = ""
    last_request: datetime = datetime.now()


@app.post("/user/")
def create_user(user: User, res: Response):
    try:
        user_data = json.loads(user.model_dump_json())
        response = UserProvider.save_user(user_data)
        return response
    except Exception as e:
        res.status_code = 500
        return {
            "status": "error",
            "message": f"Error: {e}",
        }

@app.get("/user/")
def get_user(uid: str, res: Response):
    try:
        response = UserProvider.get_user(uid)
        return response
    except Exception as e:
        res.status_code = 500
        return {
            "status": "error",
            "message": f"Error: {e}",
        }


# Recipe data manager
class Recipe(BaseModel):
    created_at: datetime = datetime.now()
    recipe_name: str
    created_by: str  # User create recipe
    ingredients: list[str]  # ingredients to compose recipe
    instructions: list[str]
    continent: str
    language: str
    duration_to_cook: int
    servings: int
    difficulty: str
    cuisine: str
    description: str
    meal_type: str
    nutrition_facts: dict  # No description
    image: str


@app.post("/recipe/")
def create_recipe(recipe: Recipe, res: Response):
    try:
        recipe_data = json.loads(recipe.model_dump_json())
        response = RecipeProvider.save_recipe(recipe_data)
        return response
    except Exception as e:
        res.status_code = 500
        return {
            "status": "error",
            "message": f"Error: {e}",
        }


@app.get("/recipe/")
def get_recipe(recipe_id: int, res: Response):
    try:
        response = RecipeProvider.find_by_id(recipe_id)
        return response
    except Exception as e:
        res.status_code = 500
        return {
            "status": "error",
            "message": f"Error: {e}",
        }


@app.get("/recipes/")
def get_all_recipes(offset: int, limit: int, res: Response):
    try:
        if (limit - offset) > 10:
            limit = offset + 10

        response = RecipeProvider.find_all(offset, limit)
        return response
    except Exception as e:
        res.status_code = 500
        return {
            "status": "error",
            "message": f"Error: {e}",
        }