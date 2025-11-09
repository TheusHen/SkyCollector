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

# Collection of aurora and northern lights cameras
AURORA_CAMERAS = [
    # Alaska Aurora Cams
    {
        "name": "aurora_fairbanks_gi",
        "url": "http://www.gi.alaska.edu/monitors/aurora/latest_allsky.jpg",
        "description": "Geophysical Institute, Fairbanks Alaska"
    },
    {
        "name": "aurora_poker_flat",
        "url": "http://www.pfrr.alaska.edu/aurora/latest_allsky.jpg",
        "description": "Poker Flat Research Range, Alaska"
    },
    {
        "name": "aurora_anchorage",
        "url": "http://auroraforecast.gi.alaska.edu/allsky/anchorage/latest.jpg",
        "description": "Anchorage, Alaska Aurora Camera"
    },
    {
        "name": "aurora_juneau",
        "url": "http://auroraforecast.gi.alaska.edu/allsky/juneau/latest.jpg",
        "description": "Juneau, Alaska Aurora Camera"
    },
    {
        "name": "aurora_nome",
        "url": "http://auroraforecast.gi.alaska.edu/allsky/nome/latest.jpg",
        "description": "Nome, Alaska Aurora Camera"
    },
    {
        "name": "aurora_barrow",
        "url": "http://auroraforecast.gi.alaska.edu/allsky/barrow/latest.jpg",
        "description": "Barrow, Alaska Aurora Camera"
    },
    # Canada Aurora Cams
    {
        "name": "aurora_yellowknife",
        "url": "http://auroramax.phys.ucalgary.ca/current.jpg",
        "description": "AuroraMAX Yellowknife, Canada"
    },
    {
        "name": "aurora_whitehorse",
        "url": "http://www.asc-csa.gc.ca/images/astronomie/auroramax/allsky_latest.jpg",
        "description": "Whitehorse, Yukon Aurora Cam"
    },
    {
        "name": "aurora_churchill",
        "url": "http://aurora.phys.ucalgary.ca/churchill/allsky/current.jpg",
        "description": "Churchill, Manitoba Aurora Cam"
    },
    {
        "name": "aurora_gillam",
        "url": "http://aurora.phys.ucalgary.ca/gillam/allsky/current.jpg",
        "description": "Gillam, Manitoba Aurora Cam"
    },
    {
        "name": "aurora_fort_smith",
        "url": "http://aurora.phys.ucalgary.ca/fortsmith/allsky/current.jpg",
        "description": "Fort Smith, NWT Aurora Cam"
    },
    {
        "name": "aurora_fort_mcmurray",
        "url": "http://aurora.phys.ucalgary.ca/fortmcmurray/allsky/current.jpg",
        "description": "Fort McMurray, Alberta Aurora Cam"
    },
    {
        "name": "aurora_edmonton",
        "url": "http://aurora.phys.ucalgary.ca/edmonton/allsky/current.jpg",
        "description": "Edmonton, Alberta Aurora Cam"
    },
    {
        "name": "aurora_calgary",
        "url": "http://aurora.phys.ucalgary.ca/calgary/allsky/current.jpg",
        "description": "Calgary, Alberta Aurora Cam"
    },
    {
        "name": "aurora_athabasca",
        "url": "http://aurora.phys.ucalgary.ca/athabasca/allsky/current.jpg",
        "description": "Athabasca, Alberta Aurora Cam"
    },
    # Scandinavia Aurora Cams
    {
        "name": "aurora_kiruna_iro",
        "url": "http://www.irf.se/allsky/kiruna/latest.jpg",
        "description": "Swedish Institute of Space Physics, Kiruna"
    },
    {
        "name": "aurora_abisko",
        "url": "http://www.aurora.abisko.nu/allsky/latest.jpg",
        "description": "Abisko, Sweden Aurora Station"
    },
    {
        "name": "aurora_tromso",
        "url": "http://tid.uio.no/plasma/aurora/latest.jpg",
        "description": "Tromsø, Norway Aurora Camera"
    },
    {
        "name": "aurora_longyearbyen",
        "url": "http://kho.unis.no/allsky/latest.jpg",
        "description": "Longyearbyen, Svalbard Aurora Cam"
    },
    {
        "name": "aurora_sodankyla",
        "url": "http://www.sgo.fi/pub_data/ASC/latest.jpg",
        "description": "Sodankylä Geophysical Observatory, Finland"
    },
    {
        "name": "aurora_kilpisjarvi",
        "url": "http://www.aurora-service.eu/allsky/kilpisjarvi/latest.jpg",
        "description": "Kilpisjärvi, Finland Aurora Cam"
    },
    {
        "name": "aurora_ivalo",
        "url": "http://www.aurora-service.eu/allsky/ivalo/latest.jpg",
        "description": "Ivalo, Finland Aurora Cam"
    },
    {
        "name": "aurora_muonio",
        "url": "http://www.aurora-service.eu/allsky/muonio/latest.jpg",
        "description": "Muonio, Finland Aurora Cam"
    },
    {
        "name": "aurora_levi",
        "url": "http://www.aurora-service.eu/allsky/levi/latest.jpg",
        "description": "Levi, Finland Aurora Cam"
    },
    {
        "name": "aurora_kevo",
        "url": "http://www.aurora-service.eu/allsky/kevo/latest.jpg",
        "description": "Kevo, Finland Aurora Cam"
    },
    # Iceland Aurora Cams
    {
        "name": "aurora_reykjavik",
        "url": "http://en.vedur.is/weather/webcams/allsky/reykjavik/latest.jpg",
        "description": "Reykjavik, Iceland Aurora Cam"
    },
    {
        "name": "aurora_akureyri",
        "url": "http://en.vedur.is/weather/webcams/allsky/akureyri/latest.jpg",
        "description": "Akureyri, Iceland Aurora Cam"
    },
    # Russia Aurora Cams
    {
        "name": "aurora_murmansk",
        "url": "http://aurora.pgia.ru/allsky/latest.jpg",
        "description": "Murmansk, Russia Aurora Camera"
    },
    {
        "name": "aurora_apatity",
        "url": "http://pgia.ru/allsky/apatity/latest.jpg",
        "description": "Apatity, Russia Aurora Camera"
    },
    # Greenland Aurora Cams
    {
        "name": "aurora_kangerlussuaq",
        "url": "http://www.space.dtu.dk/english/research/instruments/madrigal/allsky/latest.jpg",
        "description": "Kangerlussuaq, Greenland"
    },
    {
        "name": "aurora_qaanaaq",
        "url": "http://aurora.dmi.dk/allsky/qaanaaq/latest.jpg",
        "description": "Qaanaaq, Greenland Aurora Cam"
    },
    # Antarctica Aurora Cams (Aurora Australis)
    {
        "name": "aurora_south_pole",
        "url": "http://www.nsf.gov/geo/plr/support/southp/images/allsky.jpg",
        "description": "South Pole Station Aurora Camera"
    },
    {
        "name": "aurora_mcmurdo",
        "url": "http://www.usap.gov/videoclipsandmaps/mcmWebcam/allsky.jpg",
        "description": "McMurdo Station, Antarctica"
    },
    {
        "name": "aurora_mawson",
        "url": "http://data.aad.gov.au/aadc/webcams/mawson/allsky/latest.jpg",
        "description": "Mawson Station, Antarctica"
    },
    {
        "name": "aurora_davis",
        "url": "http://data.aad.gov.au/aadc/webcams/davis/allsky/latest.jpg",
        "description": "Davis Station, Antarctica"
    },
]

SOURCE_NAME_PREFIX = "aurora"

def scrape_camera(camera_info):
    """
    Scrapes a single aurora camera image.
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
    Scrapes aurora cameras. Returns the first successful one.
    """
    for camera in AURORA_CAMERAS:
        result = scrape_camera(camera)
        if result[0] is not None:
            return result
    
    logger.error("All aurora camera scrapes failed")
    return None, None

if __name__ == "__main__":
    scrape()
