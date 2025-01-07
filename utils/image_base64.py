import requests
from datetime import datetime
import uuid
from urllib.parse import urlparse


def generate_file_name(extension: str, path: str) -> str:
    """
    Génère un nom de fichier unique basé sur UUID et l'horodatage.
    """
    unique_id = uuid.uuid4().hex  # Génère un identifiant unique
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Horodatage formaté
    return f"{path}/{timestamp}_{unique_id}.{extension}"


def get_image_extension(url: str) -> str:
    """
    Extrait l'extension de l'image à partir de l'URL, en tenant compte des paramètres de la requête.
    """
    # Supprimer les paramètres de la requête
    url_without_params = urlparse(url)._replace(query='').geturl()

    # Extraire l'extension après le dernier point
    extension = url_without_params.split('.')[-1]
    return extension


def upload_image_to_firestorage(data):
    try:
        url = data['url']
        # path = data['path']
        # # Télécharger l'image
        # response = requests.get(url)
        # response.raise_for_status()  # Vérifie les erreurs HTTP
        #
        # # Extraire l'extension de l'image
        # image_format = get_image_extension(url)
        #
        # # Générer un nom de fichier unique basé sur l'extension de l'image
        # file_name = generate_file_name(extension=image_format, path=path)
        #
        # # Obtenir une référence au bucket Firebase Storage
        # bucket = storage.bucket()
        # blob = bucket.blob(file_name)
        #
        # # Téléverser l'image binaire directement dans Firebase Storage
        # blob.upload_from_string(response.content, content_type=f"image/{image_format}")
        # blob.make_public()  # Rendre l'image accessible publiquement (optionnel)
        #
        # print(f"Image téléversée avec succès à : {blob.public_url}")
        # return {"data": {"url": blob.public_url, "baseUrl": url}}  # Retourne l'URL publique du fichier
        return {"data": {"url": url, "baseUrl": url}}
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
        raise
    except Exception as e:
        print(f"Erreur inconnue : {e}")
        raise