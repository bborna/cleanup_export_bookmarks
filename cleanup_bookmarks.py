import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w',
                    filename='bookmarks.log',
                    level=logging.DEBUG)

#######
# Configuration
BOOKMARKS_FILE_PATH = './bookmarks.html'
OUTPUT_FILE_PATH = './new-bookmarks.html'
#######

def check_status_code(url):
    try:
        response = requests.get(url, timeout=2)
        # Test for 200 response
        if response.status_code == 200:
            # add to new file
            return True
        elif response.status_code == 301:
            return True
        elif response.status_code == 302:
            return True
        else:
            # return error
            return False
    except:
        logging.error('Error connecting to URL: ' + url)


# Load original bookmarks
bookmarks_file = open(BOOKMARKS_FILE_PATH, 'r')
bookmarks_html = bookmarks_file.read()
bookmarks_file.close()
logging.info('Loaded original bookmarks file.')
# create new output file
new_bookmarks_file = open(OUTPUT_FILE_PATH, 'w+')

# Read HTML DOM elements and find DT//A
soup = BeautifulSoup(bookmarks_html, "html.parser")

bookmarks = soup.find_all('a')  # Grab the first table

for bookmark in bookmarks:
    # Check if URL is good
    url = bookmark.get('href')
    logging.info('Processing: ' + url)
    url_response = check_status_code(url)
    if url_response:
        logging.info('URL: ' + url)
        # Add URL to file
        new_bookmarks_file.write(str(bookmark))
    else:
        # Log errors if not 200 response
        logging.error('URL did not return successful response: ' + url)

new_bookmarks_file.close()
