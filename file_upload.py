import os
from boxsdk import OAuth2, Client

CLIENT_ID = 'ADD_CLIENT_ID'
CLIENT_SECRET = 'ADD_CLIENT_SECRET'
ACCESS_TOKEN = 'ADD_ACCESS_TOKEN'  
ROOT_FOLDER_ID = '0' # Change to directory of choice (default root dir) 

local_directory_path = 'ADD/DIRECTORY/PATH/FOLDER'

def upload_files_to_box(folder_id, local_directory):
    oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)
    client = Client(oauth2)
    
    box_folder = client.folder(folder_id)
    
    for file_name in os.listdir(local_directory):
        file_path = os.path.join(local_directory, file_name)
        if os.path.isfile(file_path):
            print(f"Uploading {file_name}...")
            uploaded_file = box_folder.upload(file_path, file_name)
            print(f"Uploaded {file_name} to Box with ID {uploaded_file.id}")

if __name__ == '__main__':
    upload_files_to_box(ROOT_FOLDER_ID, local_directory_path)