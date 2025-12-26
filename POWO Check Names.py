import pandas as pd
import requests
import time

# =========================
# 1. LOAD INPUT EXCEL
# =========================
# Make sure the file is in the same folder as this script,
# or give the full path.
df = pd.read_excel("Scientific Name.xlsx")

# Standardise the column name containing the scientific names
df.columns = ['Sci_name']


# =========================
# 2. POWO QUERY FUNCTION
# =========================
def query_powo(name):
    """
    Query POWO for an accepted name.
    Logic:
      - Search with q = name, filter = accepted_names
      - Among all results, prefer those where genus + species
        exactly match the query (ignoring author)
      - If no exact match, fall back to the first result
    Returns:
      (accepted_name, author) or (None, None) on failure
    """
    url = "https://powo.science.kew.org/api/1/search"
    params = {
        "q": name,
        "f": "accepted_names",
        "perPage": 50   # get more results just in case
    }
    headers = {
        "Accept": "application/json",
        "User-Agent": "RezaSpeciesChecker/1.0"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=20)

        if resp.status_code != 200:
            print(f"[POWO] HTTP {resp.status_code} for '{name}'")
            return None, None

        try:
            data = resp.json()
        except Exception:
            print(f"[POWO] Non-JSON response for '{name}'")
            return None, None

        results = data.get("results", [])
        if not results:
            print(f"[POWO] No results for '{name}'")
            return None, None

        # ----- smarter match selection -----
        # Clean query
        query = str(name).strip().lower()
        query_parts = query.split()
        # genus + species from query (ignore author if present)
        if len(query_parts) >= 2:
            query_ge = " ".join(query_parts[:2])
        else:
            query_ge = query

        best = None

        # 1) Prefer exact match on genus + species (ignoring author in POWO name)
        for r in results:
            r_name = r.get("name", "")
            r_parts = r_name.lower().split()
            if len(r_parts) >= 2:
                r_ge = " ".join(r_parts[:2])
            else:
                r_ge = r_name.lower()

            if r_ge == query_ge:
                best = r
                break

        # 2) If nothing matched, fall back to first result (typical synonym case)
        if best is None:
            best = results[0]

        accepted_name = best.get("name", "")
        author = best.get("author", "")

        return accepted_name, author

    except Exception as e:
        print(f"[POWO] Error checking '{name}': {e}")
        return None, None


# =========================
# 3. PROCESS ALL NAMES
# =========================
accepted_names = []
authors = []

for idx, row in df.iterrows():
    original_name = row['Sci_name']
    print(f"Checking {idx+1}/{len(df)}: {original_name}")

    accepted, author = query_powo(original_name)

    accepted_names.append(accepted)
    authors.append(author)

    # polite delay so we don't hammer the server
    time.sleep(0.5)

# Add results to DataFrame
df['Accepted Name'] = accepted_names
df['Author'] = authors

# =========================
# 4. SAVE OUTPUT
# =========================
output_file = "POWO_Accepted_Names_Output.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Done! Saved as '{output_file}'")
