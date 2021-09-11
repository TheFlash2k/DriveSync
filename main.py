#!/usr/bin/env python3
# Author: TheFlash2k
from modules.sync import Sync
from sys import argv

'''
The purpose of this main.py is to give an example of how easy it is to setup syncing using this API.
We're using the Sync API to read all the files from the 'local_dir' folder and then sync them to the SyncDrive folder in the google drive.
'''

if __name__ == "__main__":
    local_dir = "Drive"
    # Setting the folder name from either argv or local variable.
    folder_name = local_dir if len(argv) <= 1 else argv[1]

    sync = Sync (
        folder_name=folder_name,            # This will be the name of the folder on the local drive that will be synced with the google drive.
        parent_folder_name='DriveSync',     # The parent folder into which other folders will be created
        post_folder_name='Uploaded',        # The name of the folder into which all the files be copied to onto the local drive once they're uploaded.
        token_file='client_secret.json',    # The `json` file that will be generated from developers.google.com
        verbose=True                        # Setting verbosity to true so we can see what's going on
    )
    sync.init_sync()                        # Invoking the method to start syncing the data.
