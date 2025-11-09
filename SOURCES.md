# Complete List of Sky Camera Sources

This document provides a comprehensive list of all 246 sky camera sources included in the SkyCollector project.

## Summary Statistics

| Category | Count | Description |
|----------|-------|-------------|
| Original Sources | 2 | Legacy scrapers from initial implementation |
| All-Sky Observatory Cameras | 41 | Professional observatory all-sky cameras |
| University Observatory Cameras | 45 | Educational institution observatories |
| Weather Station SkyCams | 20 | WeatherUSA network cameras |
| Aurora Cameras | 35 | Northern/Southern lights monitoring |
| Meteor Detection Cameras | 32 | Fireball and meteor surveillance |
| Space Weather Cameras | 31 | Solar and space weather monitoring |
| Miscellaneous SkyCams | 40 | Specialized and amateur cameras |
| **TOTAL** | **246** | **Total camera sources** |

---

## 1. Original Sources (2 sources)

### barnard_scraper.py
- **Barnard Astronomical Society**
  - URL: http://barnardstar.org/AllSky/image.jpg
  - Location: USA
  - Description: All-sky camera from Barnard Astronomical Society

### weatherusa_scraper.py
- **WeatherUSA Columbus SkyCam**
  - URL: https://www.weatherusa.net/skycamnet/index.php?cam=OHCMH1
  - Location: Columbus, Ohio, USA
  - Description: Weather station sky camera (scraped)

---

## 2. All-Sky Observatory Cameras (41 sources)

### scrapers/allsky_cameras.py

1. **Instituto de Astrofísica de Canarias** - Tenerife, Spain
2. **MTO South Australia** - Campbell town, Australia
3. **Las Campanas Observatory** - Chile
4. **Lowell Observatory** - Arizona, USA
5. **TÜBİTAK National Observatory** - Turkey
6. **New Mexico State University Observatory** - New Mexico, USA
7. **Kitt Peak National Observatory** - Arizona, USA
8. **ESO Paranal Observatory** - Chile
9. **ESO La Silla Observatory** - Chile
10. **Mauna Kea Weather Center** - Hawaii, USA
11. **Canada-France-Hawaii Telescope** - Hawaii, USA
12. **Gemini North Observatory** - Hawaii, USA
13. **Gemini South Observatory** - Chile
14. **Subaru Telescope** - Hawaii, USA
15. **Astroport Sabadell** - Spain
16. **Observatoire de Haute-Provence** - France
17. **Pic du Midi Observatory** - France
18. **UK Infrared Telescope** - Hawaii, USA
19. **NASA Infrared Telescope Facility** - Hawaii, USA
20. **Magdalena Ridge Observatory** - New Mexico, USA
21. **Anglo-Australian Observatory** - Australia
22. **Siding Spring Observatory** - Australia
23. **South African Astronomical Observatory** - South Africa
24. **Southern African Large Telescope** - South Africa
25. **SONEAR Observatory** - Brazil
26. **Green Bank Observatory** - West Virginia, USA
27. **Sky Quality Meter Network** - Rome, Italy
28. **Sterrekunst Observatory** - Belgium
29. **Skinakas Observatory** - Crete, Greece
30. **Helmos Observatory** - Greece
31. **Tartu Observatory** - Estonia
32. **Tuorla Observatory** - Finland
33. **Cagliari Astronomical Observatory** - Italy
34. **University of Cadiz Observatory** - Spain
35. **Calar Alto Observatory** - Spain
36. **Telescopio Nazionale Galileo** - La Palma, Spain
37. **Nordic Optical Telescope** - La Palma, Spain
38. **Mercator Telescope** - La Palma, Spain
39. **Liverpool Telescope** - La Palma, Spain
40. **Isaac Newton Telescope** - La Palma, Spain
41. **William Herschel Telescope** - La Palma, Spain

---

## 3. University Observatory Cameras (45 sources)

### scrapers/university_observatories.py

**USA Universities (15 sources):**
1. University of Arizona Steward Observatory
2. UC Berkeley Leuschner Observatory
3. Yale SMARTS Consortium
4. Caltech Palomar Observatory
5. MIT Haystack Observatory
6. University of Chicago Observatory
7. Indiana University Morgan Observatory
8. Cornell University Observatory
9. University of Wisconsin Observatory
10. University of Michigan Observatory
11. McDonald Observatory, University of Texas
12. University of Hawaii Institute for Astronomy
13. University of Colorado Sommers-Bausch Observatory
14. Penn State Observatory
15. University of Washington Observatory

