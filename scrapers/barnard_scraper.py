import requests
import os
from datetime import datetime

SOURCE_NAME = "barnard_astronomical_society"

def scrape():
    """
    Scrapes the latest image from the Barnard Astronomical Society all-sky camera.
    """
    url = "http://barnardstar.org/AllSky/image.jpg"

    print(f"[{SOURCE_NAME}] Downloading image from {url}")
    response = requests.get(url)
    response.raise_for_status()

    # Create a temporary directory for the image
    os.makedirs("tmp", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    image_path = os.path.join("tmp", f"{SOURCE_NAME}_{timestamp}.jpg")

    with open(image_path, "wb") as f:
        f.write(response.content)

    print(f"[{SOURCE_NAME}] Image saved to {image_path}")

    return image_path, {"source": SOURCE_NAME}

if __name__ == "__main__":
    scrape()
