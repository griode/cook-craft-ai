from datetime import datetime
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from database.user_provider import UserProvider
from services.image_generator import text_to_image
from services.recipe_generator import generate_recipe_by_description, generate_recipe_by_images
import json
from fastapi.middleware.cors import CORSMiddleware
from services.upload_file import upload_image

app = FastAPI()

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get('api-key')
    if api_key != 'jkhui':
        return Response(content="Unauthorized", status_code=401)
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

class User(BaseModel):
    iud: str
    full_name: str
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    birth_day: str = datetime.now().strftime("%Y-%m-%d")
    photo_url: str
    status: bool
    email: str
    info_message: str

class ImageDescription(BaseModel):
    text: str

class ImageUpload(BaseModel):
    image: str
    bucket_name: str


@app.get("/")
def root():
    return {"message": "Welcome to the Recipe Generator API!"}


@app.post("/gen_witch_text/")
def recipe_by_description(description: Description):
    string_json = description.model_dump_json()
    try:
        return generate_recipe_by_description(json.loads(string_json))
    except Exception as e:
        return f"Error: {e}"
   
    
@app.post("/gen_witch_image/")
def recipe_by_images(images: Images):
    string_json = images.model_dump_json()
    try:
        return generate_recipe_by_images(json.loads(string_json))
    except Exception as e:
        return f"Error: {e}"


@app.post("/upload_image/")
def upload_image_to_storage(image_upload: ImageUpload, res: Response):
    try:
        return upload_image(image_upload.image, image_upload.bucket_name)
    except Exception as e:
        res.status_code = 500
        return f"Error: {e}"


@app.post("/generate_image_text/")
def generate_image_text(image_description: ImageDescription, res: Response):
    try:
        return text_to_image(image_description.text)
    except Exception as e:
        res.status_code = 500
        return f"Error: {e}"


# User data manager
@app.post("/user/")
def create_user(user: User, res: Response):
    try:
        user_data = json.loads(user.model_dump_json())
        response = UserProvider.save_user(user_data)
        return response
    except Exception as e:
        res.status_code = 500
        return f"Error: {e}"

@app.get("/user/")
def get_user(uid: str, res: Response):
    try:
        response = UserProvider.get_user(uid)
        return response
    except Exception as e:
        res.status_code = 500
        return f"Error: {e}"