**European Universities (25 sources):**
16. University of Oxford Observatory - UK
17. University of Cambridge Observatory - UK
18. University of Edinburgh Royal Observatory - UK
19. Leiden Observatory - Netherlands
20. University of Amsterdam Observatory - Netherlands
21. Ludwig Maximilian University Munich - Germany
22. Heidelberg University Observatory - Germany
23. Institut d'Astrophysique de Paris - France
24. Toulouse Observatory - France
25. University of Bologna Observatory - Italy
26. Padova Observatory - Italy
27. Complutense University of Madrid - Spain
28. University of Barcelona Observatory - Spain
29. University of Valencia Observatory - Spain
30. Lisbon Astronomical Observatory - Portugal
31. Warsaw University Observatory - Poland
32. Jagiellonian University - Krakow, Poland
33. Charles University - Prague, Czech Republic
34. Konkoly Observatory - Budapest, Hungary
35. University of Vienna Observatory - Austria
36. Stockholm University Observatory - Sweden
37. University of Oslo Observatory - Norway
38. University of Copenhagen Observatory - Denmark

**Asia-Pacific Universities (5 sources):**
39. University of Tokyo Observatory - Japan
40. Kyoto University Observatory - Japan
41. Peking University Observatory - China
42. Nanjing University Observatory - China
43. University of Sydney Observatory - Australia
44. Swinburne University - Melbourne, Australia
45. Australian National University Observatory - Australia

---

## 4. Weather Station SkyCams (20 sources)

### scrapers/weather_skycams.py

All from WeatherUSA SkyCam Network:
1. Columbus, Ohio
2. Cleveland, Ohio
3. Indianapolis, Indiana
4. Detroit, Michigan
5. Chicago, Illinois
6. Pittsburgh, Pennsylvania
7. New York, New York
8. Boston, Massachusetts
9. Miami, Florida
10. Houston, Texas
11. Los Angeles, California
12. Seattle, Washington
13. Phoenix, Arizona
14. Denver, Colorado
15. Las Vegas, Nevada
16. Atlanta, Georgia
17. Charlotte, North Carolina
18. Nashville, Tennessee
19. St. Louis, Missouri
20. Minneapolis, Minnesota

---

## 5. Aurora Cameras (35 sources)

### scrapers/aurora_cameras.py

**Alaska (6 sources):**
1. Geophysical Institute, Fairbanks
2. Poker Flat Research Range
3. Anchorage Aurora Camera
4. Juneau Aurora Camera
5. Nome Aurora Camera
6. Barrow Aurora Camera

**Canada (9 sources):**
7. AuroraMAX Yellowknife
8. Whitehorse, Yukon
9. Churchill, Manitoba
10. Gillam, Manitoba
11. Fort Smith, NWT
12. Fort McMurray, Alberta
13. Edmonton, Alberta
14. Calgary, Alberta
15. Athabasca, Alberta

**Scandinavia (10 sources):**
16. Swedish Institute of Space Physics, Kiruna
17. Abisko, Sweden Aurora Station
18. Tromsø, Norway
19. Longyearbyen, Svalbard
20. Sodankylä Geophysical Observatory, Finland
21. Kilpisjärvi, Finland
22. Ivalo, Finland
23. Muonio, Finland
24. Levi, Finland
25. Kevo, Finland

**Iceland (2 sources):**
26. Reykjavik, Iceland
27. Akureyri, Iceland

**Russia (2 sources):**
28. Murmansk, Russia
29. Apatity, Russia

**Greenland (2 sources):**
30. Kangerlussuaq, Greenland
31. Qaanaaq, Greenland

**Antarctica - Aurora Australis (4 sources):**
32. South Pole Station
33. McMurdo Station
34. Mawson Station
35. Davis Station

---

## 6. Meteor Detection Cameras (32 sources)

### scrapers/meteor_cameras.py

**Global Meteor Network (5 sources):**
1. Croatia Station 1
2. USA Station 1
3. Australia Station 1
4. Canada Station 1
5. UK Station 1

**NASA All-Sky Fireball Network (5 sources):**
6. Huntsville, Alabama
7. Tullahoma, Tennessee
8. Dahlonega, Georgia
9. Oberlin, Ohio
10. Clouds Rest, California

**CAMS - Cameras for Allsky Meteor Surveillance (5 sources):**
11. Bay Area Station 1
12. Bay Area Station 2
13. BeNeLux Station 1
14. Florida Station 1
15. Texas Station 1

**IMO Video Network (4 sources):**
16. Croatia
17. Germany
18. France
19. Italy

**UK Meteor Network (5 sources):**
20. Edinburgh
21. London
22. Manchester
23. Oxford
24. Bristol

**Australia Meteor Network (5 sources):**
25. Canberra
26. Sydney
27. Melbourne
28. Brisbane
29. Perth

**SonotaCo Network - Japan (3 sources):**
30. Tokyo
31. Osaka
32. Nagoya

---

## 7. Space Weather Cameras (31 sources)

### scrapers/spaceweather_cameras.py

**NOAA Space Weather Prediction Center (5 sources):**
1. LASCO C2 Coronagraph
2. LASCO C3 Coronagraph
3. Solar Ultraviolet Imager
4. Aurora Northern Hemisphere
5. Aurora Southern Hemisphere

**NASA Solar Dynamics Observatory (9 sources):**
6. AIA 193 Å
7. AIA 211 Å
8. AIA 304 Å
9. AIA 171 Å
10. AIA 131 Å
11. AIA 335 Å
12. AIA 094 Å
13. HMI Continuum
14. HMI Magnetogram

