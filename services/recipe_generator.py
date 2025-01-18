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
    "recipe_name": "str",
    "diet": "str",
    "continent": "str"("africa", "america", "asia", "australia", "europe", "oceania"),
    "language": "str",
    "ingredients": ["str"],
    "duration_to_cook": "int",
    "servings": "int",
    "instructions": ["str"],
    "difficulty": "str",
    "cuisine": "str",
    "description": "str",
    "meal_type": "str" ("breakfast", "lunch", "dinner", "dessert"),
    "image": "str" (La description de l'image doit obligatoirement être anglais),
    "nutrition_facts": {
        "calories": "int",
        "protein": "str",
        "carbohydrates": "str",
        "fat": "str",
        "vitamins" : "str",
        "minerals" : "str",
        "dietary_fiber": "str",
        "Sugar": "str",
        "Salt": "str",
        "antioxidants": "str"
    }
}
'''


def convert_to_json(text):
    text = text.replace("json", "").replace("```", "")
    return json.loads(text)


# Generate a recipe based on a description
def generate_recipe_by_description(data):
    prompt = f"""
    Analyse la saisie de l'utilisateur suivante : "{data['text']}" et retourne une réponse appropriée en {data['language']} :
    1. Si la saisie n'est pas liée à des ingrédients ou à un plat, renvoie la réponse suivante au format JSON :
    {{"message": str,"data": []}}.
    2. Si la saisie est pertinente et décrit des ingrédients ou un plat spécifique, renvoie une recette correspondante sous la forme d'un objet JSON :
    {{"message": str, "data": [{response_format}]}}.
    Note : La réponse doit être formulée dans la langue {data['language']} et ne doit être que du JSON pas un autre autre message en plus.
    """

    response = model.generate_content(prompt)
    return convert_to_json(response.text)


def generate_recipe_by_images(data):
    prompt = f"""
    Analyse les images suivantes et retourne les résultats sous forme de JSON :
    1. Si l'image ne contient pas de recettes ou d'éléments utilisables pour cuisiner, retourne : 
    {{"message": str, "data": []}}.
    2. Si l'image contient une ou plusieurs recettes, retourne les recettes sous forme (pas la même recette) de tableau JSON :
    [{response_format}].
    3. Si l'image contient des fruits, légumes ou céréales, retourne exemple de recette que l'on peut cuisiner avec ces ingrédients. La réponse doit être sous forme de tableau JSON :
    {{"message": str, "data": [{response_format}, {response_format}]}}.
    Note : Toutes les données doivent être fournies dans la langue suivante : {data['language']} et ne doit être que du JSON pas un autre autre message en plus.
    """

    # Convert the base64 string to image
    list_file = []
    for imageBase in data['images']:
        img_data = base64.b64decode(imageBase['base64'])
        image = Image.open(io.BytesIO(img_data))
        list_file.append(image)

    response = model.generate_content([prompt] + list_file)
    text = response.text
    return convert_to_json(text)