import os
from .config import MAX_FILE_LENGTH

def get_file_content(working_directory, file_path):
    """
    Reads and returns the content of a file given a working directory and file path.
    - If the file is outside the working directory, returns an error string.
    - If it doesn't exist or is not a regular file, returns an error string.
    - If reading the file raises an error, returns an error string.
    - If the file is longer than MAX_FILE_LENGTH, truncates it and appends a message.
    """
    try:
        # Normalize paths
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if the path is inside the working directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'

        # Check if the path exists and is a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Try reading content
        with open(full_path, 'r') as f:
            content = f.read()

        # Truncate if needed
        if len(content) > MAX_FILE_LENGTH:
            truncated = content[:MAX_FILE_LENGTH]
            truncated += f'\n[...File "{file_path}" truncated at {MAX_FILE_LENGTH} characters]'
            return truncated

        return content

    except Exception as e:
        return f"Error: {str(e)}"
