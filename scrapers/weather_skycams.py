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

# Collection of weather station sky cameras
WEATHER_SKYCAMS = [
    # WeatherUSA Sky Cams
    {
        "name": "weatherusa_ohio_cmh",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=OHCMH1",
        "description": "Columbus, Ohio SkyCam"
    },
    {
        "name": "weatherusa_ohio_cleveland",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=OHCLE1",
        "description": "Cleveland, Ohio SkyCam"
    },
    {
        "name": "weatherusa_indiana_indianapolis",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=ININD1",
        "description": "Indianapolis, Indiana SkyCam"
    },
    {
        "name": "weatherusa_michigan_detroit",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=MIDET1",
        "description": "Detroit, Michigan SkyCam"
    },
    {
        "name": "weatherusa_illinois_chicago",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=ILCHI1",
        "description": "Chicago, Illinois SkyCam"
    },
    {
        "name": "weatherusa_pennsylvania_pittsburgh",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=PAPIT1",
        "description": "Pittsburgh, Pennsylvania SkyCam"
    },
    {
        "name": "weatherusa_new_york",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=NYNYC1",
        "description": "New York, New York SkyCam"
    },
    {
        "name": "weatherusa_massachusetts_boston",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=MABOS1",
        "description": "Boston, Massachusetts SkyCam"
    },
    {
        "name": "weatherusa_florida_miami",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=FLMIA1",
        "description": "Miami, Florida SkyCam"
    },
    {
        "name": "weatherusa_texas_houston",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=TXHOU1",
        "description": "Houston, Texas SkyCam"
    },
    {
        "name": "weatherusa_california_la",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=CALAX1",
        "description": "Los Angeles, California SkyCam"
    },
    {
        "name": "weatherusa_washington_seattle",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=WASEA1",
        "description": "Seattle, Washington SkyCam"
    },
    {
        "name": "weatherusa_arizona_phoenix",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=AZPHX1",
        "description": "Phoenix, Arizona SkyCam"
    },
    {
        "name": "weatherusa_colorado_denver",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=CODEN1",
        "description": "Denver, Colorado SkyCam"
    },
    {
        "name": "weatherusa_nevada_las_vegas",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=NVLAS1",
        "description": "Las Vegas, Nevada SkyCam"
    },
    {
        "name": "weatherusa_georgia_atlanta",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=GAATL1",
        "description": "Atlanta, Georgia SkyCam"
    },
    {
        "name": "weatherusa_north_carolina_charlotte",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=NCCHA1",
        "description": "Charlotte, North Carolina SkyCam"
    },
    {
        "name": "weatherusa_tennessee_nashville",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=TNNSH1",
        "description": "Nashville, Tennessee SkyCam"
    },
    {
        "name": "weatherusa_missouri_st_louis",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=MOSTL1",
        "description": "St. Louis, Missouri SkyCam"
    },
    {
        "name": "weatherusa_minnesota_minneapolis",
        "url": "https://www.weatherusa.net/skycamnet/index.php?cam=MNMSP1",
        "description": "Minneapolis, Minnesota SkyCam"
    },
]

SOURCE_NAME_PREFIX = "weather_skycam"

def scrape_weatherusa_cam(cam_url, source_name):
    """
    Scrapes a single WeatherUSA SkyCam.
    """
    logger.info(f"[{source_name}] Fetching page from {cam_url}")
    
    try:
        response = requests.get(cam_url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"[{source_name}] Failed to fetch page: {e}")
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
        logger.error(f"[{source_name}] Could not find image URL on page.")
        return None, None

    image_url = img_tag["src"]

    if not image_url.startswith("http"):
        image_url = "https:" + image_url

    logger.info(f"[{source_name}] Downloading image from {image_url}")
    
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"[{source_name}] Failed to download image: {e}")
        return None, None

    # Create a temporary directory for the image
    os.makedirs("tmp", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    image_path = os.path.join("tmp", f"{source_name}_{timestamp}.jpg")

    try:
        with open(image_path, "wb") as f:
            f.write(response.content)
        logger.info(f"[{source_name}] Image saved to {image_path} ({len(response.content)} bytes)")
    except IOError as e:
        logger.error(f"[{source_name}] Failed to save image: {e}")
        return None, None

    return image_path, {"source": source_name, "page_url": cam_url, "image_url": image_url}

def scrape():
    """
    Scrapes weather station sky cameras. Returns the first successful one.
    """
    for camera in WEATHER_SKYCAMS:
        result = scrape_weatherusa_cam(camera["url"], camera["name"])
        if result[0] is not None:
            return result
    
    logger.error("All weather station sky camera scrapes failed")
    return None, None

if __name__ == "__main__":
    scrape()
