import os

config = {
    "model_api_key": os.getenv("MODEL_API_KEY"),
    "image_gen_model_key": os.getenv("IMAGE_GEN_MODEL_KEY"),
    "image_gen_model_url": os.getenv("IMAGE_GEN_MODEL_URL"),
}