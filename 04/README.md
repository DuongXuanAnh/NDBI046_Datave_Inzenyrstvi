# Fourth Assignment
Employ SKOS to enhance your data.

Add skos:prefLabel to Regions / Districts.
Create SKOS hierarchy for Regions and Districts.

Create DCAT dataset entry (dcat:Dataset) for one data cube.

- Save the dataset entry into another file.
- Properties / scope as shown on lectures.
- Dataset: label, description, distribution, accrualPeriodicity, publisher (you), spatial, keywords, themes.
Distribution: accessURL, mediaType
- Remember to employ your prefix (base URL).
- Employ resources from:
    - Authority tables : Frequencies, File types, Countries
    - Eurovoc themes.

Note: As the Authority tables links are redirected to HTTP, you can no open them from this site as it uses HTTPS. You need to copy the link and open it a new tab/window.

# System requirements
- Python3 (>=3.10)
- Modules in requirements.txt
- Internet connection (to download dependencies and datasets)
# Installation instructions
- Clone repository
- pip install .
- Run the program
  - careProviders.py -> output/CareProvides.ttl
  - DCAT_dataset.py -> output/DCAT_Dataset.ttl