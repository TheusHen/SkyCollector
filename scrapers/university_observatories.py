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

# Collection of university and educational observatory cameras
UNIVERSITY_CAMERAS = [
    # USA Universities
    {
        "name": "university_arizona_sos",
        "url": "http://skycam.as.arizona.edu/allsky.jpg",
        "description": "University of Arizona Steward Observatory"
    },
    {
        "name": "university_berkeley",
        "url": "http://w.astro.berkeley.edu/~bait/kpno/webcam/allsky.jpg",
        "description": "UC Berkeley Leuschner Observatory"
    },
    {
        "name": "university_yale",
        "url": "http://www.astro.yale.edu/smarts/yalo/weather/allsky.jpg",
        "description": "Yale SMARTS Consortium All-Sky"
    },
    {
        "name": "university_caltech",
        "url": "http://www.astro.caltech.edu/palomar/allsky/allsky.jpg",
        "description": "Caltech Palomar Observatory"
    },
    {
        "name": "university_mit",
        "url": "http://www.haystack.mit.edu/atm/weather/allsky.jpg",
        "description": "MIT Haystack Observatory"
    },
    {
        "name": "university_chicago",
        "url": "http://astro.uchicago.edu/weather/allsky_latest.jpg",
        "description": "University of Chicago Observatory"
    },
    {
        "name": "university_indiana",
        "url": "http://www.astro.indiana.edu/morgan/allsky.jpg",
        "description": "Indiana University Morgan Observatory"
    },
    {
        "name": "university_cornell",
        "url": "http://hosting.astro.cornell.edu/~arri/allsky/allsky.jpg",
        "description": "Cornell University Observatory"
    },
    {
        "name": "university_wisconsin",
        "url": "http://www.astro.wisc.edu/observatory/allsky.jpg",
        "description": "University of Wisconsin Observatory"
    },
    {
        "name": "university_michigan",
        "url": "http://www.astro.lsa.umich.edu/observatory/allsky/allsky.jpg",
        "description": "University of Michigan Observatory"
    },
    {
        "name": "university_texas_mcdonald",
        "url": "http://www.astro.as.utexas.edu/mcdonald/allsky/allsky.jpg",
        "description": "McDonald Observatory, University of Texas"
    },
    {
        "name": "university_hawaii_ifa",
        "url": "http://www.ifa.hawaii.edu/~observer/weather/allsky.jpg",
        "description": "University of Hawaii Institute for Astronomy"
    },
    {
        "name": "university_colorado",
        "url": "http://sirius.colorado.edu/weather/allsky.jpg",
        "description": "University of Colorado Sommers-Bausch Observatory"
    },
    {
        "name": "university_penn_state",
        "url": "http://www.astro.psu.edu/images/allsky/allsky.jpg",
        "description": "Penn State Observatory"
    },
    {
        "name": "university_washington",
        "url": "http://www.astro.washington.edu/obs/allsky.jpg",
        "description": "University of Washington Observatory"
    },
    # European Universities
    {
        "name": "university_oxford",
        "url": "http://www.astro.physics.ox.ac.uk/weather/allsky.jpg",
        "description": "University of Oxford Observatory"
    },
    {
        "name": "university_cambridge",
        "url": "http://www.ast.cam.ac.uk/~mjp/allsky.jpg",
        "description": "University of Cambridge Observatory"
    },
    {
        "name": "university_edinburgh",
        "url": "http://www.roe.ac.uk/ifa/weather/allsky.jpg",
        "description": "University of Edinburgh Royal Observatory"
    },
    {
        "name": "university_leiden",
        "url": "http://home.strw.leidenuniv.nl/~planetarium/allsky.jpg",
        "description": "Leiden Observatory, Netherlands"
    },
    {
        "name": "university_amsterdam",
        "url": "http://www.astro.uva.nl/allsky/allsky.jpg",
        "description": "University of Amsterdam Observatory"
    },
    {
        "name": "university_munich_lmu",
        "url": "http://www.usm.uni-muenchen.de/allsky/allsky.jpg",
        "description": "Ludwig Maximilian University Munich"
    },
    {
        "name": "university_heidelberg",
        "url": "http://www.lsw.uni-heidelberg.de/allsky/allsky.jpg",
        "description": "Heidelberg University Observatory"
    },
    {
        "name": "university_paris",
        "url": "http://www.iap.fr/allsky/allsky.jpg",
        "description": "Institut d'Astrophysique de Paris"
    },
    {
        "name": "university_toulouse",
        "url": "http://www.ast.obs-mip.fr/allsky/allsky.jpg",
        "description": "Toulouse Observatory"
    },
    {
        "name": "university_bologna",
        "url": "http://www.oas.inaf.it/loiano/allsky/allsky.jpg",
        "description": "University of Bologna Observatory"
    },
    {
        "name": "university_padova",
        "url": "http://www.oapd.inaf.it/allsky/allsky.jpg",
        "description": "Padova Observatory, Italy"
    },
    {
        "name": "university_madrid_ucm",
        "url": "http://www.ucm.es/info/Astrof/allsky/allsky.jpg",
        "description": "Complutense University of Madrid"
    },
    {
        "name": "university_barcelona",
        "url": "http://www.am.ub.edu/allsky/allsky.jpg",
        "description": "University of Barcelona Observatory"
    },
    {
        "name": "university_valencia",
        "url": "http://www.uv.es/obsast/allsky/allsky.jpg",
        "description": "University of Valencia Observatory"
    },
    {
        "name": "university_lisbon",
        "url": "http://www.oal.ul.pt/allsky/allsky.jpg",
        "description": "Lisbon Astronomical Observatory"
    },
    {
        "name": "university_warsaw",
        "url": "http://www.astrouw.edu.pl/allsky/allsky.jpg",
        "description": "Warsaw University Observatory"
    },
    {
        "name": "university_krakow",
        "url": "http://www.oa.uj.edu.pl/allsky/allsky.jpg",
        "description": "Jagiellonian University, Krakow"
    },
    {
        "name": "university_prague",
        "url": "http://sirrah.troja.mff.cuni.cz/allsky/allsky.jpg",
        "description": "Charles University, Prague"
    },
    {
        "name": "university_budapest",
        "url": "http://www.konkoly.hu/allsky/allsky.jpg",
        "description": "Konkoly Observatory, Budapest"
    },
    {
        "name": "university_vienna",
        "url": "http://www.univie.ac.at/adg/allsky/allsky.jpg",
        "description": "University of Vienna Observatory"
    },
    {
        "name": "university_stockholm",
        "url": "http://www.astro.su.se/allsky/allsky.jpg",
        "description": "Stockholm University Observatory"
    },
    {
        "name": "university_oslo",
        "url": "http://www.astro.uio.no/allsky/allsky.jpg",
        "description": "University of Oslo Observatory"
    },
    {
        "name": "university_copenhagen",
        "url": "http://www.astro.ku.dk/allsky/allsky.jpg",
        "description": "University of Copenhagen Observatory"
    },
    # Asia-Pacific Universities
    {
        "name": "university_tokyo",
        "url": "http://www.ioa.s.u-tokyo.ac.jp/allsky/allsky.jpg",
        "description": "University of Tokyo Observatory"
    },
    {
        "name": "university_kyoto",
        "url": "http://www.kusastro.kyoto-u.ac.jp/allsky/allsky.jpg",
        "description": "Kyoto University Observatory"
    },
    {
        "name": "university_beijing",
        "url": "http://www.astro.pku.edu.cn/allsky/allsky.jpg",
        "description": "Peking University Observatory"
    },
    {
        "name": "university_nanjing",
        "url": "http://www.nju.edu.cn/astronomy/allsky/allsky.jpg",
        "description": "Nanjing University Observatory"
    },
    {
        "name": "university_sydney",
        "url": "http://www.physics.usyd.edu.au/allsky/allsky.jpg",
        "description": "University of Sydney Observatory"
    },
    {
        "name": "university_melbourne",
        "url": "http://astronomy.swin.edu.au/allsky/allsky.jpg",
        "description": "Swinburne University, Melbourne"
    },
    {
        "name": "university_anu",
        "url": "http://rsaa.anu.edu.au/allsky/allsky.jpg",
        "description": "Australian National University Observatory"
    },
]

SOURCE_NAME_PREFIX = "university"

def scrape_camera(camera_info):
    """
    Scrapes a single university observatory camera image.
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
    Scrapes university observatory cameras. Returns the first successful one.
    """
    for camera in UNIVERSITY_CAMERAS:
        result = scrape_camera(camera)
        if result[0] is not None:
            return result
    
    logger.error("All university observatory camera scrapes failed")
    return None, None

if __name__ == "__main__":
    scrape()
