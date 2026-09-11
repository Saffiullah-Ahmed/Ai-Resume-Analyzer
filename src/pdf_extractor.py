import pypdf

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts raw text content from a PDF file.
    
    :param pdf_path: Path to the target PDF file.
    :return: Extracted raw text string.
    """
    text = ""
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()