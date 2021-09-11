# DriveSync - A much easier API to upload and create files/folders to Google Drive

A simple Python3 based API which easy to use and user friendly function(s) to interact with the Google Drive API.

# Usage:
There are two different classes that are usable.
- ***Sync***
- ***GD_API***

Note: To know how to generate the json token, read [Google Drive Token Generation](token_gen.md)

## Sync:
The Sync class is built upon the GD_API class and all it simply does is upload files from a certain folder into another folder within the drive in an organized manner.

### Example:
```python
from modules.sync import *
 
sync = Sync (
    folder_name="Folder",            # This will be the name of the folder on the local drive that will be synced with the google drive.
    parent_folder_name='DriveSync',  # The parent folder into which other folders will be created
    post_folder_name='Uploaded',     # The name of the folder into which all the files be copied to onto the local drive once they're uploaded.
    token_file='client_secret.json', # The `json` file that will be generated from developers.google.com
    verbose=False
)
```
