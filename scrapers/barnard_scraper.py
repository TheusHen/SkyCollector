import requests
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

SOURCE_NAME = "barnard_astronomical_society"

def scrape():
    """
    Scrapes the latest image from the Barnard Astronomical Society all-sky camera.
    """
    url = "http://barnardstar.org/AllSky/image.jpg"

    logger.info(f"[{SOURCE_NAME}] Downloading image from {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"[{SOURCE_NAME}] Failed to download image: {e}")
        return None, None

    # Create a temporary directory for the image
    os.makedirs("tmp", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    image_path = os.path.join("tmp", f"{SOURCE_NAME}_{timestamp}.jpg")

    try:
        with open(image_path, "wb") as f:
            f.write(response.content)
        logger.info(f"[{SOURCE_NAME}] Image saved to {image_path} ({len(response.content)} bytes)")
    except IOError as e:
        logger.error(f"[{SOURCE_NAME}] Failed to save image: {e}")
        return None, None

    return image_path, {"source": SOURCE_NAME, "url": url}

if __name__ == "__main__":
    scrape()
