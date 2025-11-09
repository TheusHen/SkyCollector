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

# Collection of meteor detection and fireball cameras
METEOR_CAMERAS = [
    # Global Meteor Network
    {
        "name": "meteor_gmn_croatia_1",
        "url": "http://globalmeteornetwork.org/cameras/HR0001/latest.jpg",
        "description": "Global Meteor Network, Croatia Station 1"
    },
    {
        "name": "meteor_gmn_usa_1",
        "url": "http://globalmeteornetwork.org/cameras/US0001/latest.jpg",
        "description": "Global Meteor Network, USA Station 1"
    },
    {
        "name": "meteor_gmn_australia_1",
        "url": "http://globalmeteornetwork.org/cameras/AU0001/latest.jpg",
        "description": "Global Meteor Network, Australia Station 1"
    },
    {
        "name": "meteor_gmn_canada_1",
        "url": "http://globalmeteornetwork.org/cameras/CA0001/latest.jpg",
        "description": "Global Meteor Network, Canada Station 1"
    },
    {
        "name": "meteor_gmn_uk_1",
        "url": "http://globalmeteornetwork.org/cameras/UK0001/latest.jpg",
        "description": "Global Meteor Network, UK Station 1"
    },
    # NASA All-Sky Fireball Network
    {
        "name": "meteor_nasa_huntsville",
        "url": "http://fireballs.ndc.nasa.gov/allsky/huntsville/latest.jpg",
        "description": "NASA All-Sky Fireball, Huntsville AL"
    },
    {
        "name": "meteor_nasa_tullahoma",
        "url": "http://fireballs.ndc.nasa.gov/allsky/tullahoma/latest.jpg",
        "description": "NASA All-Sky Fireball, Tullahoma TN"
    },
    {
        "name": "meteor_nasa_dahlonega",
        "url": "http://fireballs.ndc.nasa.gov/allsky/dahlonega/latest.jpg",
        "description": "NASA All-Sky Fireball, Dahlonega GA"
    },
    {
        "name": "meteor_nasa_oberlin",
        "url": "http://fireballs.ndc.nasa.gov/allsky/oberlin/latest.jpg",
        "description": "NASA All-Sky Fireball, Oberlin OH"
    },
    {
        "name": "meteor_nasa_cloudsrest",
        "url": "http://fireballs.ndc.nasa.gov/allsky/cloudsrest/latest.jpg",
        "description": "NASA All-Sky Fireball, Clouds Rest CA"
    },
    # CAMS (Cameras for Allsky Meteor Surveillance)
    {
        "name": "meteor_cams_bayarea_1",
        "url": "http://cams.seti.org/CAMS/Bay_Area/latest/cam1.jpg",
        "description": "CAMS Bay Area Station 1"
    },
    {
        "name": "meteor_cams_bayarea_2",
        "url": "http://cams.seti.org/CAMS/Bay_Area/latest/cam2.jpg",
        "description": "CAMS Bay Area Station 2"
    },
    {
        "name": "meteor_cams_benelux_1",
        "url": "http://cams.seti.org/CAMS/BeNeLux/latest/cam1.jpg",
        "description": "CAMS BeNeLux Station 1"
    },
    {
        "name": "meteor_cams_florida_1",
        "url": "http://cams.seti.org/CAMS/Florida/latest/cam1.jpg",
        "description": "CAMS Florida Station 1"
    },
    {
        "name": "meteor_cams_texas_1",
        "url": "http://cams.seti.org/CAMS/Texas/latest/cam1.jpg",
        "description": "CAMS Texas Station 1"
    },
    # IMO (International Meteor Organization) Video Network
    {
        "name": "meteor_imo_croatia",
        "url": "http://www.imo.net/data/visual/croatia/latest.jpg",
        "description": "IMO Video Network, Croatia"
    },
    {
        "name": "meteor_imo_germany",
        "url": "http://www.imo.net/data/visual/germany/latest.jpg",
        "description": "IMO Video Network, Germany"
    },
    {
        "name": "meteor_imo_france",
        "url": "http://www.imo.net/data/visual/france/latest.jpg",
        "description": "IMO Video Network, France"
    },
    {
        "name": "meteor_imo_italy",
        "url": "http://www.imo.net/data/visual/italy/latest.jpg",
        "description": "IMO Video Network, Italy"
    },
    # UK Meteor Network
    {
        "name": "meteor_ukmon_edinburgh",
        "url": "http://www.ukmeteornetwork.co.uk/cameras/edinburgh/latest.jpg",
        "description": "UK Meteor Network, Edinburgh"
    },
    {
        "name": "meteor_ukmon_london",
        "url": "http://www.ukmeteornetwork.co.uk/cameras/london/latest.jpg",
        "description": "UK Meteor Network, London"
    },
    {
        "name": "meteor_ukmon_manchester",
        "url": "http://www.ukmeteornetwork.co.uk/cameras/manchester/latest.jpg",
        "description": "UK Meteor Network, Manchester"
    },
    {
        "name": "meteor_ukmon_oxford",
        "url": "http://www.ukmeteornetwork.co.uk/cameras/oxford/latest.jpg",
        "description": "UK Meteor Network, Oxford"
    },
    {
        "name": "meteor_ukmon_bristol",
        "url": "http://www.ukmeteornetwork.co.uk/cameras/bristol/latest.jpg",
        "description": "UK Meteor Network, Bristol"
    },
    # Australia Meteor Camera Network
    {
        "name": "meteor_australia_canberra",
        "url": "http://fireballsinthesky.com.au/cameras/canberra/latest.jpg",
        "description": "Australia Meteor Network, Canberra"
    },
    {
        "name": "meteor_australia_sydney",
        "url": "http://fireballsinthesky.com.au/cameras/sydney/latest.jpg",
        "description": "Australia Meteor Network, Sydney"
    },
    {
        "name": "meteor_australia_melbourne",
        "url": "http://fireballsinthesky.com.au/cameras/melbourne/latest.jpg",
        "description": "Australia Meteor Network, Melbourne"
    },
    {
        "name": "meteor_australia_brisbane",
        "url": "http://fireballsinthesky.com.au/cameras/brisbane/latest.jpg",
        "description": "Australia Meteor Network, Brisbane"
    },
    {
        "name": "meteor_australia_perth",
        "url": "http://fireballsinthesky.com.au/cameras/perth/latest.jpg",
        "description": "Australia Meteor Network, Perth"
    },
    # SonotaCo Meteor Network (Japan)
    {
        "name": "meteor_sonotaco_tokyo",
        "url": "http://sonotaco.jp/soft/met/latest/tokyo.jpg",
        "description": "SonotaCo Network, Tokyo"
    },
    {
        "name": "meteor_sonotaco_osaka",
        "url": "http://sonotaco.jp/soft/met/latest/osaka.jpg",
        "description": "SonotaCo Network, Osaka"
    },
    {
        "name": "meteor_sonotaco_nagoya",
        "url": "http://sonotaco.jp/soft/met/latest/nagoya.jpg",
        "description": "SonotaCo Network, Nagoya"
    },
]

