from pathlib import Path
import pypdf
import docx # python-docx library
from typing import Optional
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_file(file_path: str, mime_type: Optional[str] = None) -> str:
    """
    Extracts text from PDF, DOCX, and TXT files.

    Args:
        file_path (str): The path to the file.
        mime_type (Optional[str]): The MIME type of the file (currently informational).

    Returns:
        str: The extracted text, or an empty string if extraction fails,
             or "Unsupported file type" if the file extension is not supported.
    """
    path = Path(file_path)
    extracted_text = ""

    if not path.exists():
        logging.error(f"File not found: {file_path}")
        return ""

    file_extension = path.suffix.lower()
    
    # Informational: Log if mime_type and extension mismatch, but trust extension for now.
    if mime_type:
        if "pdf" in mime_type.lower() and file_extension != ".pdf":
            logging.warning(f"MIME type '{mime_type}' suggests PDF, but extension is '{file_extension}'. Trusting extension.")
        elif "wordprocessingml.document" in mime_type.lower() and file_extension != ".docx":
            logging.warning(f"MIME type '{mime_type}' suggests DOCX, but extension is '{file_extension}'. Trusting extension.")
        elif "plain" in mime_type.lower() and file_extension != ".txt":
             logging.warning(f"MIME type '{mime_type}' suggests TXT, but extension is '{file_extension}'. Trusting extension.")


    try:
        if file_extension == ".pdf":
            try:
                reader = pypdf.PdfReader(path)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n" # Add newline between pages
            except pypdf.errors.PdfReadError as e:
                logging.error(f"Error reading PDF file {path}: {e}. The file might be corrupted or password-protected.")
                return ""
            except Exception as e_pdf: # Catch other potential pypdf errors
                logging.error(f"An unexpected error occurred while processing PDF {path}: {e_pdf}")
                return ""
        
        elif file_extension == ".docx":
            try:
                document = docx.Document(path)
                for para in document.paragraphs:
                    extracted_text += para.text + "\n"
            except Exception as e_docx: # Catches errors like package not found if file is not a valid docx
                logging.error(f"Error reading DOCX file {path}: {e_docx}")
                return ""

        elif file_extension == ".txt":
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
            except UnicodeDecodeError:
                logging.warning(f"UTF-8 decoding failed for {path}. Trying 'latin-1'.")
                try:
                    with open(path, 'r', encoding='latin-1') as f:
                        extracted_text = f.read()
                except Exception as e_latin1:
                    logging.error(f"Failed to read {path} with 'latin-1' encoding: {e_latin1}")
                    return ""
            except Exception as e_txt:
                logging.error(f"Error reading TXT file {path}: {e_txt}")
                return ""
        
        else:
            logging.warning(f"Unsupported file type: '{file_extension}' for file {path}")
            return "Unsupported file type"

    except FileNotFoundError: # This is already checked above, but as a safeguard
        logging.error(f"File not found (should have been caught earlier): {file_path}")
        return ""
    except Exception as e: # Generic catch-all for other unexpected errors
        logging.error(f"An unexpected error occurred processing file {path}: {e}")
        return ""

    return extracted_text.strip()

if __name__ == '__main__':
    # Create dummy files for basic local testing
    # Note: For robust testing, these files should be created in a temporary directory
    # and cleaned up afterwards. This is a simplified example.

    # Create dummy .txt file
    Path("dummy_test.txt").write_text("This is a test TXT file with some special characters: éàçöü.", encoding="utf-8")
    Path("dummy_latin1.txt").write_text("This is a latin-1 encoded file: éàç.", encoding="latin-1")


    # The following requires actual PDF and DOCX files to be present.
    # To run these tests, place 'dummy_test.pdf' and 'dummy_test.docx' in the same directory.
    # You can create simple ones for testing.

    # Example: Test TXT
    print(f"--- Testing TXT (UTF-8) ---")
    text_utf8 = extract_text_from_file('dummy_test.txt')
    print(f"Extracted (UTF-8): '{text_utf8}'\n")

    print(f"--- Testing TXT (Latin-1) ---")
    text_latin1 = extract_text_from_file('dummy_latin1.txt')
    print(f"Extracted (Latin-1): '{text_latin1}'\n")

    # Example: Test non-existent file
    print(f"--- Testing Non-Existent File ---")
    text_non_existent = extract_text_from_file('non_existent_file.txt')
    print(f"Extracted (Non-Existent): '{text_non_existent}'\n")

    # Example: Test unsupported file type
    Path("dummy_unsupported.py").write_text("print('hello')", encoding="utf-8")
    print(f"--- Testing Unsupported File Type ---")
    text_unsupported = extract_text_from_file('dummy_unsupported.py')
    print(f"Extracted (Unsupported): '{text_unsupported}'\n")

    # Placeholder for PDF and DOCX tests - requires files
    # Ensure you have 'dummy_test.pdf' and 'dummy_test.docx' to test these.
    # if Path('dummy_test.pdf').exists():
    #     print(f"--- Testing PDF ---")
    #     text_pdf = extract_text_from_file('dummy_test.pdf')
    #     print(f"Extracted (PDF): '{text_pdf[:200]}...'") # Print first 200 chars
    # else:
    #     print("\nSkipping PDF test: dummy_test.pdf not found.")

    # if Path('dummy_test.docx').exists():
    #     print(f"\n--- Testing DOCX ---")
    #     text_docx = extract_text_from_file('dummy_test.docx')
    #     print(f"Extracted (DOCX): '{text_docx[:200]}...'") # Print first 200 chars
    # else:
    #     print("\nSkipping DOCX test: dummy_test.docx not found.")

    # Clean up dummy files
    Path("dummy_test.txt").unlink(missing_ok=True)
    Path("dummy_latin1.txt").unlink(missing_ok=True)
    Path("dummy_unsupported.py").unlink(missing_ok=True)
    print("\nCleaned up dummy files.")
