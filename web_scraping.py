import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import json

number_of_pages = 2050
matches_details = []

def main(page_number):
    page = requests.get(f"https://www.bayut.eg/en/egypt/properties-for-sale/page-{page_number}/")
    src = page.content
    soup = BeautifulSoup(src, "lxml")


    all_units = soup.find_all("li", {"role" : "article"})

    for unit in all_units:
        script_tag = unit.find("script", {"type": "application/ld+json"})
        if script_tag:
            data = json.loads(script_tag.string)
            house = {
                "name": data["name"],

                # convert to float (if not None)
                "latitude": float(data.get("geo", {}).get("latitude")) if data.get("geo", {}).get("latitude") else None,
                "longitude": float(data.get("geo", {}).get("longitude")) if data.get("geo", {}).get("longitude") else None,
                
                # convert to int
                "area(Sq. M.)": int(data.get("floorSize", {}).get("value").replace(",", "")) if data.get("floorSize", {}).get("value") else None,
                "bedrooms": int(data.get("numberOfRooms", {}).get("value")) if data.get("numberOfRooms", {}).get("value") else None,
                "bathrooms": int(data.get("numberOfBathroomsTotal")) if data.get("numberOfBathroomsTotal") else None,

                "region": data.get("address", {}).get("addressRegion"),
                "locality": data.get("address", {}).get("addressLocality"),

            }
        else:
            house = {}
        
        unit_type = unit.find("span", {"c377cd7b _3002c6fb"})
        if unit_type:
            house["unit_type"] = unit_type.get_text(strip=True)

        price = unit.find("div", {"class": "ef4841d9"}).find("span", {"aria-label": "Price"})
        if price:
            price_text = price.get_text(strip=True)
            house["price(EGP)"] = int(price_text.replace(",", ""))


        # add match info to matches_details    
        matches_details.append(house)

        

        




for i in range(2, number_of_pages + 1):
    main(i)
    print("page", i , " DONE👍")

# Convert to DataFrame
df = pd.DataFrame(matches_details)

# Save as CSV
csv_path = "E:/Python Project(VS Code)/Web Scraping House Prices in Egypt/units_details.csv"
df.to_csv(csv_path, index=False)

