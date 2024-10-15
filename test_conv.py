import logging
import os
import sys
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

from app.utils.file_utils import get_files_in_directory
from app.services.deeplake_service import DeepLakeService

# loading env vars
load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

data_directory = os.path.join(SCRIPT_DIR, "app/data")

deeplake_service = DeepLakeService(
    dataset_name="stealth"
)

supported_extensions = [".pdf", '.md']
all_files = get_files_in_directory(data_directory, supported_extensions)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
)

def main():

    if not all_files:
        logging.warning(f"No files of format {', '.join(supported_extensions)} found in given directory, aborting...")

    # Process each file based on its type
    for file_path in [all_files[0]]:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        split_docs = text_splitter.split_documents(pages)
        
        deeplake_service.add_docs(split_docs)
        
        print(split_docs)

if __name__ == '__main__':
    main()
