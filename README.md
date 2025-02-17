# Recipe Generator API

## Project Description

This project is an API that generates recipes and their corresponding images. It leverages several technologies:
- **FastAPI** for building the API.
- **Google Gemini Model** for generating recipe-related content.
- **Getimg.ai** API for generating images based on the recipe details. (https://getimg.ai/) to create your API KEY
- **Supabase** service to store and manage data.

The API exposes endpoints to generate recipes from text or images, upload images, and manage recipe and user data.

## Environment Variables

Create a `.env` file at the root of the project with the required keys:

```properties
MODEL_API_KEY=your_google_gemini_api_key
IMAGE_GEN_MODEL_KEY=your_getimg_ai_api_key
IMAGE_GEN_MODEL_URL=your_getimg_ai_url
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_api_key
API_KEY=your_custom_api_key
```

## How to Run

### Running in a Local Environment

1. Clone the repository and navigate to the project directory:

```bash
git clone <repository_url>
cd recipe_gen
```

2. Create and configure your `.env` file as described above.

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the FastAPI application using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```