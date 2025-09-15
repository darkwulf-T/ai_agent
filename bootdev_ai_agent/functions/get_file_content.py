import os
from config import *

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(full_path)
    if not target_abs.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_abs, "r") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS]
                content = content + f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f"Error: {str(e)}"