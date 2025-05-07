import re
UNKNOWN = 'unknown'

def sanitize_filename(name):
    """
    Sanitize a string to make it safe for use as a file name.
    Removes or replaces invalid characters.
    """
    # Replace invalid characters with an underscore
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', name)
    # Strip leading/trailing whitespace and dots
    return sanitized.strip().strip('.')