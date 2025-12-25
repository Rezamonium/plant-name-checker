# Plant Scientific Name Checker

This Python tool checks plant scientific names using the [Plants of the World Online (POWO)](https://powo.science.kew.org) API and outputs accepted names and authors. This script queries the POWO search endpoint for personal research.
Respect server limits and avoid mass scraping.

## 🔍 Features

- Input: Excel file with a list of scientific names
- Checks against POWO database
- Returns accepted name, author, and more
- Output saved as Excel for easy use

## 📂 Input Format

| Sci_name           |
|---------------------------|
| Bulbophyllum superpositum |
| Phalaenopsis amabilis     |
| ...                       |

## ⚙️ Setup
1. Download all files and save to your folder.
2. Install Python.
3. Install required packages:

```bash
F:
cd Python\plant-name-checker #  ← example if you save the downloaded files into "F:\Python\plant-name-checker" folder
dir   # ← optional, just to confirm the file is listed
pip install -r requirements.txt
```

## Checking bulk your plant list scientific name
1. Making your plant species list in excel file
2. Run the Python code

## Acknowledgements
1. POWO Kew Royal Botanic Garden.
2. Developed by Reza Saputra, Papua Barat

## Important Note: This script queries the POWO search endpoint for personal research. Respect server limits and avoid mass scraping.

