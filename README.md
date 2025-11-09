# Automated Astronomical Data Collector

This project automatically collects astronomical images from open APIs, analyzes them using Python and Julia, and stores the data in this repository. The goal is to build a large dataset of the sky over time for change analysis.

## Project Structure

- `src/python/main.py`: The main orchestrator script that fetches data, runs the analysis, and saves the results.
- `src/julia/analyze.jl`: The Julia script that performs image analysis.
- `data/`: The directory where the collected data is stored.
- `.github/workflows/collect_data.yml`: The GitHub Actions workflow that automates the data collection process.

## How to Run Manually

1.  **Install Dependencies:**
    - Python 3.10+
    - Julia 1.6+
    - `pip install -r src/python/requirements.txt`
    - `julia -e 'using Pkg; Pkg.add("JSON")'`

2.  **Set Environment Variables:**
    - Export your NASA API key: `export NASA_API_KEY="YOUR_API_KEY"`

3.  **Run the Script:**
    - `python src/python/main.py`

## GitHub Actions

This project uses GitHub Actions to automate the data collection process. The workflow is defined in `.github/workflows/collect_data.yml` and runs every 30 minutes.

### Setting up the `NASA_API_KEY` Secret

For the GitHub Action to work, you need to add your NASA API key as a secret to your GitHub repository.

1.  Go to your repository's **Settings**.
2.  In the left sidebar, click **Secrets and variables**, then **Actions**.
3.  Click **New repository secret**.
4.  Name the secret `NASA_API_KEY`.
5.  Paste your API key into the value field.
6.  Click **Add secret**.
