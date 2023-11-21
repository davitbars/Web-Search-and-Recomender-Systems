from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def connectDataBase():
    client = MongoClient("mongodb://localhost:27017")  
    db = client["A3"]
    print("succesfully connected")
    return db


def get_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute_url = urljoin(url, href)
        links.append(absolute_url)

    return links

def find_heading_on_page(url, target_heading):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    store_page(url, soup.prettify())
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for heading in headings:
        if target_heading.lower() in heading.text.lower():
            return True

    return False

def crawl_web(start_url, target_heading):
    visited_urls = set()
    urls_to_visit = [start_url]

    while urls_to_visit:
        current_url = urls_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)

        if find_heading_on_page(current_url, target_heading):
            print(f'Found "{target_heading}" at: {current_url}')
            return

        new_links = get_links_from_page(current_url)
        urls_to_visit.extend(new_links)

def store_page(url, html):
    pages = db.pages
    page = {
        "url": url,
        "html": html
    }

    pages.insert_one(page)

if __name__ == "__main__":
    start_url = "https://www.cpp.edu/sci/computer-science/"
    target_heading = "Permanent Faculty"
    db = connectDataBase()
    
    crawl_web(start_url, target_heading)
