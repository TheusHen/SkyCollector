import os
import subprocess
import json
import gzip
from datetime import datetime
import importlib

# Import scrapers
from scrapers import barnard_scraper, weatherusa_scraper

SCRAPERS = [
    barnard_scraper,
    weatherusa_scraper
]

def analyze_image(image_path):
    """Invokes the Julia script to analyze an image."""
    julia_script_path = "src/julia/analyze.jl"
    print(f"Invoking Julia script: {julia_script_path}")
    result = subprocess.run(["julia", julia_script_path, image_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running Julia script: {result.stderr}")
        return None

    return json.loads(result.stdout)

def main():
    """Main function to orchestrate the data collection process."""
    for scraper in SCRAPERS:
        try:
            image_path, metadata = scraper.scrape()

            if not image_path:
                continue

            analysis_data = analyze_image(image_path)

            if not analysis_data:
                os.remove(image_path)
                continue

            # Combine metadata with analysis data
            combined_data = {
                "metadata": metadata,
                "analysis": analysis_data
            }

            # Create directory structure and save the results
            source_name = metadata.get("source", "unknown")
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

            output_dir = os.path.join("data", source_name)
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"{timestamp}.json.gz")

            print(f"Saving data to {output_path}")
            with gzip.open(output_path, "wt", encoding="UTF-8") as f:
                json.dump(combined_data, f)

            # Clean up the downloaded image
            os.remove(image_path)
        except Exception as e:
            print(f"Error processing scraper {scraper.SOURCE_NAME}: {e}")
            continue

    print("Orchestration complete.")

if __name__ == "__main__":
    main()
