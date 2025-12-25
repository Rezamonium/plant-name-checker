import pandas as pd
import requests
import time

# Load your Excel file
df = pd.read_excel("Scientific Name.xlsx")
df.columns = ['Sci_name']  # standardize column name

# --- UPDATED POWO QUERY FUNCTION ---
def query_powo(name):
    url = "https://powo.science.kew.org/api/1/search"  # more reliable endpoint
    params = {"q": name, "f": "accepted_names"}
    headers = {
        "Accept": "application/json",
        "User-Agent": "RezaSpeciesChecker/1.0"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=20)

        # Check HTTP status
        if resp.status_code != 200:
            print(f"[POWO] HTTP {resp.status_code} for '{name}'")
            return None, None

        # Attempt to parse JSON
        try:
            data = resp.json()
        except:
            print(f"[POWO] Non-JSON response for '{name}'")
            return None, None

        results = data.get("results", [])
        if not results:
            print(f"[POWO] No results for '{name}'")
            return None, None

        first = results[0]
        accepted_name = first.get("name", "")
        author = first.get("author", "")

        return accepted_name, author

    except Exception as e:
        print(f"[POWO] Error checking '{name}': {e}")
        return None, None


# --- PROCESS ALL NAMES ---
accepted_names = []
authors = []

for idx, row in df.iterrows():
    original_name = row['Sci_name']
    print(f"Checking {idx+1}/{len(df)}: {original_name}")
    accepted, author = query_powo(original_name)
    accepted_names.append(accepted)
    authors.append(author)
    time.sleep(0.5)  # friendly delay

# --- SAVE RESULTS ---
df['Accepted Name'] = accepted_names
df['Author'] = authors
df.to_excel("POWO_Accepted_Names_Output.xlsx", index=False)

print("✅ Done! Saved as 'POWO_Accepted_Names_Output.xlsx'")
