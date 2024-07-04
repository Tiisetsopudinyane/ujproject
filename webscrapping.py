import requests
from bs4 import BeautifulSoup
import schedule
import time

def fetch_and_parse():
    # Define the URL
    url = 'https://www.inside-sme.com/innovative-funding-models-for-south-african-startups/'

    # Define headers with a User-Agent to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send a GET request to the specified URL with headers
    req = requests.get(url, headers=headers)

    # Check if the request was successful
    if req.status_code == 200:
        # Parse the response content with BeautifulSoup
        soup = BeautifulSoup(req.content, 'html.parser')

        # Find blockquote tag with class 'wp-block-quote'
        s = soup.find('blockquote', class_='wp-block-quote')

        # Check if blockquote exists
        if s:
            # Find all list items within the blockquote
            content = s.find_all('li')

            # Create a list to store the dictionaries
            results = []

            # Process each list item
            for item in content:
                anchor = item.find('a')
                if anchor:
                    # Extract title, link, and description
                    title = anchor.text
                    link = anchor['href']
                    description = item.get_text(strip=True).replace(title, '').strip(': ')

                    # Create a dictionary for the item
                    item_dict = {
                        'title': title,
                        'link': link,
                        'description': description
                    }

                    # Add the dictionary to the results list
                    results.append(item_dict)
            
            # Print the results
            # for result in results:
            print(results)
            return results
        else:
            print("No blockquote with class 'wp-block-quote' found.")
    else:
        print(f"Failed to retrieve the page. Status code: {req.status_code}")

# Schedule the task to run every 30 days
# schedule.every(30).days.do(fetch_and_parse)

# Keep the script running
# while True:
#     schedule.run_pending()
#     time.sleep(1)
fetch_and_parse()