SOURCE_NAME_PREFIX = "meteor"

def scrape_camera(camera_info):
    """
    Scrapes a single meteor camera image.
    """
    source_name = camera_info["name"]
    url = camera_info["url"]
    
    logger.info(f"[{source_name}] Downloading image from {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"[{source_name}] Failed to download image: {e}")
        return None, None

    # Create a temporary directory for the image
    os.makedirs("tmp", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    
    # Determine file extension from URL
    ext = "jpg"
    if ".png" in url.lower():
        ext = "png"
    elif ".jpeg" in url.lower():
        ext = "jpeg"
    
    image_path = os.path.join("tmp", f"{source_name}_{timestamp}.{ext}")

    try:
        with open(image_path, "wb") as f:
            f.write(response.content)
        logger.info(f"[{source_name}] Image saved to {image_path} ({len(response.content)} bytes)")
    except IOError as e:
        logger.error(f"[{source_name}] Failed to save image: {e}")
        return None, None

    return image_path, {
        "source": source_name,
        "url": url,
        "description": camera_info["description"]
    }

def scrape():
    """
    Scrapes meteor detection cameras. Returns the first successful one.
    """
    for camera in METEOR_CAMERAS:
        result = scrape_camera(camera)
        if result[0] is not None:
            return result
    
    logger.error("All meteor camera scrapes failed")
    return None, None

if __name__ == "__main__":
    scrape()
