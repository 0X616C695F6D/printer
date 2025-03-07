import requests
from bs4 import BeautifulSoup
from PIL import Image
import io

def fetch_nasa_image_of_the_day():
    """
    Fetch the first image on NASA's 'Image of the Day' gallery.
    Returns a PIL Image object in black & white (grayscale).
    """
    url = "https://www.nasa.gov/image-of-the-day/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        )
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception(f"Failed to retrieve NASA image of the day page: {r.status_code}")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # The first item is often found in:
    # <div class="hds-gallery-item-single hds-gallery-image"> with an <img> inside
    first_item = soup.select_one(".hds-gallery-items .hds-gallery-item-single img")
    if not first_item:
        # If nothing found
        return None
    
    img_url = first_item.get("src", "").strip()
    if not img_url:
        return None
    
    # Download the image
    img_resp = requests.get(img_url, headers=headers)
    if img_resp.status_code != 200:
        return None
    
    # Open with PIL, convert to black & white
    pil_img = Image.open(io.BytesIO(img_resp.content)).convert("L")
    
    return pil_img
