from google.genai import types
from functions.get_files_info import get_files_info
from functions.file_utils import get_file_content
from functions.file_writer import write_file
from functions.run_python import run_python_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Map function names to actual callables
    functions_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call_part.name
    function_to_call = functions_map.get(function_name)

    # If unknown function, return tool response describing the error
    if not function_to_call:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ],
        )

    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    try:
        function_result = function_to_call(**args)
    except Exception as e:
        function_result = f"Error while calling function: {e}"

    # ✅ Return result wrapped as a proper tool response
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
