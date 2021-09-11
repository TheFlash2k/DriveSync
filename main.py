#!/usr/bin/env python3
from modules.sync import Sync
import sys

if __name__ == "__main__":

    try:
        folder_name = sys.argv[1]
    except IndexError:
        folder_name = "Drive" # The folder that you want to upload.
    sync_handle = Sync(folder_name=folder_name, parent_folder_name='SyncDrive')
    sync_handle.init_sync()