import base64
import io
import json

import google.generativeai as genai
from PIL import Image  # Pillow library for image manipulation

from config import config

# Configuration of the Gemini model
genai.configure(api_key=config.get("model_api_key"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")
# format of the response from the model
response_format = '''
{
    "recipe_name": "string",
    "diet": "string",
    "continent": "string"("africa", "america", "asia", "australia", "europe", "oceania"),
    "language": "string",
    "ingredients": ["string"],
    "duration_to_cook": "int",
    "servings": "int",
    "instructions": ["string"],
    "difficulty": "string",
    "cuisine": "string",
    "description": "string",
    "meal_type": "string" ("breakfast", "lunch", "dinner", "dessert"),
    "image": "string" (The description of the image must be in English),
    "nutrition_facts": {
        "calories": "string",
        "protein": "string",
        "carbohydrates": "string",
        "fat": "string",
        "vitamins" : "string",
        "minerals" : "string",
        "dietary_fiber": "string",
        "Sugar": "string",
        "Salt": "string",
        "antioxidants": "string"
    }
}
'''


def convert_to_json(text):
    text = text.replace("json", "").replace("```", "")
    return json.loads(text)


# Generate a recipe based on a description
def generate_recipe_by_description(data):
    prompt = f"""
    Analyze the following user input: "{data['text']}" and return an appropriate response in {data['language']}:
    1. If the input is not related to ingredients or a dish, return the following response in JSON format:
    {{"message": str, "data": []}}.
    2. If the input is relevant and describes specific ingredients or a dish, return a corresponding recipe in the form of a JSON object:
    {{"message": str, "data": [{response_format}]}}.
    Note: The response must be formulated in the language {data['language']} and should be only JSON, not any other message.
    """

    response = model.generate_content(prompt)
    return convert_to_json(response.text)


def generate_recipe_by_images(data):
    prompt = f"""
    Analyze the following images and return the results in JSON format:
    1. If the image does not contain recipes or elements usable for cooking, return:
    {{"message": str, "data": []}}.
    2. If the image contains one or more recipes, return the recipes in the form of a JSON array (not the same recipe):
    [{response_format}].
    3. If the image contains fruits, vegetables, or grains, return an example recipe that can be cooked with these ingredients. The response should be in the form of a JSON array:
    {{"message": str, "data": [{response_format}, {response_format}]}}.
    Note: All data must be provided in the following language: {data['language']} and should be only JSON, not any other message.
    """

    # Convert the base64 string to image
    list_file = []
    for imageBase in data['images']:
        img_data = base64.b64decode(imageBase['base64'])
        image = Image.open(io.BytesIO(img_data))
        list_file.append(image)

    response = model.generate_content([prompt] + list_file)
    return convert_to_json(response.text)