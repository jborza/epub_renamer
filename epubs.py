# called on an epub file
import os
from ebooklib import epub

from utils import UNKNOWN, sanitize_filename

def get_metadata_epub(epub_path):
    """Extract author and title metadata from an EPUB file."""
    try:
        book = epub.read_epub(epub_path)
        title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else UNKNOWN
        author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else UNKNOWN
        return author, title
    except Exception as e:
        print(f"Error reading {epub_path}: {e}")
        return None, None

# def rename_epubs(directory):
#     """Rename all EPUB files in the given directory."""
#     for root, _, files in os.walk(directory):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)
#             author, title = get_metadata(file_path)
#             if author.lower() == UNKNOWN or title.lower() == UNKNOWN:
#                 print(f"Skipping: {file_name} (metadata not found)")
#                 continue

#             if author and title:
#                 new_name = f"{author} - {title}.epub"
#                 new_name = sanitize_filename(new_name)
#                 new_path = os.path.join(root, new_name)
#                 if file_path == new_path:
#                     # skip, no rename needed
#                     continue
#                 try:
#                     os.rename(file_path, new_path)
#                     print(f"Renamed: {file_name} -> {new_name}")
#                 except OSError as e:
#                     print(f"Error renaming {file_name} to {new_name}: {e}")
#             else:
#                 print(f"Skipping: {file_name} (metadata not found)")

# if __name__ == "__main__":
#     # Specify the directory containing your EPUB files
#     epub_directory = input("Enter the path to your EPUB collection: ").strip()
#     if os.path.isdir(epub_directory):
#         rename_epubs(epub_directory)
#     else:
#         print(f"{epub_directory} is not a valid directory.")