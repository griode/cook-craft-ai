from fastapi import Request

# En-têtes CORS
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",  # À remplacer par votre domaine en production
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}


def handle_options_request():
    """Gère les requêtes OPTIONS pour les CORS."""
    return {"message": "ok"}, 204, CORS_HEADERS


def handle_post_request(data, data_processor):
    """
    Gère les requêtes POST en appelant la fonction appropriée.

    :param data:
    :param data_processor: Fonction pour traiter les données de la requête
    :return: Réponse JSON
    """
    try:
        # Utilisation de .get pour éviter les KeyErrors
        if not data:
            return {"error message": "Missing 'data' in request body"}, 400, CORS_HEADERS

        result = data_processor(data)
        return result, 200, CORS_HEADERS
    except Exception as e:
        print(f"Error: {e}")
        return {"error message": str(e)}, 500, CORS_HEADERS


def handle_invalid_method():
    """Gère les méthodes non supportées."""
    return {"message": "Invalid method. Only POST is allowed."}, 405, CORS_HEADERS
