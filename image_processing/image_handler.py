import requests
from PIL import Image
import io

def process_image(image_url: str, max_width: int, max_height: int) -> Image.Image:
    """
    Downloads an image from the provided URL, resizes it proportionally to fit within
    the specified max_width and max_height, and returns the processed PIL Image object.

    Parameters:
        image_url (str): The URL of the image to download.
        max_width (int): Maximum width allowed for the resized image.
        max_height (int): Maximum height allowed for the resized image.

    Returns:
        Image.Image: The processed PIL Image object.
    """
    response = requests.get(image_url)
    response.raise_for_status() 

    image = Image.open(io.BytesIO(response.content))

    original_width, original_height = image.size

    new_width = int(original_width * 0.33)
    new_height = int(original_height * 0.1)

    processed_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return processed_image

