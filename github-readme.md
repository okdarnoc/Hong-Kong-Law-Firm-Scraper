# Web Scraping Tutorial: Law Firms Data Extraction

This tutorial demonstrates how to scrape data from the law society website and save it to a JSON file using Python. We'll be extracting information about law firms from a public directory.

## Prerequisites

- Python 3.x
- Required libraries: requests, beautifulsoup4

## Installation

Install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Code Overview

The main script consists of three key functions:

1. `scrape_firm_data(firm_id)`: Scrapes data for a single law firm
2. `save_to_json(data, filename)`: Saves the scraped data to a JSON file
3. `main()`: Coordinates the scraping process for multiple firms

## Key Concepts

- Making HTTP requests with error handling
- Parsing HTML using BeautifulSoup
- Extracting structured data from HTML tables
- Implementing rate limiting to be respectful to the server
- Saving data incrementally to prevent data loss

## Code Snippet

```python
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
```

## Usage

To run the script, simply execute it using Python:

```bash
python law_firm_scraper.py
```

The script will start scraping data for law firms and save the results in a file named `law_firms_data.json`.

## Ethical Considerations

> Always respect the website's terms of service and robots.txt file when scraping. Consider using APIs if they're available, and implement proper rate limiting to avoid overwhelming the server.

## Further Learning

To expand on this tutorial, you could explore:

- Adding command-line arguments for customization
- Implementing multi-threading for faster scraping
- Storing the data in a database instead of a JSON file
- Adding more robust error handling and logging

## Full Code

Here's the complete code for the web scraping script:

```python
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

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

def main():
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
            
            save_to_json(all_data, filename)
            print(f"Data saved to {filename}")
        else:
            print(f"Skipping FirmId: {firm_id} - No data or error occurred")
        
        print("-" * 50)
        time.sleep(1)

    print(f"Scraping completed. Total firms scraped: {len(all_data)}")
    print(f"All data has been saved to '{filename}' with UTF-8 encoding")

if __name__ == "__main__":
    main()
```

---

Created as part of a web scraping tutorial. Code and tutorial are for educational purposes only.
