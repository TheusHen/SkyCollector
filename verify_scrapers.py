#!/usr/bin/env python3
"""
Verification script to test scraper sources.

This script tests each camera source to verify that images can be downloaded.
It provides a summary of working vs. non-working sources.

Usage:
    PYTHONPATH=. python verify_scrapers.py [--category CATEGORY] [--verbose]

Options:
    --category CATEGORY  Test only scrapers from a specific category
                        (allsky, university, weather, aurora, meteor, spaceweather, misc)
    --verbose           Show detailed output for each source
    --timeout SECONDS   Timeout for each request (default: 10)
"""

import sys
import argparse
import requests
from datetime import datetime

# Import all scraper modules
from scrapers import (
    allsky_cameras,
    university_observatories,
    weather_skycams,
    aurora_cameras,
    meteor_cameras,
    spaceweather_cameras,
    misc_skycams
)

# Map category names to modules
CATEGORIES = {
    'allsky': ('All-Sky Cameras', allsky_cameras.ALLSKY_CAMERAS),
    'university': ('University Observatories', university_observatories.UNIVERSITY_CAMERAS),
    'weather': ('Weather SkyCams', weather_skycams.WEATHER_SKYCAMS),
    'aurora': ('Aurora Cameras', aurora_cameras.AURORA_CAMERAS),
    'meteor': ('Meteor Detection Cameras', meteor_cameras.METEOR_CAMERAS),
    'spaceweather': ('Space Weather Cameras', spaceweather_cameras.SPACE_WEATHER_CAMERAS),
    'misc': ('Miscellaneous SkyCams', misc_skycams.MISC_SKYCAMS)
}

def test_camera(camera_info, timeout=10, verbose=False):
    """
    Test if a camera URL returns a valid response.
    
    Returns: (success: bool, status_code: int, size_bytes: int, error_msg: str)
    """
    name = camera_info.get("name", "unknown")
    url = camera_info.get("url", "")
    
    if not url:
        return False, 0, 0, "No URL provided"
    
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        status_code = response.status_code
        
        # If HEAD request successful, try GET to confirm image data
        if status_code == 200:
            response = requests.get(url, timeout=timeout, stream=True)
            content_length = int(response.headers.get('content-length', 0))
            
            # Read first 1KB to verify it's image-like data
            chunk = next(response.iter_content(1024), b'')
            
            if len(chunk) > 0:
                if verbose:
                    print(f"  ✓ {name}: {status_code}, {content_length} bytes")
                return True, status_code, content_length, ""
            else:
                if verbose:
                    print(f"  ✗ {name}: Empty response")
                return False, status_code, 0, "Empty response"
        else:
            if verbose:
                print(f"  ✗ {name}: HTTP {status_code}")
            return False, status_code, 0, f"HTTP {status_code}"
            
    except requests.exceptions.Timeout:
        if verbose:
            print(f"  ✗ {name}: Timeout after {timeout}s")
        return False, 0, 0, f"Timeout after {timeout}s"
    except requests.exceptions.RequestException as e:
        error_msg = str(e)[:100]  # Limit error message length
        if verbose:
            print(f"  ✗ {name}: {error_msg}")
        return False, 0, 0, error_msg

def main():
    parser = argparse.ArgumentParser(description='Verify scraper sources')
    parser.add_argument('--category', choices=list(CATEGORIES.keys()),
                       help='Test only scrapers from a specific category')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output for each source')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Timeout for each request in seconds (default: 10)')
    
    args = parser.parse_args()
    
    print("="*70)
    print(f"Sky Camera Scraper Verification - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()
    
    # Select categories to test
    if args.category:
        categories_to_test = {args.category: CATEGORIES[args.category]}
    else:
        categories_to_test = CATEGORIES
    
    total_tested = 0
    total_working = 0
    total_failed = 0
    
    results_by_category = {}
    
    for cat_key, (cat_name, cameras) in categories_to_test.items():
        print(f"Testing {cat_name} ({len(cameras)} sources)...")
        if args.verbose:
            print()
        
        working = 0
        failed = 0
        failed_sources = []
        
        for camera in cameras:
            success, status, size, error = test_camera(camera, args.timeout, args.verbose)
            
            if success:
                working += 1
            else:
                failed += 1
                failed_sources.append({
                    'name': camera.get('name', 'unknown'),
                    'url': camera.get('url', ''),
                    'error': error
                })
            
            total_tested += 1
        
        total_working += working
        total_failed += failed
        
        results_by_category[cat_name] = {
            'total': len(cameras),
            'working': working,
            'failed': failed,
            'failed_sources': failed_sources
        }
        
        if not args.verbose:
            print(f"  ✓ Working: {working}, ✗ Failed: {failed}")
        print()
    
    # Print summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    
    for cat_name, results in results_by_category.items():
        percentage = (results['working'] / results['total'] * 100) if results['total'] > 0 else 0
        print(f"{cat_name:.<40} {results['working']:>3}/{results['total']:<3} ({percentage:>5.1f}%)")
    
    print("-"*70)
    total_percentage = (total_working / total_tested * 100) if total_tested > 0 else 0
    print(f"{'TOTAL':.<40} {total_working:>3}/{total_tested:<3} ({total_percentage:>5.1f}%)")
    print("="*70)
    
    # Print failed sources if verbose
    if args.verbose and total_failed > 0:
        print()
        print("FAILED SOURCES:")
        print("-"*70)
        for cat_name, results in results_by_category.items():
            if results['failed_sources']:
                print(f"\n{cat_name}:")
                for failed in results['failed_sources']:
                    print(f"  • {failed['name']}")
                    print(f"    URL: {failed['url']}")
                    print(f"    Error: {failed['error']}")
    
    # Exit with error code if too many failures
    if total_percentage < 50:
        print(f"\n⚠ WARNING: Less than 50% of sources are working!")
        sys.exit(1)
    elif total_percentage < 80:
        print(f"\n⚠ NOTICE: {total_percentage:.1f}% of sources are working.")
        sys.exit(0)
    else:
        print(f"\n✓ SUCCESS: {total_percentage:.1f}% of sources are working!")
        sys.exit(0)

if __name__ == "__main__":
    main()
