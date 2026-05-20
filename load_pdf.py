import os
from pypdf import PdfReader


def pdfloader(pdf_path):
    if not os.path.exists(pdf_path):
        return FileNotFoundError(f'File not found {pdf_path}')

    reader = PdfReader(pdf_path)
    pages = [page.extract_text() for page in reader.pages]
    return pages
