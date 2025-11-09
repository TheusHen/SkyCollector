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

# Collection of all-sky camera URLs from various observatories and amateur astronomers
ALLSKY_CAMERAS = [
    # USA All-Sky Cameras
    {
        "name": "allsky_tenerife_iac",
        "url": "http://www.iac.es/weather/lastimages/lastimage_allsky.jpg",
        "description": "Instituto de Astrofísica de Canarias, Tenerife"
    },
    {
        "name": "allsky_mto_sa_gov",
        "url": "http://site.mto.sa.gov.au/campbelltown/latest_image.jpg",
        "description": "MTO South Australia All-Sky Camera"
    },
    {
        "name": "allsky_obs_carnegiescience",
        "url": "https://obs.carnegiescience.edu/allsky/AllSkyCurrentImage.JPG",
        "description": "Las Campanas Observatory, Chile"
    },
    {
        "name": "allsky_lowell_edu",
        "url": "http://www.lowell.edu/wp-content/uploads/2015/12/allsky.jpg",
        "description": "Lowell Observatory All-Sky Camera"
    },
    {
        "name": "allsky_tug",
        "url": "http://allsky.tug.tubitak.gov.tr/images/current_image.jpg",
        "description": "TÜBİTAK National Observatory, Turkey"
    },
    {
        "name": "allsky_nmsu",
        "url": "http://telescope.nmsu.edu/images/allsky.jpg",
        "description": "New Mexico State University Observatory"
    },
    {
        "name": "allsky_kpno",
        "url": "http://www.kpno.noao.edu/Images/webcam/allsky.jpg",
        "description": "Kitt Peak National Observatory All-Sky"
    },
    {
        "name": "allsky_eso_paranal",
        "url": "http://www.eso.org/public/images/paranal-allsky-cc.jpg",
        "description": "ESO Paranal Observatory All-Sky Camera"
    },
    {
        "name": "allsky_eso_lasilla",
        "url": "http://www.eso.org/public/images/lasilla-allsky-cc.jpg",
        "description": "ESO La Silla Observatory All-Sky Camera"
    },
    {
        "name": "allsky_maunakea",
        "url": "http://mkwc.ifa.hawaii.edu/current/cams/cfhtcam/cfhtallsky.jpg",
        "description": "Mauna Kea Weather Center All-Sky"
    },
    {
        "name": "allsky_cfht",
        "url": "http://www.cfht.hawaii.edu/en/gallery/images/skycam.jpg",
        "description": "Canada-France-Hawaii Telescope All-Sky"
    },
    {
        "name": "allsky_gemini_north",
        "url": "http://www.gemini.edu/sciops/telescopes-and-sites/weather/mauna-kea/allsky-current.jpg",
        "description": "Gemini North Observatory All-Sky"
    },
    {
        "name": "allsky_gemini_south",
        "url": "http://www.gemini.edu/sciops/telescopes-and-sites/weather/cerro-pachon/allsky-current.jpg",
        "description": "Gemini South Observatory All-Sky"
    },
    {
        "name": "allsky_subaru",
        "url": "http://mkwc.ifa.hawaii.edu/current/cams/subarucam/image.jpg",
        "description": "Subaru Telescope All-Sky Camera"
    },
    {
        "name": "allsky_astroport_sabadell",
        "url": "http://www.astrosabadell.org/sabadell/allsky/allsky.jpg",
        "description": "Astroport Sabadell, Spain"
    },
    {
        "name": "allsky_obs_hp",
        "url": "http://www.obs-hp.fr/meteo/allsky.jpg",
        "description": "Observatoire de Haute-Provence All-Sky"
    },
    {
        "name": "allsky_pic_du_midi",
        "url": "http://www.picdumidi.com/webcams/allsky/current.jpg",
        "description": "Pic du Midi Observatory All-Sky"
    },
    {
        "name": "allsky_ukirt",
        "url": "http://www.ukirt.hawaii.edu/images/current_allsky.jpg",
        "description": "UK Infrared Telescope All-Sky"
    },
    {
        "name": "allsky_irtf",
        "url": "http://irtfweb.ifa.hawaii.edu/allsky/current_allsky.jpg",
        "description": "NASA Infrared Telescope Facility All-Sky"
    },
    {
        "name": "allsky_mro",
        "url": "http://mro.nmt.edu/allsky/allsky.jpg",
        "description": "Magdalena Ridge Observatory All-Sky"
    },
    {
        "name": "allsky_aao",
        "url": "http://www.aao.gov.au/images/calib/allsky/allsky.jpg",
        "description": "Anglo-Australian Observatory All-Sky"
    },
    {
        "name": "allsky_sso",
        "url": "http://msowww.anu.edu.au/~rmr/ssso_allsky.jpg",
        "description": "Siding Spring Observatory All-Sky"
    },
    {
        "name": "allsky_saao",
        "url": "http://www.saao.ac.za/~holtzman/allsky/allsky.jpg",
        "description": "South African Astronomical Observatory"
    },
    {
        "name": "allsky_salt",
        "url": "http://www.salt.ac.za/weather-and-seeing/allsky-latest.jpg",
        "description": "Southern African Large Telescope All-Sky"
    },
    {
        "name": "allsky_sonear",
        "url": "http://www.sonear.com.br/allsky/latest.jpg",
        "description": "SONEAR Observatory, Brazil"
    },
    {
        "name": "allsky_coast_nrao",
        "url": "http://www.gb.nrao.edu/~rmaddale/Weather/allsky.jpg",
        "description": "Green Bank Observatory All-Sky"
    },
    {
        "name": "allsky_skyquality_uniroma1",
        "url": "http://www.skyquality.eu/camera/Current_AllSkyImage.jpg",
        "description": "Sky Quality Meter Network, Rome"
    },
    {
        "name": "allsky_sterrekunst",
        "url": "http://www.sterrekunst.be/allsky/allsky.jpg",
        "description": "Sterrekunst Observatory, Belgium"
    },
    {
        "name": "allsky_skinakas",
        "url": "http://www.skinakas.physics.uoc.gr/weather/allsky.jpg",
        "description": "Skinakas Observatory, Crete"
    },
    {
        "name": "allsky_helmos",
        "url": "http://helmos.astro.noa.gr/allsky/allsky.jpg",
        "description": "Helmos Observatory, Greece"
    },
    {
        "name": "allsky_tartu",
        "url": "http://www.aai.ee/allsky/latest.jpg",
        "description": "Tartu Observatory, Estonia"
    },
    {
        "name": "allsky_tuorla",
        "url": "http://www.astro.utu.fi/weather/allsky_latest.jpg",
        "description": "Tuorla Observatory, Finland"
    },
    {
        "name": "allsky_oa_cagliari",
        "url": "http://www.oa-cagliari.inaf.it/meteo/allsky.jpg",
        "description": "Cagliari Astronomical Observatory, Italy"
    },
    {
        "name": "allsky_ouca",
        "url": "http://ouca.uca.es/allsky/current.jpg",
        "description": "University of Cadiz Observatory, Spain"
    },
    {
        "name": "allsky_caha",
        "url": "http://www.caha.es/allsky/allsky.jpg",
        "description": "Calar Alto Observatory All-Sky"
    },
    {
        "name": "allsky_tng",
        "url": "http://www.tng.iac.es/weather/allsky.jpg",
        "description": "Telescopio Nazionale Galileo All-Sky"
    },
    {
        "name": "allsky_not",
        "url": "http://www.not.iac.es/weather/allsky.jpg",
        "description": "Nordic Optical Telescope All-Sky"
    },
    {
        "name": "allsky_mercator",
        "url": "http://www.mercator.iac.es/weather/allsky.jpg",
        "description": "Mercator Telescope All-Sky"
    },
    {
        "name": "allsky_liverpool",
        "url": "http://telescope.livjm.ac.uk/images/allsky.jpg",
        "description": "Liverpool Telescope All-Sky"
    },
    {
        "name": "allsky_int",
        "url": "http://www.ing.iac.es/weather/allsky/allsky_int.jpg",
        "description": "Isaac Newton Telescope All-Sky"
    },
    {
        "name": "allsky_wht",
        "url": "http://www.ing.iac.es/weather/allsky/allsky_wht.jpg",
        "description": "William Herschel Telescope All-Sky"
    },
]

SOURCE_NAME_PREFIX = "allsky"

def scrape_camera(camera_info):
    """
    Scrapes a single all-sky camera image.
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
    Scrapes all all-sky cameras. Returns the first successful one.
    """
    for camera in ALLSKY_CAMERAS:
        result = scrape_camera(camera)
        if result[0] is not None:
            return result
    
    logger.error("All all-sky camera scrapes failed")
    return None, None

if __name__ == "__main__":
    scrape()
