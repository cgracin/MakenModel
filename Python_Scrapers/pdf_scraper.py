import os
import sys
import requests
import PyPDF2
import tempfile
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from urllib.parse import urljoin
import pytesseract
from pdf2image import convert_from_path

PAGE_LINK_OUTPUT = 'model_page_links.output'
MODEL_PDF_LINKS = 'pdf_links.output'
PDF_TEXT_FOLDER = 'pdf_texts'

def get_model_urls(page_url):
    if os.path.exists(PAGE_LINK_OUTPUT):
        print("Model links already exist. Skipping scraping.")
        return

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(page_url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all('div', class_='ac dg bgl cc pr mt4')

    with open(PAGE_LINK_OUTPUT, 'w', encoding='utf-8') as output:
        for div in divs:
            link = div.find('a', class_='pf')['href']
            output.write(link + '\n')

def get_pdfs():

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

def extract_text():
    if not os.path.exists(MODEL_PDF_LINKS):
        print("PDF links file not found. Please run the script with -p option first.")
        return

    if not os.path.exists(PDF_TEXT_FOLDER):
        os.makedirs(PDF_TEXT_FOLDER)

    with open(MODEL_PDF_LINKS, 'r', encoding='utf-8') as links:
        for pdf_link in links.readlines():
            pdf_link = pdf_link.strip()
            # Extract text from PDF
            pdf_text = extract_text_from_pdf_url(pdf_link)
            # Extract text from image of PDF
            image_text = extract_text_from_pdf_image(pdf_link)
            # Combine the text
            combined_text = pdf_text + image_text
            if combined_text:
                filename = pdf_link.split('/')[-1]
                output_file_path = os.path.join(PDF_TEXT_FOLDER, filename + ".txt")
                with open(output_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(combined_text)

def extract_text_from_pdf_image(pdf_url):
    base_url = "https://www.scalemates.com"
    full_link = urljoin(base_url, pdf_url)
    response = requests.get(full_link)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(response.content)
            temp_file.flush()
            # Convert the PDF to images
            images = convert_from_path(temp_file.name)
            extracted_text = ""
            for image in images:
                # Use pytesseract to perform OCR on the image
                text = pytesseract.image_to_string(image)
                extracted_text += text + "\n"
            return extracted_text
    else:
        print("Failed to download PDF file:", pdf_url)
        return ""

def extract_text_from_pdf_url(pdf_url):
    base_url = "https://www.scalemates.com"
    full_link = urljoin(base_url, pdf_url)
    response = requests.get(full_link)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(response.content)
            temp_file.flush()
            with open(temp_file.name, 'rb') as pdf_file:
                reader = PyPDF2.PdfFileReader(pdf_file)
                text = ""
                for page_num in range(reader.numPages):
                    page = reader.getPage(page_num)
                    text += page.extractText()
                return text
    else:
        print("Failed to download PDF file:", pdf_url)
        return None


def main():
    url = "https://www.scalemates.com/search.php?q=*&fkSECTION[]=Kits&fkCOMPNAME%5B%5D=%22Tamiya%22"

    mode = sys.argv[1]

    if mode == '-u':
        get_model_urls(url)
    elif mode == '-p':
        get_pdfs()
    elif mode == '-t':
        extract_text()

if __name__ == "__main__":
    main()
