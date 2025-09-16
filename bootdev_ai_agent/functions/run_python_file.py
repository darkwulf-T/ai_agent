import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    working_dir_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(full_path)
    if not target_abs.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_abs):
        return f'Error: File "{file_path}" not found.'
    if not target_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        cp = subprocess.run([sys.executable, target_abs, *args], cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        out = cp.stdout or ""
        err = cp.stderr or ""
        stdout_part = f"STDOUT: {out.strip()}" if out else "STDOUT:"
        stderr_part = f"STDERR: {err.strip()}" if err else "STDERR:"
        parts = [stdout_part, stderr_part]
        if cp.returncode != 0:
            parts.append(f"Process exited with code {cp.returncode}")
        if cp.returncode == 0 and out == "" and err == "":
            return "No output produced."
        else:
            return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"]
    ),
)