**SOHO - Solar and Heliospheric Observatory (4 sources):**
15. EIT 195 Å
16. EIT 284 Å
17. EIT 304 Å
18. MDI Magnetogram

**STEREO (2 sources):**
19. STEREO-A EUVI 195 Å
20. STEREO-B EUVI 195 Å

**Hinode Solar Telescope - Japan (2 sources):**
21. X-Ray Telescope
22. Solar Optical Telescope

**Ground-based Solar Observatories (6 sources):**
23. NSO GONG H-alpha
24. NSO GONG Magnetogram
25. Kanzelhöhe Solar Observatory H-alpha
26. Big Bear Solar Observatory H-alpha
27. Catania Astrophysical Observatory
28. Mees Solar Observatory H-alpha

**Atmospheric Monitoring (3 sources):**
29. DMI Lidar, Greenland
30. Airglow Imager, Pisgah Observatory
31. Noctilucent Clouds Monitor

---

## 8. Miscellaneous SkyCams (40 sources)

### scrapers/misc_skycams.py

**Dark Sky Preserves (5 sources):**
1. Cherry Springs State Park, Pennsylvania
2. Jasper Dark Sky Preserve, Canada
3. Galloway Forest Dark Sky Park, UK
4. Brecon Beacons Dark Sky Reserve, Wales
5. Exmoor Dark Sky Reserve, UK

**Radio Astronomy Observatories (6 sources):**
6. Arecibo Observatory, Puerto Rico
7. Parkes Observatory, Australia
8. Jodrell Bank Observatory, UK
9. Effelsberg Radio Observatory, Germany
10. Very Large Array, New Mexico
11. ALMA Observatory, Chile

**Planetariums and Science Centers (4 sources):**
12. Griffith Observatory, Los Angeles
13. Adler Planetarium, Chicago
14. Hayden Planetarium, New York
15. Franklin Institute, Philadelphia

**Amateur Astronomy Clubs (8 sources):**
16. Canberra Astronomical Society, Australia
17. Perth Observatory, Australia
18. Auckland Observatory, New Zealand
19. Christchurch Astronomical Society, New Zealand
20. Buenos Aires Observatory, Argentina
21. Santiago Astronomical Society, Chile
22. Bogota Astronomical Observatory, Colombia
23. Mexico City Astronomical Society, Mexico

**Research Stations and Remote Locations (5 sources):**
24. Concordia Station, Antarctica
25. Summit Camp, Greenland
26. Halley Research Station, Antarctica
27. Syowa Station, Antarctica
28. Zhongshan Station, Antarctica

**Mountain Observatories (5 sources):**
29. Wendelstein Observatory, Germany
30. Jungfraujoch High Altitude Station, Switzerland
31. Sphinx Observatory, Switzerland
32. Teide Observatory, Canary Islands
33. Roque de los Muchachos, La Palma

**Island Observatories (5 sources):**
34. Haleakala Observatory, Maui
35. Teide Observatory, Tenerife
36. La Réunion Observatory
37. Madeira Observatory
38. Azores Observatory

**Radio Sky Monitoring (2 sources):**
39. GRAVES Radar Meteor Scatter, France
40. BRAMS Meteor Network, Belgium

---

## Usage Notes

### Testing Sources
Use the provided verification script to test which sources are currently active:

```bash
# Test all sources
PYTHONPATH=. python verify_scrapers.py --verbose

# Test specific category
PYTHONPATH=. python verify_scrapers.py --category aurora --verbose

# Quick test with shorter timeout
PYTHONPATH=. python verify_scrapers.py --timeout 5
```

### Expected Availability
Not all sources will be available at all times due to:
- Maintenance windows
- Camera malfunctions
- Network issues
- Websites being restructured or moved
- Observatories going offline

The system is designed to gracefully handle failures and continue with available sources.

### Adding New Sources
To add new sources:
1. Add the camera information to the appropriate list in the scraper module
2. Follow the existing format with `name`, `url`, and `description` fields
3. Test the new source with the verification script
4. Update this documentation

---

## Geographic Distribution

### By Continent:
- **North America:** ~90 sources (USA, Canada, Mexico)
- **Europe:** ~70 sources (UK, Spain, France, Germany, Scandinavia, etc.)
- **Asia:** ~15 sources (Japan, China, Turkey, Middle East)
- **South America:** ~10 sources (Chile, Brazil, Argentina)
- **Oceania:** ~25 sources (Australia, New Zealand)
- **Antarctica:** ~10 sources (Various research stations)
- **Space-based:** ~20 sources (Satellites, solar observatories)

### By Observatory Type:
- **Professional Observatories:** ~80 sources
- **University/Educational:** ~45 sources
- **Amateur/Community:** ~25 sources
- **Weather Stations:** ~20 sources
- **Research Stations:** ~15 sources
- **Space Weather/Solar:** ~30 sources
- **Specialized (Aurora, Meteor):** ~70 sources

---

*Last Updated: 2025-11-09*
*Total Sources: 246*
