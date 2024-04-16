import os
import sys
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from urllib.parse import urljoin
import os
from google.cloud import storage
import json

PAGE_LINK_OUTPUT = 'model_page_links.output'
MODEL_PDF_LINKS = 'pdf_links.output'
PDF_TEXT_FOLDER = 'pdf_texts'

BUCKET_NAME = "makenmodel_extractedpdfs"
EXTRACTED_PDF_FOLDER = "json_extracted"

def get_model_urls():
    """Retrieval all relevant models from Scale Mates."""
    if os.path.exists(PAGE_LINK_OUTPUT):
        print("Model links already exist. Skipping scraping.")
        return

    url = "https://www.scalemates.com/search.php?q=tamiya&fkSECTION[]=Kits&fkCOMPNAME[]=%22Tamiya%22&fkTYPENAME[]=%22Full%20kits%22&fkGROUPS[]=%22Ships%22&fkGROUPS[]=%22Aircraft%22&fkGROUPS[]=%22Vehicles%22&fkGROUPS[]=%22Space%22&fkGROUPS[]=%22Trains%22"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    # for infinite scrolling
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all('div', class_='ac dg bgl cc pr mt4')

    # find all model page links on scale mates search page
    with open(PAGE_LINK_OUTPUT, 'w', encoding='utf-8') as output:
        for div in divs:
            link = div.find('a', class_='pf')['href']
            output.write(link + '\n')

def get_pdfs():
    """Get links for model PDF instructions."""
    with open(MODEL_PDF_LINKS, 'w', encoding='utf-8') as out:
        out.write('')

    with open(PAGE_LINK_OUTPUT, 'r', encoding='utf-8') as links:
        page_links = [link.strip() for link in links.readlines()]

    for link in page_links:
        base_url = "https://www.scalemates.com"
        full_link = urljoin(base_url, link)
        page = requests.get(full_link)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            download_link = soup.find('a', href=True, title="Download Instruction Plans")
            if download_link:
                pdf_link = download_link['href']
                with open(MODEL_PDF_LINKS, 'a', encoding='utf-8') as output:
                    output.write(pdf_link + '\n')


def download_text():
    """Download processed JSONs from Cloud Storage."""
    if not os.path.exists(EXTRACTED_PDF_FOLDER):
        os.makedirs(EXTRACTED_PDF_FOLDER)

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = storage_client.list_blobs(BUCKET_NAME)

    json_paths = []
    for blob in blobs:
        name = (blob.name).split("-")
        if name[-1] == "0.json":
            json_paths.append(blob.name)

    for path in json_paths:
        file = bucket.blob(path)
        json_file = json.loads(file.download_as_string())
        blob_name = (file.name).split("/")[-1]
        remote_file = os.path.join(EXTRACTED_PDF_FOLDER, blob_name)
        with open(remote_file, "w") as output:
            json.dump(json_file, output)

def main():
    mode = sys.argv[1]

    if mode == '-u':
        get_model_urls()
    elif mode == '-p':
        get_pdfs()
    elif mode == '-t':
        download_text()


if __name__ == "__main__":
    main()
