'''
Extract all circular items, convert the extracted data to JSON, and save it to a file named cbn_circulars.json .
'''
import requests
from bs4 import BeautifulSoup
import json
def fetch_and_parse_cbn():
    url = "https://www.cbn.gov.ng/Documents/circulars.html"
    # Prepending a User-Agent to avoid the 403 Forbidden error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"Connecting to {url}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Check if the request was successful
        
        # Initialize BeautifulSoup to read the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        circulars_list = []
        table = soup.find('table') 
        
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if len(cols) >= 2:
                    item = {
                        "date": cols[0].text.strip(),
                        "title": cols[1].text.strip(),
                        "link": "https://www.cbn.gov.ng" + cols[1].find('a')['href'] # type: ignore if cols[1].find('a') else "N/A"
                    }
                    circulars_list.append(item)

        # Save the structured data to JSON
        with open('cbn_circulars.json', 'w', encoding='utf-8') as f:
            json.dump(circulars_list, f, indent=4)

        print(f"Successfully extracted {len(circulars_list)} items to cbn_circulars.json")

    except Exception as e:
        print(f"An error occurred during extraction: {e}")

if __name__ == "__main__":
    fetch_and_parse_cbn()
    
          