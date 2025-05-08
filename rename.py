# called on an epub file
import os
import re
from ebooklib import epub

from epubs import get_metadata_epub
from pdfs import get_metadata_pdf
from utils import UNKNOWN, sanitize_filename

def get_metadata(epub_path):
    """Extract author and title metadata from an EPUB file."""
    try:
        book = epub.read_epub(epub_path)
        title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else UNKNOWN
        author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else UNKNOWN
        return author, title
    except Exception as e:
        print(f"Error reading {epub_path}: {e}")
        return None, None

def contains_alphabetic_characters(s):
    """
    Check if a string contains any alphabetic characters (a-zA-Z).
    """
    return bool(re.search(r'[a-zA-Z]', s))

def rename_books(directory):
    """Rename all EPUB/PDF files in the given directory."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not file_name.lower().endswith(('.epub', '.pdf')):
                continue
            if file_name.lower().endswith('.pdf'):
                author, title = get_metadata_pdf(file_path)
            elif file_name.lower().endswith('.epub'):
                author, title = get_metadata_epub(file_path)
            if not author or not title:
                print(f"Skipping: {file_name} (metadata not found)")
                continue
            if author.lower() == UNKNOWN or title.lower() == UNKNOWN:
                print(f"Skipping: {file_name} (metadata not found)")
                continue
            # sometimes the author is replaced with numbers - then don't rename
            if not contains_alphabetic_characters(author):
                print(f"Skipping: {file_path} (author name doesn't contain alphabetic characters)")
                continue


            if author and title:
                author = author.strip()
                title = title.strip()
                original_extension = os.path.splitext(file_name)[1]
                new_name = f"{author} - {title}{original_extension}"
                # sometimes there are two folowing dots
                new_name = re.sub(r'\.\.+', '.', new_name)

                new_name = sanitize_filename(new_name).strip()
                new_path = os.path.join(root, new_name)
                if file_path == new_path:
                    # skip, no rename needed
                    continue
                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed: {file_name} -> {new_name}")
                except OSError as e:
                    print(f"Error renaming {file_name} to {new_name}: {e}")
            else:
                print(f"Skipping: {file_name} (metadata not found)")

if __name__ == "__main__":
    # Specify the directory containing your EPUB files
    directory = input("Enter the path to your book collection: ").strip()
    if os.path.isdir(directory):
        rename_books(directory)
    else:
        print(f"{directory} is not a valid directory.")