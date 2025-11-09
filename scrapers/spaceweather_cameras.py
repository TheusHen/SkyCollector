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

# Collection of space weather, solar, and atmospheric monitoring cameras
SPACE_WEATHER_CAMERAS = [
    # NOAA Space Weather Prediction Center
    {
        "name": "spaceweather_noaa_coronagraph",
        "url": "https://services.swpc.noaa.gov/images/lasco-c2-latest.jpg",
        "description": "NOAA LASCO C2 Coronagraph"
    },
    {
        "name": "spaceweather_noaa_c3",
        "url": "https://services.swpc.noaa.gov/images/lasco-c3-latest.jpg",
        "description": "NOAA LASCO C3 Coronagraph"
    },
    {
        "name": "spaceweather_noaa_solar_disk",
        "url": "https://services.swpc.noaa.gov/images/suvi-primary-195.jpg",
        "description": "NOAA Solar Ultraviolet Imager"
    },
    {
        "name": "spaceweather_noaa_aurora_northern",
        "url": "https://services.swpc.noaa.gov/images/aurora/north/latest.jpg",
        "description": "NOAA Aurora Northern Hemisphere"
    },
    {
        "name": "spaceweather_noaa_aurora_southern",
        "url": "https://services.swpc.noaa.gov/images/aurora/south/latest.jpg",
        "description": "NOAA Aurora Southern Hemisphere"
    },
    # NASA Solar Dynamics Observatory
    {
        "name": "spaceweather_sdo_193",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193.jpg",
        "description": "SDO AIA 193 Å"
    },
    {
        "name": "spaceweather_sdo_211",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0211.jpg",
        "description": "SDO AIA 211 Å"
    },
    {
        "name": "spaceweather_sdo_304",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg",
        "description": "SDO AIA 304 Å"
    },
    {
        "name": "spaceweather_sdo_171",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg",
        "description": "SDO AIA 171 Å"
    },
    {
        "name": "spaceweather_sdo_131",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0131.jpg",
        "description": "SDO AIA 131 Å"
    },
    {
        "name": "spaceweather_sdo_335",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0335.jpg",
        "description": "SDO AIA 335 Å"
    },
    {
        "name": "spaceweather_sdo_094",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0094.jpg",
        "description": "SDO AIA 094 Å"
    },
    {
        "name": "spaceweather_sdo_hmi_continuum",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIC.jpg",
        "description": "SDO HMI Continuum"
    },
    {
        "name": "spaceweather_sdo_hmi_magnetogram",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIB.jpg",
        "description": "SDO HMI Magnetogram"
    },
    # SOHO (Solar and Heliospheric Observatory)
    {
        "name": "spaceweather_soho_eit_195",
        "url": "https://soho.nascom.nasa.gov/data/realtime/eit_195/1024/latest.jpg",
        "description": "SOHO EIT 195 Å"
    },
    {
        "name": "spaceweather_soho_eit_284",
        "url": "https://soho.nascom.nasa.gov/data/realtime/eit_284/1024/latest.jpg",
        "description": "SOHO EIT 284 Å"
    },
    {
        "name": "spaceweather_soho_eit_304",
        "url": "https://soho.nascom.nasa.gov/data/realtime/eit_304/1024/latest.jpg",
        "description": "SOHO EIT 304 Å"
    },
    {
        "name": "spaceweather_soho_mdi",
        "url": "https://soho.nascom.nasa.gov/data/realtime/mdi_igr/1024/latest.jpg",
        "description": "SOHO MDI Magnetogram"
    },
    # STEREO (Solar TErrestrial RElations Observatory)
    {
        "name": "spaceweather_stereo_ahead_195",
        "url": "https://stereo-ssc.nascom.nasa.gov/data/ins_data/ahead/euvi/195/latest.jpg",
        "description": "STEREO-A EUVI 195 Å"
    },
    {
        "name": "spaceweather_stereo_behind_195",
        "url": "https://stereo-ssc.nascom.nasa.gov/data/ins_data/behind/euvi/195/latest.jpg",
        "description": "STEREO-B EUVI 195 Å"
    },
    # Solar Optical Telescope (Japan)
    {
        "name": "spaceweather_hinode_xrt",
        "url": "http://solarwww.mtk.nao.ac.jp/en/latest_xrt_l1.jpg",
        "description": "Hinode X-Ray Telescope"
    },
    {
        "name": "spaceweather_hinode_sot",
        "url": "http://solarwww.mtk.nao.ac.jp/en/latest_sot_l1.jpg",
        "description": "Hinode Solar Optical Telescope"
    },
    # Ground-based Solar Observatories
    {
        "name": "spaceweather_gong_halpha",
        "url": "http://halpha.nso.edu/latest.jpg",
        "description": "NSO GONG H-alpha"
    },
    {
        "name": "spaceweather_gong_magnetogram",
        "url": "http://gong.nso.edu/data/magmap/latest.jpg",
        "description": "NSO GONG Magnetogram"
    },
    {
        "name": "spaceweather_kanzelhohe_halpha",
        "url": "http://www.kso.ac.at/images/latest_halpha.jpg",
        "description": "Kanzelhohe Solar Observatory H-alpha"
    },
    {
        "name": "spaceweather_big_bear",
        "url": "http://www.bbso.njit.edu/Images/latest_halpha.jpg",
        "description": "Big Bear Solar Observatory H-alpha"
    },
    {
        "name": "spaceweather_catania",
        "url": "http://www.ct.astro.it/sun/latest.jpg",
        "description": "Catania Astrophysical Observatory Solar"
    },
    {
        "name": "spaceweather_mees_halpha",
        "url": "http://www.solar.ifa.hawaii.edu/latest.jpg",
        "description": "Mees Solar Observatory H-alpha"
    },
    # Atmospheric Monitoring
    {
        "name": "spaceweather_lidar_greenland",
        "url": "http://lidar.dmi.dk/latest_image.jpg",
        "description": "DMI Lidar, Greenland"
    },
    {
        "name": "spaceweather_airglow_pisgah",
        "url": "http://allsky.terrapub.co.jp/pisgah/latest.jpg",
        "description": "Airglow Imager, Pisgah Observatory"
    },
    {
        "name": "spaceweather_noctilucent_clouds",
        "url": "http://spaceweather.com/glossary/images/nlc_latest.jpg",
        "description": "Noctilucent Clouds Monitor"
    },
]

SOURCE_NAME_PREFIX = "spaceweather"

def scrape_camera(camera_info):
    """
    Scrapes a single space weather camera image.
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
    Scrapes space weather cameras. Returns the first successful one.
    """
    for camera in SPACE_WEATHER_CAMERAS:
        result = scrape_camera(camera)
        if result[0] is not None:
            return result
    
    logger.error("All space weather camera scrapes failed")
    return None, None

if __name__ == "__main__":
    scrape()
