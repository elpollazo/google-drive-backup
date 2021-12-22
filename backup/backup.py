#!/usr/bin/python3

import os
import sys

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def conditional():
    if len(sys.argv) != 2:
        print('Ussage: python3 backup.py [folder name in Google Drive]')
        sys.exit(1)

def get_id(drive, parent_folder_id, name):
    """
    Gets file or folder ID.
    """
    file_list = GoogleDriveFileList()
    file_list = drive.ListFile({
        'q': f"'{parent_folder_id}' in parents and trashed=false"
        }).GetList()
    
    return [file_list[i]['id'] for i in range(len(file_list)) if file_list[i]['title'] == name][0]

def upload_files(folder, parent_folder_id):
    """
    Uploads/updates all files recusively.
    """
    for file in [f.path for f in os.scandir(folder) if f.is_file()]:
        file_name = file.split('/')[-1]
        try:
            fldr = drive.CreateFile({'id': get_id(drive, parent_folder_id, file_name)})
            fldr.SetContentFile(file)
            fldr.Upload()
            print(f'Updating file: {file}')

        except:
            file_metadata = {'title': file_name, 'parents': [{'id': parent_folder_id, 'kind': "drive#childList"}]}
            fldr = drive.CreateFile(file_metadata)
            fldr.SetContentFile(file)
            fldr.Upload()
            print(f'Uploading file: {file}')

    for subdir in [f.path for f in os.scandir(folder) if f.is_dir()]:
        folder_name = subdir.split('/')[-1]
        try:
            print(f'Scanning folder: {subdir}')
            upload_files(subdir, get_id(drive, parent_folder_id, folder_name))

        except:
            body = {'title': folder_name,
                    'mimeType': "application/vnd.google-apps.folder",
                    'parents': [{'id': parent_folder_id}]}

            fldr = drive.CreateFile(body)
            fldr.Upload()
            print(f'New folder created: {folder_name}')
            upload_files(subdir, get_id(drive, parent_folder_id, folder_name))

if __name__ == '__main__':
    """
    Checks if the folder specified in arguments exists in Google Drive. If not, creates it.
    """
    conditional()
    try:
        upload_files('..', get_id(drive, 'root', sys.argv[1]))

    except:
        body = {'title': sys.argv[1],
                'mimeType': "application/vnd.google-apps.folder",
                'parents': [{'id': 'root'}]}

        fldr = drive.CreateFile(body)
        fldr.Upload()
