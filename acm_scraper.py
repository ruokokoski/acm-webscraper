import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
from bs4 import BeautifulSoup
#import time

# Command line input
parser = argparse.ArgumentParser(description='ACM Search Scraper')
parser.add_argument('search_words', type=str, help='The search query for ACM')
args = parser.parse_args()

search_variable = args.search_words

base_url = "https://dl.acm.org/action/doSearch?"
query_params = {"AllField": search_variable}
encoded_query = urlencode(query_params)

# Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
#prefs = {"profile.managed_default_content_settings.images": 2}  # Disable images
#options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

# ACM search URL
search_url = f"{base_url}{encoded_query}"
driver.get(search_url)

# Wait results to load
wait = WebDriverWait(driver, 20)
try:
    results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-result__xsl-body")))
except:
    print("\nHakutuloksia ei löytynyt\n")
    driver.quit()
    exit()

# Parse the HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Find the first search result
first_result = soup.find('li', class_='search__item')
if not first_result:
    print("\nHakutuloksia ei löytynyt\n")
    driver.quit()
    exit()
#print(f"First result: {first_result}\n")

# Access first_result to ensure parsing
_ = first_result.prettify()

# Extract tile
title_tag = first_result.find('h5', class_='issue-item__title') if first_result else None
title = title_tag.text.strip() if title_tag else "Title ei löytynyt"

# Extract authors
author_list = first_result.find('ul', class_='rlist--inline loa truncate-list')
if author_list:
    authors = ', '.join(
        author.find('span').text.strip() for author in author_list.find_all('li') if author.find('span')
    )
else:
    authors = "Authoreita ei löytynyt"

# Extract year
year_tag = first_result.find('div', class_='bookPubDate')
year = None
if year_tag:
    year = year_tag.text.strip().split()[-1]  # Oletetaan, että vuosi on aina viimeisenä
year = year if year else "Vuotta ei löytynyt"

# Extract DOI link
doi_link = None
if title_tag:
    link_tag = title_tag.find('a')
    if link_tag and 'href' in link_tag.attrs:
        doi_link = f"https://dl.acm.org{link_tag['href']}"
doi_link = doi_link if doi_link else "DOI-linkkiä ei löytynyt"
'''

# Trigger the BibTeX button
#bibtex_button = driver.find_element(By.CLASS_NAME, 'btn--icon')
bibtex_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn--icon')))
bibtex_button.click()

# Wait for the export modal
time.sleep(3)
modal_html = driver.page_source
modal_soup = BeautifulSoup(modal_html, 'html.parser')

# Extract BibTeX content
bibtex_section = modal_soup.find('pre', class_='bibtex')
bibtex_citation = bibtex_section.text.strip() if bibtex_section else "BibTeX virhe"
'''
print(f"\nEncoded query: \t{encoded_query}\n")
print(f"Authors: \t{authors}")
print(f"Year: \t\t{year}")
print(f"Title: \t\t{title}")
print(f"DOI: \t\t{doi_link}")

#print(f"BibTeX: {bibtex_citation}")
print()
driver.quit()

