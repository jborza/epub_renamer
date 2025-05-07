import os
from PyPDF2 import PdfReader
import re
UNKNOWN = 'Unknown'

def sanitize_filename(name):
    """
    Sanitize a string to make it safe for use as a file name.
    Removes or replaces invalid characters.
    """
    # Replace invalid characters with an underscore
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', name)
    # Strip leading/trailing whitespace and dots
    return sanitized.strip().strip('.')

def get_metadata(pdf_path):
    """Extract author and title metadata from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        title = metadata.title if metadata and metadata.title else UNKNOWN
        author = metadata.author if metadata and metadata.author else UNKNOWN
        return author, title
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None, None

def rename_pdfs(directory):
    """Rename all PDF files in the given directory."""
    for file_name in os.listdir(directory):
        if file_name.lower().endswith('.pdf'):
            file_path = os.path.join(directory, file_name)
            author, title = get_metadata(file_path)
            if author == UNKNOWN or title == UNKNOWN:
                print(f"Skipping: {file_name} (metadata not found)")
                continue

            if author and title:
                new_name = f"{author} - {title}.pdf"
                # Sanitize the new file name
                new_name = sanitize_filename(new_name)
                new_path = os.path.join(directory, new_name)
                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed: {file_name} -> {new_name}")
                except OSError as e:
                    print(f"Error renaming {file_name} to {new_name}: {e}")
            else:
                print(f"Skipping: {file_name} (metadata not found)")

if __name__ == "__main__":
    # Specify the directory containing your PDF files
    pdf_directory = input("Enter the path to your PDF collection: ").strip()
    if os.path.isdir(pdf_directory):
        rename_pdfs(pdf_directory)
    else:
        print(f"{pdf_directory} is not a valid directory.")