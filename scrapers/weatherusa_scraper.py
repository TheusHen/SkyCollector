import requests
from bs4 import BeautifulSoup
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

SOURCE_NAME = "weatherusa_skycam"

def scrape(cam_url="https://www.weatherusa.net/skycamnet/index.php?cam=OHCMH1"):
    """
    Scrapes the latest image from a weatherUSA SkyCam.
    """
    logger.info(f"[{SOURCE_NAME}] Fetching page from {cam_url}")
    
    try:
        response = requests.get(cam_url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"[{SOURCE_NAME}] Failed to fetch page: {e}")
        return None, None

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the image tag
    img_tag = soup.find("img", {"alt": "SkyCam Image"})
    if not img_tag:
        # Fallback for when the main image is not found
        img_tags = soup.find_all("img")
        for tag in img_tags:
            if "snap" in tag.get("src", ""):
                img_tag = tag
                break

    if not img_tag:
        logger.error(f"[{SOURCE_NAME}] Could not find image URL on page.")
        return None, None

    image_url = img_tag["src"]

    if not image_url.startswith("http"):
        image_url = "https:" + image_url

    logger.info(f"[{SOURCE_NAME}] Downloading image from {image_url}")
    
    try:
        response = requests.get(image_url, timeout=30)
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

    return image_path, {"source": SOURCE_NAME, "page_url": cam_url, "image_url": image_url}

if __name__ == "__main__":
    scrape()
