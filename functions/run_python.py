import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working direct'

        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'

        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            ["python3", full_path],
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        output_parts = []

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"
