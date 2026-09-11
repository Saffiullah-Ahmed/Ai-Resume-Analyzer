import os
import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts raw text from a PDF document using pdfplumber.
    
    :param pdf_path: Absolute or relative path to the PDF file.
    :return: Cleaned single string containing all extracted text across pages.
    :raises FileNotFoundError: If the provided path does not exist.
    :raises ValueError: If the file is not a valid PDF or contains no extractable text.
    """
    # 1. Verify file existence before attempting to open
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")
        
    extracted_pages = []
    
    # 2. Open PDF securely using pdfplumber's context manager
    with pdfplumber.open(pdf_path) as pdf:
        # Check for empty PDF documents
        if len(pdf.pages) == 0:
            raise ValueError(f"The PDF file '{pdf_path}' contains no pages.")
            
        # 3. Iterate page-by-page and extract readable text
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                extracted_pages.append(page_text.strip())
            else:
                print(f"[WARNING] Page {page_num} in '{pdf_path}' contained no readable text.")

    # 4. Join all page content with clean newlines
    full_text = "\n\n".join(extracted_pages).strip()
    
    if not full_text:
        raise ValueError(f"No extractable text found inside '{pdf_path}'. It may be a scanned image-only PDF.")
        
    return full_text