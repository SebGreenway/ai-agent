from google.genai import types
import os

def get_files_info(working_directory, directory=None):
    """
    Get information about files and directories in a specified directory within the working_directory.

    Args:
        working_directory (str): The root working directory.
        directory (str, optional): Relative path within the working_directory.

    Returns:
        str: A formatted string describing each item, or an error string if invalid.
    """
    try:
        # If no directory is specified, use the working_directory itself
        if directory:
            resolved_path = os.path.join(working_directory, directory)
        else:
            resolved_path = working_directory

        # Normalize paths
        resolved_path = os.path.abspath(resolved_path)
        working_directory = os.path.abspath(working_directory)

        # Check that the resolved path is within the working directory
        if not resolved_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path exists
        if not os.path.exists(resolved_path):
            return f'Error: The directory "{directory}" does not exist within the working directory'

        # Check if the path is a directory
        if not os.path.isdir(resolved_path):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for item in os.listdir(resolved_path):
            item_path = os.path.join(resolved_path, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            entries.append(f'- {item}: file_size={file_size} bytes, is_dir={is_dir}')

        return "\n".join(entries)

    except Exception as e:
        return f'Error: {str(e)}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, "
                    "relative to the working directory. "
                    "If not provided, lists files in the working directory itself."
                ),
            ),
        },
    ),
)




schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to read, inside the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within the working directory. Creates the file if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to write to, inside the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute, inside the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)