# Automated Astronomical Data Collector (Scraping Edition)

This project automatically collects astronomical images from public webcams via web scraping, analyzes them using a combination of Python and Julia, and stores the resulting data in this repository. The goal is to build a large, timestamped dataset of the sky from various sources over time.

This version is completely free of API keys and relies on scraping public websites.

## Project Structure

- `src/python/main.py`: The main orchestrator script that runs the scrapers, invokes the analysis, and saves the results.
- `src/julia/analyze.jl`: The Julia script that performs image analysis, including star detection and moon phase calculation.
- `scrapers/`: A Python package containing individual modules for scraping each data source.
- `data/`: The directory where the collected and compressed (`.json.gz`) data is stored, organized by source.
- `.github/workflows/collect_data.yml`: The GitHub Actions workflow that automates the entire process.

## Data Sources

Currently, the project scrapes images from the following sources:

1.  **Barnard Astronomical Society:** A static URL pointing to the latest all-sky camera image.
2.  **weatherUSA SkyCam Network:** Scrapes specific camera pages to find the latest image URL.

## How to Run Manually

1.  **Install Dependencies:**
    - Python 3.10+
    - Julia 1.6+
    - Install Python packages: `pip install -r src/python/requirements.txt`
    - Install Julia packages: `julia -e 'using Pkg; Pkg.add("JSON"); Pkg.add("Images"); Pkg.add("BlobTracking"); Pkg.add("AstroLib")'`

2.  **Run the Script:**
    - Execute the main orchestrator from the root of the project:
      ```bash
      python src/python/main.py
      ```

## Automation via GitHub Actions

The project is configured to run automatically every 30 minutes using the GitHub Action defined in `.github/workflows/collect_data.yml`. It will commit and push any new data it collects directly to the `data/` directory in this repository.
