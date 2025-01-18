from config import supabase_client


class RecipeProvider:
    recipe_table = supabase_client.table("recipe")

    @staticmethod
    def save_recipe(self, recipe: dict) :
        response = self.recipe_table.insert(recipe).execute()
        return response

    def get_recipe(self, recipe_id: int):
        self.recipe_table.select("*").eq('id', recipe_id)