import os
import shutil
import tempfile
from urllib.parse import urljoin
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud import storage
import requests  # type: ignore

PAGE_LINK_OUTPUT = "vehicle_model_links.output"
MODEL_PDF_LINKS = "model_pdfs.output"
PDF_PROCESSED_FOLDER = "pdf_preprocessed"

def list_blobs():
    """Lists all the blobs in the bucket."""
    bucket_name = "makenmodel-pdf"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)




def main():
    if not os.path.exists(PDF_PROCESSED_FOLDER):
        os.makedirs(PDF_PROCESSED_FOLDER)

    list_blobs()


if __name__ == "__main__":
    main()
