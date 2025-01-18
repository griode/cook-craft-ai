from config import supabase_client


class UserProvider:
    userTable = supabase_client.table("users")

    @staticmethod
    def save_user(user: dict):
        response = UserProvider.userTable.insert(user).execute()
        return response

    @staticmethod
    def get_user(user_id: str):
        response = UserProvider.userTable.select("*").eq("id", user_id).execute()
        return response