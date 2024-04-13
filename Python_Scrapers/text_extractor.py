import os
import shutil
import tempfile
from urllib.parse import urljoin
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import requests  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
project_id = "a25b9b0c1d131d1b"
location = "us"  # Format is "us" or "eu"
# file_path = "/path/to/local/pdf"
processor_display_name = "makenmodel" # Must be unique per project, e.g.: "My Processor"

PAGE_LINK_OUTPUT = "vehicle_model_links.output"
MODEL_PDF_LINKS = "model_pdfs.output"
PDF_TEXT_FOLDER = "pdf_extracted"

def quickstart(
    project_id: str,
    location: str,
    file_path: str,
    processor_display_name: str = "My Processor",
):
    # You must set the `api_endpoint`if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location, e.g.:
    # `projects/{project_id}/locations/{location}`
    parent = client.common_location_path(project_id, location)

    # Create a Processor
    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            type_="OCR_PROCESSOR",  # Refer to https://cloud.google.com/document-ai/docs/create-processor for how to get available processor types
            display_name=processor_display_name,
        ),
    )

    # Print the processor information
    print(f"Processor Name: {processor.name}")

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf",  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    )

    # Configure the process request
    # `processor.name` is the full resource name of the processor, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    # Read the text recognition output from the processor
    print("The document contains the following text:")
    print(document.text)


def extract_text():
    if not os.path.exists(MODEL_PDF_LINKS):
        print("PDF links file not found. Please run the script with -p option first.")
        return

    if not os.path.exists(PDF_TEXT_FOLDER):
        os.makedirs(PDF_TEXT_FOLDER)

    with open(MODEL_PDF_LINKS, "r", encoding="utf-8") as links:
        for pdf_link in links.readlines():
            pdf_link = pdf_link.strip()
            # Extract text from image of PDF
            image_text = extract_text_from_pdf_image(pdf_link)

            if image_text:
                filename = pdf_link.split("/")[-1]
                output_file_path = os.path.join(PDF_TEXT_FOLDER, filename + ".txt")
                with open(output_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(image_text + "\n\n\n\n")


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

def main():
    if os.path.exists(PDF_TEXT_FOLDER):
        print("Removing existing PDF text folder and files...")
        shutil.rmtree(PDF_TEXT_FOLDER)
    # extract_text()
    if not os.path.exists(PDF_TEXT_FOLDER):
        os.makedirs(PDF_TEXT_FOLDER)
    base_url = "https://www.scalemates.com"

    with open(MODEL_PDF_LINKS, "r", encoding="utf-8") as file:
        for link in file.readlines():
            pdf_url = link.strip()
            full_link = urljoin(base_url, pdf_url)
            response = requests.get(full_link)
            if response.status_code == 200:
                filename = pdf_url.split("/")[-1]
                output_file_path = os.path.join(PDF_TEXT_FOLDER, filename)
                with open(output_file_path, "wb") as pdf:
                    pdf.write(response.content)
            else:
                print(f"Failed to download PDF: {pdf_url}")


if __name__ == "__main__":
    main()
