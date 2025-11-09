# Automated Astronomical Data Collector (Scraping Edition)

This project automatically collects astronomical images from public webcams via web scraping, analyzes them using a combination of Python and Julia, and stores the resulting data in this repository. The goal is to build a large, timestamped dataset of the sky from various sources over time.

This version is completely free of API keys and relies on scraping public websites.

## Project Structure

- `src/python/main.py`: The main orchestrator script that runs the scrapers, invokes the analysis, and saves the results.
- `src/julia/analyze.jl`: The Julia script that performs image analysis, including star detection and moon phase calculation.
- `scrapers/`: A Python package containing individual modules for scraping each data source.
- `data/`: The directory where the collected and compressed (`.json.gz`) data is stored, organized by source.
- `logs/`: Contains detailed execution logs and collection summaries (not committed to repository).
- `.github/workflows/collect_data.yml`: The GitHub Actions workflow that automates the entire process.

## Logging and Monitoring

The application provides comprehensive logging for debugging and monitoring:

- **Console Output**: Real-time progress updates displayed during execution
- **Log Files**: Detailed logs saved to `logs/collection_YYYY-MM-DD_HH-MM-SS.log`
- **Summary Reports**: JSON summary saved after each run in `logs/latest_summary.json`
- **GitHub Actions Artifacts**: In automated runs, logs are uploaded as artifacts and retained for 30 days

Log files include:
- Timestamp for each operation
- Download progress and file sizes
- Julia analysis details (image loading, blob detection count, moon phase)
- Success/failure statistics
- Error messages with full stack traces when issues occur

## Data Sources

The project scrapes images from over **240+ astronomical and sky observation sources** worldwide, organized into the following categories:

### 1. Original Sources (2 sources)
- **Barnard Astronomical Society:** A static URL pointing to the latest all-sky camera image.
- **weatherUSA SkyCam Network:** Scrapes specific camera pages to find the latest image URL.

### 2. All-Sky Observatory Cameras (41 sources)
Professional observatory all-sky cameras including:
- Major observatories: ESO (Paranal, La Silla), Gemini North/South, CFHT, Subaru, UKIRT, IRTF
- International facilities: IAC Tenerife, TUG Turkey, KPNO, Lowell Observatory, McDonald Observatory
- European observatories: Calar Alto, TNG, NOT, Mercator, Liverpool Telescope, WHT, INT
- Southern hemisphere: AAO, Siding Spring, SAAO, SALT, SONEAR
- And many more professional observatories worldwide

### 3. University Observatory Cameras (45 sources)
University and educational institution observatories including:
- **USA:** University of Arizona, UC Berkeley, Yale, Caltech, MIT, Chicago, Cornell, Michigan, Texas, Hawaii, Colorado, Penn State, Washington
- **Europe:** Oxford, Cambridge, Edinburgh, Leiden, Amsterdam, Munich, Heidelberg, Paris, Bologna, Padova, Madrid, Barcelona, Valencia, Warsaw, Prague, Vienna, Stockholm, Oslo, Copenhagen
- **Asia-Pacific:** University of Tokyo, Kyoto, Beijing, Nanjing, Sydney, Melbourne, ANU

### 4. Weather Station SkyCams (20 sources)
WeatherUSA SkyCam network cameras across major US cities including:
- Columbus, Cleveland, Indianapolis, Detroit, Chicago, Pittsburgh, New York, Boston
- Miami, Houston, Los Angeles, Seattle, Phoenix, Denver, Las Vegas
- Atlanta, Charlotte, Nashville, St. Louis, Minneapolis

### 5. Aurora and Northern Lights Cameras (35 sources)
Dedicated aurora observation cameras including:
- **Alaska:** Fairbanks GI, Poker Flat, Anchorage, Juneau, Nome, Barrow
- **Canada:** AuroraMAX Yellowknife, Churchill, Gillam, Fort Smith, Edmonton, Calgary, Athabasca
- **Scandinavia:** Kiruna IRF, Abisko, Tromsø, Longyearbyen, Sodankylä, Kilpisjärvi, Ivalo, Muonio, Levi, Kevo
- **Iceland:** Reykjavik, Akureyri
- **Russia:** Murmansk, Apatity
- **Greenland:** Kangerlussuaq, Qaanaaq
- **Antarctica:** South Pole, McMurdo, Mawson, Davis (Aurora Australis)

