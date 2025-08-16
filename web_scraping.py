import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import json

# Total number of pages to scrape
number_of_pages = 2050

# List to store details of all scraped units
matches_details = []


def main(page_number):
    # Send GET request to the page
    page = requests.get(f"https://www.bayut.eg/en/egypt/properties-for-sale/page-{page_number}/")

    # Get page content(as byte code)
    src = page.content

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(src, "lxml")

    # Find all property listings on the page
    all_units = soup.find_all("li", {"role" : "article"})

    # Loop through each property listing
    for unit in all_units:
        # Look for the <script> tag containing structured JSON-LD data
        script_tag = unit.find("script", {"type": "application/ld+json"})

        if script_tag:
            # Load JSON data from the script tag
            data = json.loads(script_tag.string)

            # Extract relevant information and convert data types as needed
            house = {
                "name": data["name"],

                # Convert latitude and longitude to float if available
                "latitude": float(data.get("geo", {}).get("latitude")) if data.get("geo", {}).get("latitude") else None,
                "longitude": float(data.get("geo", {}).get("longitude")) if data.get("geo", {}).get("longitude") else None,
                
                # Convert area to integer (remove commas if present
                "area(Sq. M.)": int(data.get("floorSize", {}).get("value").replace(",", "")) if data.get("floorSize", {}).get("value") else None,

                # Convert number of bedrooms, bathrooms to integer
                "bedrooms": int(data.get("numberOfRooms", {}).get("value")) if data.get("numberOfRooms", {}).get("value") else None,
                "bathrooms": int(data.get("numberOfBathroomsTotal")) if data.get("numberOfBathroomsTotal") else None,

                # Extract region and locality
                "region": data.get("address", {}).get("addressRegion"),
                "locality": data.get("address", {}).get("addressLocality"),

            }
        else:
            # If no JSON-LD data found, create empty dictionary
            house = {}
        
        # Try to extract unit type(Apartment, Villa, Duplex, ...) if available
        unit_type = unit.find("span", {"c377cd7b _3002c6fb"})
        if unit_type:
            house["unit_type"] = unit_type.get_text(strip=True)

        # Try to extract price if available and convert to integer
        price = unit.find("div", {"class": "ef4841d9"}).find("span", {"aria-label": "Price"})
        if price:
            price_text = price.get_text(strip=True)
            house["price(EGP)"] = int(price_text.replace(",", ""))


        # Append the extracted house information to the main list    
        matches_details.append(house)

        

# Loop through all pages starting from page 2
for i in range(2, number_of_pages + 1):
    main(i)
    print("page", i , " DONE👍")

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(matches_details)

# Save the DataFrame as a CSV file
csv_path = "E:/Python Project(VS Code)/Web Scraping House Prices in Egypt/units_details.csv"
df.to_csv(csv_path, index=False)

