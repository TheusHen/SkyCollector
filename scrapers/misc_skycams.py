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

# Collection of miscellaneous sky cameras from around the world
MISC_SKYCAMS = [
    # Dark Sky Preserves and Observatories
    {
        "name": "darksky_cherry_springs",
        "url": "http://www.cherrysprings.org/allsky/allsky.jpg",
        "description": "Cherry Springs State Park, PA"
    },
    {
        "name": "darksky_jasper",
        "url": "http://www.jasperskytram.com/allsky/allsky.jpg",
        "description": "Jasper Dark Sky Preserve, Canada"
    },
    {
        "name": "darksky_galloway",
        "url": "http://www.gallowayforestskypark.org/allsky/allsky.jpg",
        "description": "Galloway Forest Dark Sky Park, UK"
    },
    {
        "name": "darksky_brecon_beacons",
        "url": "http://www.breconbeacons.org/allsky/allsky.jpg",
        "description": "Brecon Beacons Dark Sky Reserve, Wales"
    },
    {
        "name": "darksky_exmoor",
        "url": "http://www.exmoor-nationalpark.gov.uk/allsky/allsky.jpg",
        "description": "Exmoor Dark Sky Reserve, UK"
    },
    # Radio Astronomy Observatories
    {
        "name": "radio_arecibo",
        "url": "http://www.naic.edu/~astro/allsky/allsky.jpg",
        "description": "Arecibo Observatory All-Sky"
    },
    {
        "name": "radio_parkes",
        "url": "http://www.parkes.atnf.csiro.au/weather/allsky.jpg",
        "description": "Parkes Observatory All-Sky"
    },
    {
        "name": "radio_jodrell_bank",
        "url": "http://www.jb.man.ac.uk/allsky/allsky.jpg",
        "description": "Jodrell Bank Observatory All-Sky"
    },
    {
        "name": "radio_effelsberg",
        "url": "http://www.mpifr-bonn.mpg.de/allsky/allsky.jpg",
        "description": "Effelsberg Radio Observatory All-Sky"
    },
    {
        "name": "radio_vla",
        "url": "http://www.vla.nrao.edu/astro/allsky/allsky.jpg",
        "description": "Very Large Array All-Sky"
    },
    {
        "name": "radio_alma",
        "url": "http://www.almaobservatory.org/allsky/allsky.jpg",
        "description": "ALMA Observatory All-Sky"
    },
    # Planetariums and Science Centers
    {
        "name": "planetarium_griffith",
        "url": "http://www.griffithobs.org/allsky/allsky.jpg",
        "description": "Griffith Observatory, Los Angeles"
    },
    {
        "name": "planetarium_adler",
        "url": "http://www.adlerplanetarium.org/allsky/allsky.jpg",
        "description": "Adler Planetarium, Chicago"
    },
    {
        "name": "planetarium_hayden",
        "url": "http://www.amnh.org/hayden/allsky/allsky.jpg",
        "description": "Hayden Planetarium, New York"
    },
    {
        "name": "planetarium_franklin",
        "url": "http://www.fi.edu/allsky/allsky.jpg",
        "description": "Franklin Institute, Philadelphia"
    },
    # Amateur Astronomy Clubs
    {
        "name": "amateur_canberra",
        "url": "http://www.canberraastronomy.org/allsky/allsky.jpg",
        "description": "Canberra Astronomical Society"
    },
    {
        "name": "amateur_perth",
        "url": "http://www.perthobservatory.wa.gov.au/allsky/allsky.jpg",
        "description": "Perth Observatory"
    },
    {
        "name": "amateur_auckland",
        "url": "http://www.astronomy.org.nz/allsky/allsky.jpg",
        "description": "Auckland Observatory"
    },
    {
        "name": "amateur_christchurch",
        "url": "http://www.astronomy.net.nz/allsky/allsky.jpg",
        "description": "Christchurch Astronomical Society"
    },
    {
        "name": "amateur_buenos_aires",
        "url": "http://www.astronomia.com.ar/allsky/allsky.jpg",
        "description": "Buenos Aires Observatory"
    },
    {
        "name": "amateur_santiago",
        "url": "http://www.achaya.cl/allsky/allsky.jpg",
        "description": "Santiago Astronomical Society, Chile"
    },
    {
        "name": "amateur_bogota",
        "url": "http://www.astrocol.org/allsky/allsky.jpg",
        "description": "Bogota Astronomical Observatory"
    },
    {
        "name": "amateur_mexico_city",
        "url": "http://www.astromexico.org/allsky/allsky.jpg",
        "description": "Mexico City Astronomical Society"
    },
    # Research Stations and Remote Locations
    {
        "name": "remote_concordia",
        "url": "http://www.concordiastation.aq/allsky/allsky.jpg",
        "description": "Concordia Station, Antarctica"
    },
    {
        "name": "remote_summit_camp",
        "url": "http://www.summitcamp.org/allsky/allsky.jpg",
        "description": "Summit Camp, Greenland"
    },
    {
        "name": "remote_halley",
        "url": "http://www.antarctica.ac.uk/allsky/halley/allsky.jpg",
        "description": "Halley Research Station, Antarctica"
    },
    {
        "name": "remote_syowa",
        "url": "http://www.nipr.ac.jp/allsky/syowa/allsky.jpg",
        "description": "Syowa Station, Antarctica"
    },
    {
        "name": "remote_zhongshan",
        "url": "http://www.chinare.gov.cn/allsky/zhongshan/allsky.jpg",
        "description": "Zhongshan Station, Antarctica"
    },
    # Mountain Observatories
    {
        "name": "mountain_wendelstein",
        "url": "http://www.wendelstein-observatorium.de/allsky/allsky.jpg",
        "description": "Wendelstein Observatory, Germany"
    },
    {
        "name": "mountain_jungfraujoch",
        "url": "http://www.hfsjg.ch/allsky/allsky.jpg",
        "description": "Jungfraujoch High Altitude Station"
    },
    {
        "name": "mountain_sphinx",
        "url": "http://sphinx.epfl.ch/allsky/allsky.jpg",
        "description": "Sphinx Observatory, Switzerland"
    },
    {
        "name": "mountain_teide",
        "url": "http://www.iac.es/ot/allsky/teide/allsky.jpg",
        "description": "Teide Observatory, Canary Islands"
    },
    {
        "name": "mountain_roque",
        "url": "http://www.iac.es/ot/allsky/roque/allsky.jpg",
        "description": "Roque de los Muchachos, La Palma"
    },
    # Island Observatories
    {
        "name": "island_hawaii_haleakala",
        "url": "http://www.ifa.hawaii.edu/haleakala/allsky/allsky.jpg",
        "description": "Haleakala Observatory, Maui"
    },
    {
        "name": "island_tenerife_ot",
        "url": "http://www.iac.es/ot/allsky/tenerife/allsky.jpg",
        "description": "Teide Observatory, Tenerife"
    },
    {
        "name": "island_la_reunion",
        "url": "http://www.obs-reunion.fr/allsky/allsky.jpg",
        "description": "La Réunion Observatory"
    },
    {
        "name": "island_madeira",
        "url": "http://www.madeira.org/allsky/allsky.jpg",
        "description": "Madeira Observatory"
    },
    {
        "name": "island_azores",
        "url": "http://www.oal.ul.pt/azores/allsky/allsky.jpg",
        "description": "Azores Observatory"
    },
    # Meteor scatter and Radio Sky Monitoring
    {
        "name": "radio_graves_france",
        "url": "http://www.astrosurf.com/re/graves/allsky/allsky.jpg",
        "description": "GRAVES Radar Meteor Scatter, France"
    },
    {
        "name": "radio_brams_belgium",
        "url": "http://www.brams.aeronomie.be/allsky/allsky.jpg",
        "description": "BRAMS Meteor Network, Belgium"
    },
]

SOURCE_NAME_PREFIX = "misc_skycam"

def scrape_camera(camera_info):
    """
    Scrapes a single miscellaneous sky camera image.
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
    Scrapes miscellaneous sky cameras. Returns the first successful one.
    """
    for camera in MISC_SKYCAMS:
        result = scrape_camera(camera)
        if result[0] is not None:
            return result
    
    logger.error("All miscellaneous sky camera scrapes failed")
    return None, None

if __name__ == "__main__":
    scrape()
