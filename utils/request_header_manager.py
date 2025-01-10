from fastapi import Request, Response

# En-têtes CORS
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",  # À remplacer par votre domaine en production
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}


def handle_options_request():
    """Gère les requêtes OPTIONS pour les CORS."""
    return {"message": "ok"}, 204, CORS_HEADERS


def handle_post_request(data, res: Response, data_processor):
    """
    Gère les requêtes POST en appelant la fonction appropriée.

    :param data:
    :param data_processor: Fonction pour traiter les données de la requête
    :return: Réponse JSON
    """
    res.headers.update(CORS_HEADERS)
    try:
       return {} #data_processor(data)
    except Exception as e:
        print(f"Error: {e}")
        return {"error message": str(e)}


def handle_invalid_method(res: Response):
    """Gère les méthodes non supportées."""
    return {"message": "Invalid method. Only POST is allowed."}
