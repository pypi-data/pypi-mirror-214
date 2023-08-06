import os
import shutil 

def read_lines(file_path):
    with open(file_path) as f:
            lines = f.readlines()
    return lines

def count_lines(file_path):
    return len(read_lines(file_path))

def count_folders(folder_path):
    return len(list_directories(folder_path))

def count_files(folder_path):
    return len(list_files(folder_path))

def get_file_info(file_path):
    split_path = os.path.splitext(file_path)
    file_name = file_path.split("/")[-1]
    file_extension = split_path[1]
    file_location = file_path.split("/" + file_name)[0]
    return [file_name, file_extension, file_location]

def get_file_name(file_path):
    return get_file_info(file_path)[0]

def get_file_extension(file_path):
    return get_file_info(file_path)[1]

def get_file_location(file_path):
    return get_file_info(file_path)[2]

def is_file(path):
    return os.path.isfile(path)
          
def is_folder(path):
    return os.path.isdir(path)

def is_existing(path):
    return os.path.exists(path) 

def list_directories(folder_path):
    return [
        d for d in (os.path.join(folder_path, d1) for d1 in os.listdir(folder_path))
        if os.path.isdir(d)
    ]

def list_files(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) if f[0] != "."]

def is_empty(folder_path):
    return len(os.listdir(folder_path)) == 0

def delete_file(file_path):
    os.remove(file_path)

def delete_folder(folder_path):
    shutil.rmtree(folder_path)