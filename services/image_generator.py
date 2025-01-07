from requests import post
from config import config

# Request headers
headers = {
    "Authorization": f"Bearer {config.get('image_gen_model_key')}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def text_to_image(text: str) -> str:
    payload = {
        "style": "photorealism",
        "prompt": text,
        "aspect_ratio": "1:1",
        "output_format": "png",
        "response_format": "url",
        "width": 832,
        "height": 832,
    }

    try:
        response = post(
            config.get('image_gen_model_url'),
            json=payload, headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('url')
        else:
            print(f'Error while generating image text: {response.json()}')
            return ''

    except Exception as e:
        print(e)
        return ''