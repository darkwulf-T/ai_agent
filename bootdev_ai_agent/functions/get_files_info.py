import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, directory)
    target_abs = os.path.abspath(full_path)
    if not target_abs.startswith(working_dir_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_abs):
        return f'Error: "{directory}" is not a directory'

    try:
        dir_content = os.listdir(target_abs)
        string_list = []
        for con in dir_content:
            con_path =os.path.join(target_abs, con)
            file_size = os.path.getsize(con_path)
            is_dir =  os.path.isdir(con_path)
            con_string = f"- {con}: file_size={file_size}, is_dir={is_dir}"
            string_list.append(con_string)
        result = "\n".join(string_list)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)