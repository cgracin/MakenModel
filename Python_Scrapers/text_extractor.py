import os
from google.cloud import storage
import json

BUCKET_NAME = "makenmodel_extractedpdfs"
EXTRACTED_PDF_FOLDER = "json_extracted"

def extract_text():
    """Lists all the blobs in the bucket."""
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
    if not os.path.exists(EXTRACTED_PDF_FOLDER):
        os.makedirs(EXTRACTED_PDF_FOLDER)

    extract_text()


if __name__ == "__main__":
    main()
