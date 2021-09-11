# DriveSync - A much easier API to upload and create files/folders in Google Drive

A simple Python3 based API which easy to use and user friendly function(s) to interact with the Google Drive API.

# Usage:
There are two different classes that are usable.
- ***Sync***
- ***GD_API***

Note: To know how to generate the json token, read [Google Drive API Token Generation](token_gen.md)

## Sync:
The Sync class is built upon the GD_API class and all it simply does is upload files from a certain folder into another folder within the drive in an organized manner.
The Sync class will firstly create a parent folder from the argument `parent_folder_name`. Then, within that folder, different folders will be created such as, `Images, Audios, Videos, Documents` etc. The main reason behind creation of these folders is to keep everything organized during the syncing process. Everything is sync based on their mimetypes.

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

sync.init_sync() # This method will control everything, no need to configure anything else, just pass the valid arugments to the constructor and everything will work fine.
```

## GD_API:
This class simplifies everything from creation of the service to interact with the Google API and then invoking other methods and dealing with Mime-Types for each thing.
I've managed to simplify each task so that it's as easy as invoking a method with correct arguments. These are a few important methods which are as easy to invoke as a `sum` function with 2 parameters (I'm bad at giving references ;-;). Following are the methods:
```python
# Details for each method is provided in the Examples section
get_files_list()
get_folder_id(folder_name)
get_folder_name(folder_id)
check_folder_exists(folder_name=None,folder_id=None)
create_folder(folder_name,parent_folder_name=None,parent_folder_id=None)
upload_file(file_name,parent_folder_name=None,parent_folder_id=None)
```

### Example:
```python
from modules.GD_API import GD_API

# This constructor will only take the token file as an argument, and then will validate this token before returning a handle of the original google API.
api = GD_API(
    client_token_file='client_secret.json'
)

# Available methods:

# This will return all the files in the drive of that particular user
file_list = api.get_files_list()

# This will return the id of a folder name that is passed as its argument.
api.get_folder_id(
    folder_name='DriveSync'
)

# This will return the name of the folder who's id is passed as the argument.
api.get_folder_name(
    folder_id='1DqW-HBoC3W4BTcJUmHTEu871AplDwhTa'
)

# This method takes two values as its argument but only one can be set when called.
# This method will look for the existence of a folder in the drive, the existence can be on the basis of the id or the name.
## Examples:
api.check_folder_exists(
    folder_name=None,
    folder_id=None
)
# For Name:
api.check_folder_exists(
    folder_name='DriveSync',
    folder_id=None
) # Here you can also just provide folder_name as folder_id is already default set to None
# For ID:
api.check_folder_exists(
    folder_name=None,
    folder_id='1DqW-HBoC3W4BTcJUmHTEu871AplDwhTa'
) # Here you can also just provide folder_id as folder_name is already default set to None

# This method will take as its argument at most 2 values, one will be the folder name and the other will be
# either the parent folder name or its id. The parent folder means that you want to create the new folder inside an already existing folder that will be its parent.
# You can call the function using the following conventions:
api.create_folder('DriveSync') # This will create a folder named 'DriveSync' in the root of the Drive.
api.create_folder(
    folder_name='DriveSync',
    parent_folder_name=None,
    parent_folder_id=None
) # This will be the same as the above calling.
# Using name:
api.create_folder('DriveSync', parent_folder_name='Parent') # This will create a folder named 'DriveSync' within another folder 'Parent'
api.create_folder(
    folder_name='DriveSync',
    parent_folder_name='Parent',
    parent_folder_id=None
) # This will be the same as the above calling.
# Using ID:
api.create_folder('DriveSync', parent_folder_id='1DqW-HBoC3W4BTcJUmHTEu871AplDwhTa') # This will create a folder named 'DriveSync' within another folder who's id is : '1DqW-HBoC3W4BTcJUmHTEu871AplDwhTa'
api.create_folder(
    folder_name='DriveSync',
    parent_folder_name=None,
    parent_folder_id='1DqW-HBoC3W4BTcJUmHTEu871AplDwhTa'
) # This will be the same as the above calling.

# This method will be used to upload files to the drive. All the mime-types and everything has been taken care of behind the scenes and uploading is as easy as invoking this method.
api.upload_file(
    file_name='Test.txt',
    parent_folder_name=None,
    parent_folder_id=None
) # This will upload the file 'Test.txt' to the root of the Drive.
# Same as all the other methods, you can upload files within a certain directory and what not.
```
