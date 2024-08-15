# This script shows you how to grab information from a website and save it to a file on your computer.
# We'll be looking at law firm data as an example.

# First, we need to bring in some helpful tools (these are called libraries):
import requests  # This is like a robot that can visit websites for us
from bs4 import BeautifulSoup  # This helps us read and understand the website's content
import json  # This helps us work with a special kind of data format called JSON
import time  # This lets us add pauses in our script
from requests.exceptions import RequestException  # This helps us handle errors when visiting websites

# This is a function. Think of it like a recipe for a specific task.
# This recipe is for getting information about one law firm.
def scrape_firm_data(firm_id):
    # We're creating the web address (URL) for the law firm's page
    # It's like writing down the address of a house we want to visit
    url = f"https://www.hklawsoc.org.hk/en/Serve-the-Public/The-Law-List/Firm-Detail?FirmId={firm_id}"
    
    try:
        # Now we're asking our robot (requests) to visit the website
        # We're giving it 10 seconds to do this task
        response = requests.get(url, timeout=10)
        # If something goes wrong (like the page doesn't exist), we want to know about it
        response.raise_for_status()
    except RequestException as e:
        # If there's a problem, we print out what went wrong
        print(f"Oops! We couldn't get the data for FirmId {firm_id}. Here's what happened: {e}")
        return None  # We return None, which is like saying "we got nothing"
    
    # Now we use BeautifulSoup to read and understand the website's content
    # It's like translating the website into a language our program can understand
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # We're looking for a table on the page that has the firm's information
    table = soup.find('table')
    
    # If we can't find a table, we let ourselves know and return None (nothing)
    if not table:
        print(f"We couldn't find any information for FirmId: {firm_id}")
        return None
    
    # We're creating a basket (dictionary) to put all the firm's information in
    # We start by putting the firm's ID in the basket
    data = {'FirmId': firm_id}
    
    # Now we're going through each row of the table
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 2:  # We're only interested in rows with two cells
            key = cells[0].text.strip()  # The first cell is the type of information
            value = cells[1].text.strip()  # The second cell is the actual information
            # We stop when we reach the "Staff" section because we don't need that info
            if key.lower() == "staff":
                break
            # We put this piece of information in our basket
            data[key] = value
    
    # If we found more than just the FirmId, we return our basket of information
    # Otherwise, we return None (nothing)
    return data if len(data) > 1 else None

# This function saves our collected data to a file
def save_to_json(data, filename):
    # We're opening a file to write our data into
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        # We're using json.dump to write our data in a special format (JSON)
        # ensure_ascii=False and encoding='utf-8' make sure we can save names in any language
        # indent=2 makes the file look nice and readable
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

# This is our main function. It's like the conductor of an orchestra,
# telling all the other functions when to play their part.
def main():
    start_id = 1  # We'll start with the first firm
    end_id = 2000  # We'll stop at the 2000th firm
    all_data = []  # This is a big basket to hold all the firms' data
    filename = 'law_firms_data.json'  # This is the name of the file we'll save our data in
    
    # We're going to look at each firm, one by one
    for firm_id in range(start_id, end_id + 1):
        print(f"Let's try to get information for FirmId: {firm_id}")
        
        # We use our scrape_firm_data recipe to get info about this firm
        firm_data = scrape_firm_data(firm_id)
        
        if firm_data:  # If we got some data back...
            # We add this firm's data to our big basket
            all_data.append(firm_data)
            print("Great! We found some data:")
            # We print out each piece of information we found
            for key, value in firm_data.items():
                print(f"  {key}: {value}")
            print(f"We successfully got data for FirmId: {firm_id}")
            
            # We save all our data to a file, just in case something goes wrong later
            save_to_json(all_data, filename)
            print(f"We saved all our data to {filename}")
        else:
            print(f"We're skipping FirmId: {firm_id} - We couldn't find any data for this one")
        
        print("-" * 50)  # This prints a line of dashes to separate each firm's info
        time.sleep(1)  # We pause for 1 second to be nice to the website's server

    # We're all done! Let's print out a summary
    print(f"We're finished! We got information for {len(all_data)} firms in total.")
    print(f"All the data has been saved in the file '{filename}'")

# This is a special line that Python looks for. It tells Python to run our main function
# when we start our script.
if __name__ == "__main__":
    main()
