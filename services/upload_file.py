import base64
import uuid
from datetime import datetime
from urllib.parse import urlparse
from config import supabase_client

def get_image_extension(base64_image: str) -> str:
    # Split the Base64 string to extract metadata
    if "," in base64_image:
        metadata = base64_image.split(",")[0]
    else:
        metadata = base64_image  # If no metadata, handle as raw Base64

    # Check for the "data:image" prefix and extract the format
    if metadata.startswith("data:image/"):
        return metadata.split("/")[1].split(";")[0]  # Extract extension (e.g., png, jpeg)
    else:
        return "unknown"

def get_file_name(base64_image: str) -> str:
    # generate file name
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}_{unique_id}.{get_image_extension(base64_image)}"

def upload_image(bs64_image, bucket_name):
    file = bs64_image.split(",")[-1]
    image_data = base64.b64decode(file)
    file_name = get_file_name(bs64_image)
    response = supabase_client.storage.from_(bucket_name).upload(image_data, file_name)
    return response