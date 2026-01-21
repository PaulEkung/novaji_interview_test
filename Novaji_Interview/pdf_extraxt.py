'''
The source code downloads all linked PDF files from https://www.cbn.gov.ng/Documents/circulars.html, saves them into a sub-directory, renamed the files and removed spaces from file names, and included the local file path or link to each downloaded PDF in the JSON records created in task main.py.
'''
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_and_download_circulars():
    root_url = "https://www.cbn.gov.ng/Documents/circulars.html"
    base_domain = "https://www.cbn.gov.ng"
    download_dir = "downloaded_pdfs"
    json_file = "cbn_circulars.json"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Create sub-directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")

    try:
        response = requests.get(root_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        circulars_data = []
        
        #Find the table and rows
        table = soup.find('table')
        if not table:
            print("Could not find the data table on the page.")
            return

        rows = table.find_all('tr')
        print(f"Found {len(rows)-1} potential circulars. Starting download...")

        for row in rows[1:]:  # Skip header
            cols = row.find_all('td')
            if len(cols) >= 2:
                date = cols[0].text.strip()
                title = cols[1].text.strip()
                link_tag = cols[1].find('a')
                
                if link_tag and link_tag.get('href'):
                    # Create full URL for the PDF
                    pdf_url = urljoin(base_domain, link_tag['href']) # type: ignore
                    
                    if pdf_url.lower().endswith('.pdf'):
                        # 3. Rename and remove spaces
                        original_name = pdf_url.split('/')[-1]
                        clean_name = original_name.replace(" ", "_")
                        file_path = os.path.join(download_dir, clean_name)
                        
                        # 4. Download the PDF file
                        try:
                            pdf_res = requests.get(pdf_url, headers=headers, stream=True)
                            if pdf_res.status_code == 200:
                                with open(file_path, 'wb') as f:
                                    for chunk in pdf_res.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                
                                # 5. Store record with local path
                                circulars_data.append({
                                    "date": date,
                                    "title": title,
                                    "original_url": pdf_url,
                                    "local_path": os.path.abspath(file_path)
                                })
                                print(f"Downloaded: {clean_name}")
                        except Exception as e:
                            print(f"Failed to download {pdf_url}: {e}")

        # 6. Save final JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(circulars_data, f, indent=4)
            
        print(f"\nTask Complete! JSON saved to {json_file}")

    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    fetch_and_download_circulars()