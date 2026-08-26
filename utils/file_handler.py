import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from utils.logger_handler import logger


def get_file_md5_hex(file_path: str) -> str:
    if not os.path.exists(file_path):
        logger.error(f"{file_path} does not exist.")
        return ""  # Return an empty string or handle the error as needed

    if not os.path.isfile(file_path):
        logger.error(f"{file_path} is not a valid file path.")
        return ""  # Return an empty string or handle the error as needed

    md5_hash = hashlib.md5()

    chunk_size = 4096  # Read in chunks of 4KB

    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating MD5 for {file_path}: {e}")
        return ""  # Return an empty string or handle the error as needed

def listdir_with_allower_type(path: str, allowed_types: tuple[str]):
    files=[]

    if not os.path.isdir(path):
        logger.error(f"{path} is not a valid directory.")
        return files  # Return an empty list or handle the error as needed

    for file_name in os.listdir(path):
        if file_name.endswith(allowed_types):
            files.append(os.path.join(path, file_name))

    return tuple(files)

def pdf_loader(filepath: str, password=None) -> list[Document]:
    return PyPDFLoader(filepath, password=password).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()