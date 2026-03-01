import requests
import pandas as pd
import time


# Base API endpoint
BASE_URL = "https://world.openfoodfacts.org/api/v2/search"

# Parameters
CATEGORY = "chocolates"
FIELDS = "code,product_name,brands,nutriments"
PAGE_SIZE = 100
MAX_RECORDS = 12000  # target
MAX_PAGES = MAX_RECORDS // PAGE_SIZE  # = 120 pages
SLEEP_BETWEEN_REQUESTS = 1.2  # seconds

all_rows = []

print(f"📦 Starting data fetch for '{CATEGORY}' — target: {MAX_RECORDS} records")

for page in range(1, MAX_PAGES + 1):
    url = f"{BASE_URL}?categories={CATEGORY}&fields={FIELDS}&page_size={PAGE_SIZE}&page={page}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        
        if not products:
            print(f"⚠️ No products on page {page}, stopping early.")
            break
        
        # Flatten products
        for p in products:
            code = p.get("code", "")
            name = p.get("product_name", "")
            brand = p.get("brands", "")
            nutriments = p.get("nutriments", {})
            
            row = {"product_code": code, "product_name": name, "brand": brand}
            for k, v in nutriments.items():
                row[k] = v
            all_rows.append(row)

        print(f"✅ Page {page} fetched — total records so far: {len(all_rows)}")

        # Sleep to avoid hitting rate limits
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching page {page}: {e}")
        time.sleep(5)  # backoff before retrying
        continue

# Convert to DataFrame
df = pd.DataFrame(all_rows)

# Save to CSV
output_file = "openfood_chocolates_12000.csv"
df.to_csv(output_file, index=False)

print(f"\n🎉 Done! Total records saved: {len(df)}")
print(f"📁 File: {output_file}")