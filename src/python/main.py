import os
import requests
import subprocess
import json
import gzip
from datetime import datetime

def get_apod_data(api_key):
    """Fetches data from NASA's APOD API."""
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def main():
    """Main function to orchestrate the data collection process."""
    api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")

    print("Fetching APOD data...")
    apod_data = get_apod_data(api_key)

    image_url = apod_data.get("hdurl") or apod_data.get("url")
    if not image_url:
        print("No image URL found in APOD data.")
        return

    print(f"Downloading image from {image_url}")
    response = requests.get(image_url)
    response.raise_for_status()

    # Create a temporary directory for the image
    os.makedirs("tmp", exist_ok=True)
    image_path = os.path.join("tmp", os.path.basename(image_url))
    with open(image_path, "wb") as f:
        f.write(response.content)

    # Invoke Julia script for analysis
    julia_script_path = "src/julia/analyze.jl"
    print(f"Invoking Julia script: {julia_script_path}")
    result = subprocess.run(["julia", julia_script_path, image_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running Julia script: {result.stderr}")
        return

    analysis_data = json.loads(result.stdout)

    # Combine APOD metadata with analysis data
    combined_data = {
        "apod_metadata": apod_data,
        "analysis": analysis_data
    }

    # Create directory structure and save the results
    country = "USA" # Placeholder, as APOD is US-based
    coordinates = "space" # Placeholder
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    output_dir = os.path.join("data", country, coordinates)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}.json.gz")

    print(f"Saving data to {output_path}")
    with gzip.open(output_path, "wt", encoding="UTF-8") as f:
        json.dump(combined_data, f)

    # Clean up the downloaded image
    os.remove(image_path)

    print("Orchestration complete.")

if __name__ == "__main__":
    main()
