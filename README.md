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
