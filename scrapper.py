import requests
from bs4 import BeautifulSoup
import json
import time
from requests.exceptions import RequestException

def scrape_firm_data(firm_id):
    url = f"https://www.hklawsoc.org.hk/en/Serve-the-Public/The-Law-List/Firm-Detail?FirmId={firm_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"Error fetching data for FirmId {firm_id}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    
    if not table:
        print(f"No data found for FirmId: {firm_id}")
        return None
    
    data = {'FirmId': firm_id}
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            if key.lower() == "staff":
                break
            data[key] = value
    
    return data if len(data) > 1 else None

# ... (rest of the code)
