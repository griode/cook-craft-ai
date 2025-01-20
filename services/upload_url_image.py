from datetime import datetime
import uuid
from urllib.parse import urlparse
import requests
from config import supabase_client


def generate_file_name(extension: str) -> str:
    """
    Generates a unique file name based on a UUID and a timestamp.

    Args:
        extension (str): The file extension (e.g., 'jpg', 'png').

    Returns:
        str: A unique file name in the format 'YYYYMMDDHHMMSS_UUID.extension'.
    """
    unique_id = uuid.uuid4().hex  # Generate a unique identifier
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Generate a timestamp
    return f"{timestamp}_{unique_id}.{extension}"


def get_image_extension(url: str) -> str:
    """
    Extracts the image file extension from the URL.

    Args:
        url (str): The URL of the image.

    Returns:
        str: The image extension (e.g., 'jpg', 'png').
    """
    # Parse the URL and remove query parameters
    url_without_params = urlparse(url)._replace(query='').geturl()

    # Extract the extension from the file name
    extension = url_without_params.split('.')[-1].lower()

    # Validate that the extension exists and is plausible
    if not extension or len(extension) > 5:  # Arbitrary max length for extensions
        raise ValueError(f"Invalid or missing file extension in URL: {url}")

    return extension


def save_image(url: str, bucket: str):
   
    try:
        # Download the image
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
        # Extract the image extension
        image_format = get_image_extension(url)
        # Generate a unique file name
        file_name = generate_file_name(extension=image_format)

        # Upload the image to the specified Supabase bucket
        upload_response = supabase_client.storage.from_(bucket).upload(
            file_name, response.content, {"content-type": f"image/{image_format}"}
        )
        return {
           "url": f"https://kwzdocspghdcsinmkpex.supabase.co/storage/v1/object/public/{upload_response.full_path}",
            "details": upload_response,
        }
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to download image: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred during the upload: {e}")