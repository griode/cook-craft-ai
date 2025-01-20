from config import supabase_client


class RecipeProvider:
    recipe_table = supabase_client.table("recipes")

    @staticmethod
    def save_recipe(recipe: dict) :
        response = RecipeProvider.recipe_table.insert(recipe).execute()
        return response

    @staticmethod
    def find_by_id(recipe_id: int):
        response = RecipeProvider.recipe_table.select("*").eq('id', recipe_id).execute()
        return response

    @staticmethod
    def find_all(offset: int = 0, limit: int = 10) :
        response = RecipeProvider.recipe_table.select('*').range(offset, limit).execute()
        return response