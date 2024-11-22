# hk_law_society_scraper.py

import requests
from bs4 import BeautifulSoup
import json
import time
from requests.exceptions import RequestException

def scrape_firm_data(firm_id):
    """
    Scrape data for a single law firm from the Hong Kong Law Society website.
    
    Args:
        firm_id (int): The unique identifier for the law firm
        
    Returns:
        dict: Dictionary containing the firm's data if found, None otherwise
        
    The function scrapes basic firm information until it reaches the staff section,
    excluding staff details to respect privacy and data minimization principles.
    """
    url = f"https://www.hklawsoc.org.hk/en/Serve-the-Public/The-Law-List/Firm-Detail?FirmId={firm_id}"
    try:
        # Attempt to fetch the webpage with a timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"Error fetching data for FirmId {firm_id}: {e}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    
    if not table:
        print(f"No data found for FirmId: {firm_id}")
        return None
    
    # Extract firm details from the table
    data = {'FirmId': firm_id}
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            # Stop at the staff section to exclude personal information
            if key.lower() == "staff":
                break
            data[key] = value
    
    return data if len(data) > 1 else None

def save_to_json(data, filename):
    """
    Save the scraped data to a JSON file with UTF-8 encoding.
    
    Args:
        data (list): List of dictionaries containing firm data
        filename (str): Name of the output JSON file
    """
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

def main():
    """
    Main function to orchestrate the scraping process.
    
    Scrapes data for law firms with IDs from 1 to 2000,
    saving results incrementally to prevent data loss.
    """
    start_id = 1
    end_id = 2000
    all_data = []
    filename = 'law_firms_data.json'
    
    for firm_id in range(start_id, end_id + 1):
        print(f"Attempting to scrape data for FirmId: {firm_id}")
        firm_data = scrape_firm_data(firm_id)
        
        if firm_data:
            all_data.append(firm_data)
            print("Data found:")
            for key, value in firm_data.items():
                print(f"  {key}: {value}")
            print(f"Data scraped successfully for FirmId: {firm_id}")
            
            # Save data incrementally to prevent data loss
            save_to_json(all_data, filename)
            print(f"Data saved to {filename}")
        else:
            print(f"Skipping FirmId: {firm_id} - No data or error occurred")
        
        print("-" * 50)  # Visual separator for log readability
        time.sleep(1)  # Respectful delay between requests

    print(f"Scraping completed. Total firms scraped: {len(all_data)}")
    print(f"All data has been saved to '{filename}' with UTF-8 encoding")

if __name__ == "__main__":
    main()