### 6. Meteor Detection Cameras (32 sources)
Fireball and meteor surveillance cameras including:
- **Global Meteor Network:** Stations in Croatia, USA, Australia, Canada, UK
- **NASA All-Sky Fireball Network:** Huntsville, Tullahoma, Dahlonega, Oberlin, Clouds Rest
- **CAMS (Cameras for Allsky Meteor Surveillance):** Bay Area, BeNeLux, Florida, Texas
- **IMO Video Network:** Croatia, Germany, France, Italy
- **UK Meteor Network:** Edinburgh, London, Manchester, Oxford, Bristol
- **Australia Meteor Network:** Canberra, Sydney, Melbourne, Brisbane, Perth
- **SonotaCo Network (Japan):** Tokyo, Osaka, Nagoya

### 7. Space Weather and Solar Monitoring Cameras (31 sources)
Solar observation and space weather monitoring including:
- **NOAA:** LASCO C2/C3 Coronagraph, SUVI Solar Imager, Aurora forecasts
- **NASA SDO:** Multiple wavelengths (193Å, 211Å, 304Å, 171Å, 131Å, 335Å, 094Å), HMI Continuum/Magnetogram
- **SOHO:** EIT multiple wavelengths, MDI Magnetogram
- **STEREO:** EUVI observations
- **Hinode:** X-Ray Telescope, Solar Optical Telescope
- **Ground-based Solar:** NSO GONG H-alpha and Magnetogram, Kanzelhöhe, Big Bear, Catania, Mees Observatory
- **Atmospheric:** Lidar, Airglow imagers, Noctilucent cloud monitors

### 8. Miscellaneous Sky Cameras (40 sources)
Additional specialized cameras including:
- **Dark Sky Preserves:** Cherry Springs, Jasper, Galloway Forest, Brecon Beacons, Exmoor
- **Radio Astronomy:** Arecibo, Parkes, Jodrell Bank, Effelsberg, VLA, ALMA
- **Planetariums:** Griffith Observatory, Adler Planetarium, Hayden Planetarium, Franklin Institute
- **Amateur Astronomy Clubs:** Worldwide locations in Australia, New Zealand, South America
- **Research Stations:** Antarctica (Concordia, Halley, Syowa, Zhongshan), Greenland Summit Camp
- **Mountain Observatories:** Wendelstein, Jungfraujoch, Sphinx, Teide, Roque de los Muchachos
- **Island Observatories:** Haleakala, Tenerife, La Réunion, Madeira, Azores
- **Radio Sky Monitoring:** GRAVES radar (France), BRAMS (Belgium)

### Total: 246 Sky Observation Sources

Each scraper automatically attempts to download the latest image from these sources, processes them through astronomical image analysis, and stores the results with metadata and timestamps. The system is designed to be robust, with error handling and retry logic to handle network issues and unavailable sources.

## How to Run Manually

1.  **Install Dependencies:**
    - Python 3.10+
    - Julia 1.6+
    - Install Python packages: `pip install -r src/python/requirements.txt`
    - Install Julia packages: `julia -e 'using Pkg; Pkg.add("JSON"); Pkg.add("Images"); Pkg.add("BlobTracking"); Pkg.add("AstroLib")'`

2.  **Run the Script:**
    - Execute the main orchestrator from the root of the project. You need to set the `PYTHONPATH` to include the project root so that the scrapers can be found.
      ```bash
      PYTHONPATH=. python src/python/main.py
      ```

## Automation via GitHub Actions

The project is configured to run automatically every 30 minutes using the GitHub Action defined in `.github/workflows/collect_data.yml`. It will commit and push any new data it collects directly to the `data/` directory in this repository.

### Accessing Logs

When running via GitHub Actions:
1. Go to the "Actions" tab in the repository
2. Click on a workflow run
3. Download the "collection-logs" artifact to view detailed logs

## Troubleshooting

### Common Issues

**Julia MethodError with blob_LoG**: Ensure you're using the correct function signature with the scale parameter:
```julia
σscales = 1:10
blobs = blob_LoG(img_gray, σscales, rthresh=0.1)
```

**Network Errors**: The scrapers include 30-second timeouts and retry logic. Check the logs for detailed error messages.

**Missing Dependencies**: Make sure all Python and Julia packages are installed as described in the setup instructions.
