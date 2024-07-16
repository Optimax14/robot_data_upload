import os
import zipfile
from boxsdk import OAuth2, Client

CLIENT_ID = 'ADD_CLIENT_ID'
CLIENT_SECRET = 'ADD_CLIENT_SECRET'
ACCESS_TOKEN = 'ADD_ACCESS_TOKEN'  
ROOT_FOLDER_ID = '0' # Change to directory of choice (default root dir) 

def zip_directory(directory_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                zipf.write(dir_path, os.path.relpath(dir_path, directory_path))

def upload_files_to_box(folder_id, local_directory):

    oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)
    client = Client(oauth2)
    
    zip_file_path = f'{local_directory}.zip'
    zip_directory(local_directory, zip_file_path)
    print(f"Directory {local_directory} zipped successfully to {zip_file_path}")

    box_folder = client.folder(folder_id)
    file_name = os.path.basename(zip_file_path)
    
    for file_name in os.listdir(local_directory):
        file_path = os.path.join(local_directory, file_name)
        if os.path.isfile(file_path):
            print(f"Uploading {file_name}...")
            uploaded_file = box_folder.upload(file_path, file_name)
            print(f"Uploaded {file_name} to Box with ID {uploaded_file.id}")

if __name__ == '__main__':
    local_directory_path = 'ADD/LOCAL/DIRECTORY/PATH'  # Update with your local directory path
    upload_files_to_box(ROOT_FOLDER_ID, local_directory_path)
