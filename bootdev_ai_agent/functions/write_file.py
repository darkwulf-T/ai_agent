import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(full_path)
    if not target_abs.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        parent = os.path.dirname(target_abs)
        if parent:
            os.makedirs(parent, exist_ok=True)
    except Exception as e:
        return f"Error: {str(e)}"
    
    try:
        with open(target_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"