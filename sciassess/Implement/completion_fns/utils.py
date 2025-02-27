import os
from functools import wraps
import pickle
import json
import uuid
from pathlib import Path

def cache_to_disk(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_dir = os.path.join('SciAssess_library/tmp', 'cache')
        os.makedirs(cache_dir, exist_ok=True)
        # generate id of call info
        call_id = f"{func.__qualname__}"
        for arg in args:
            call_id += "args0:"
            try:
                call_id += json.dumps(arg)
            except TypeError:
                call_id += json.dumps(arg.__dict__)
            call_id += ","
        for k, v in kwargs.items():
            call_id += f"kwargs {k}:"
            try:
                call_id += json.dumps(v)
            except TypeError:
                call_id += json.dumps(v.__dict__)
            call_id += ","
        call_id = uuid.uuid5(uuid.NAMESPACE_DNS, call_id)
        cache_file = str(cache_dir / f"{func.__qualname__}_{call_id}.pkl")
        if os.path.exists(cache_file):
            print('loading from cache:', cache_file)
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        result = func(*args, **kwargs)
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
        return result
    return wrapper

def extract_text(pdf_path, add_page_num: bool = False) -> list[str]:
    """
    Extracts text from a PDF file and returns it as a list of strings.
    Args:
        pdf_path: The path to the PDF file.
        add_page_num: Whether to add the page number to the beginning of each page's text.

    Returns:
        texts: A list of strings, where each string is the text from a page.
    """
    # Open the PDF file
    texts = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Iterate through each page and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            text = f"Page {page_num + 1}:\n{text}\n" if add_page_num else text + "\n"
            texts.append(text)
    return texts

