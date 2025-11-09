import os
import subprocess
import json
import gzip
from datetime import datetime
import importlib
import sys
import logging

# Configure logging with both console and file output
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"collection_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Create formatters
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configure root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info(f"Logging to file: {log_file}")

# Import scrapers
from scrapers import (
    barnard_scraper, 
    weatherusa_scraper,
    allsky_cameras,
    university_observatories,
    weather_skycams,
    aurora_cameras,
    meteor_cameras,
    spaceweather_cameras,
    misc_skycams
)

SCRAPERS = [
    barnard_scraper,
    weatherusa_scraper,
    allsky_cameras,
    university_observatories,
    weather_skycams,
    aurora_cameras,
    meteor_cameras,
    spaceweather_cameras,
    misc_skycams
]

def analyze_image(image_path):
    """Invokes the Julia script to analyze an image."""
    julia_script_path = "src/julia/analyze.jl"
    logger.info(f"Invoking Julia script: {julia_script_path}")
    logger.info(f"Analyzing image: {image_path}")
    
    try:
        result = subprocess.run(
            ["julia", julia_script_path, image_path], 
            capture_output=True, 
            text=True,
            timeout=60  # 60 second timeout
        )
        
        # Log Julia stderr output (which contains our logging messages)
        if result.stderr:
            for line in result.stderr.strip().split('\n'):
                if line:
                    logger.info(f"Julia: {line}")

        if result.returncode != 0:
            logger.error(f"Julia script failed with return code {result.returncode}")
            logger.error(f"Julia stderr: {result.stderr}")
            logger.error(f"Julia stdout: {result.stdout}")
            return None

        logger.info("Julia analysis completed successfully")
        return json.loads(result.stdout)
        
    except subprocess.TimeoutExpired:
        logger.error(f"Julia script timed out after 60 seconds")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Julia output as JSON: {e}")
        logger.error(f"Julia stdout: {result.stdout}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error running Julia script: {e}")
        return None

def main():
    """Main function to orchestrate the data collection process."""
    logger.info("="*60)
    logger.info("Starting astronomical data collection")
    logger.info("="*60)
    
    successful_collections = 0
    failed_collections = 0
    
    for scraper in SCRAPERS:
        scraper_name = scraper.SOURCE_NAME
        logger.info(f"Processing scraper: {scraper_name}")
        
        try:
            image_path, metadata = scraper.scrape()

            if not image_path:
                logger.warning(f"Scraper {scraper_name} did not return an image path")
                failed_collections += 1
                continue

            logger.info(f"Image downloaded successfully: {image_path}")
            
            analysis_data = analyze_image(image_path)

            if not analysis_data:
                logger.error(f"Analysis failed for {scraper_name}, removing image")
                if os.path.exists(image_path):
                    os.remove(image_path)
                failed_collections += 1
                continue

            # Combine metadata with analysis data
            combined_data = {
                "metadata": metadata,
                "analysis": analysis_data,
                "timestamp": datetime.now().isoformat()
            }

            # Create directory structure and save the results
            source_name = metadata.get("source", "unknown")
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

            output_dir = os.path.join("data", source_name)
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"{timestamp}.json.gz")

            logger.info(f"Saving data to {output_path}")
            with gzip.open(output_path, "wt", encoding="UTF-8") as f:
                json.dump(combined_data, f, indent=2)

            logger.info(f"Data saved successfully, stars detected: {len(analysis_data.get('stars', []))}")
            
            # Clean up the downloaded image
            if os.path.exists(image_path):
                os.remove(image_path)
                logger.info(f"Cleaned up temporary image: {image_path}")
                
            successful_collections += 1
            
        except Exception as e:
            logger.error(f"Error processing scraper {scraper_name}: {e}", exc_info=True)
            failed_collections += 1
            continue

    logger.info("="*60)
    logger.info(f"Data collection complete")
    logger.info(f"Successful: {successful_collections}, Failed: {failed_collections}")
    logger.info(f"Log file saved to: {log_file}")
    logger.info("="*60)
    
    # Save a summary report
    summary_dir = "logs"
    summary_file = os.path.join(summary_dir, "latest_summary.json")
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "successful_collections": successful_collections,
        "failed_collections": failed_collections,
        "total_scrapers": len(SCRAPERS),
        "log_file": log_file
    }
    
    try:
        with open(summary_file, "w") as f:
            json.dump(summary_data, f, indent=2)
        logger.info(f"Summary saved to: {summary_file}")
    except Exception as e:
        logger.error(f"Failed to save summary: {e}")

if __name__ == "__main__":
    main()
