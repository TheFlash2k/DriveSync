from GD_API import GD_API, get_mime_type
import os

class Sync:
    def __init__(self, folder_name, parent_folder_name='AU-BBS', post_folder_name='Uploaded', token_file='client_secret.json', verbose=False):
        self.verbose = verbose
        self.folder_name = folder_name
        self.post_folder = post_folder_name
        # Validating if each of these folders exists or not.
        self.__validate__()
        # Getting all the files from the folder
        files = os.listdir(folder_name)
        # Getting the absolute path of each file and storing it in the list
        self.files = list()
        self.delim = '\\' if os.name == 'nt' else '/'
        for file in files:
            abs_file = os.path.abspath(folder_name + self.delim + file)
            if os.path.isfile(abs_file):
                self.files.append(abs_file)

        # A tuple containing all the folders that will be checked for in the drive.
        self.drive_folders = ('Images', 'Documents', 'Audios', 'Videos', 'Texts', 'Applications', 'Un-Identified')
        
        # Creating an instance of the API that will be used to handle everything
        self.api = GD_API(
            client_token_file=token_file, 
            verbose=self.verbose
        )
        
        # Name of the parent folder
        self.parent_folder = parent_folder_name

    # This "private" method will check and create all the folders in the google drive.
    def __create__(self):
        # Checking if the parent directory exists or not
        if not self.api.check_folder_exists(folder_name=self.parent_folder):
            if self.verbose:
                print("[*] You're running this script for the first time. Please wait while the necessary folder(s) are being created on the drive for you.")
            # Creating the parent and all the sub-parent folders:
            self.api.create_folder(folder_name=self.parent_folder)
            # Creating all the sub-folders:
            for folder in self.drive_folders:
                self.api.create_folder(folder_name=folder, parent_folder_name=self.parent_folder)
            if self.verbose:
                print("[*] Created all the folders.")
        # If the parent directory exists, we still need to check if any of the sub-folder is not created, so we will create those sub-folders:
        else:
            if self.verbose:
                print("[+] Parent directory found. Checking for any missing sub-directories.")
            for folder in self.drive_folders:
                if not self.api.check_folder_exists(folder_name=folder):
                    self.api.create_folder(folder_name=folder, parent_folder_name=self.parent_folder)
                    if self.verbose:
                        print(f"[*] {folder} was missing. Creating it now.")

    # This "private" method will return the folder name into which a ceratin file will be uploaded in the drive
    def __get_folder__(self, file_name):
        mime = get_mime_type(file_name)
        # We're checking this because these are are primarily documents but they will be stored in Applications because of their mime type
        document_types = ('pdf', 'powerpoint', 'presentation', 'excel', 'spreadsheet', 'json', 'document', 'word', 'epub', 'txt')
        for doc in document_types:
            if doc in mime:
                return 'Documents'
        # Otherwise, just getting the folder name from mime type.
        try:
            return mime.split('/')[0].capitalize() + 's'
        except AttributeError:
            return 'Un-Identified'

    # Main method to initialize syncing
    def init_sync(self):
        self.__create__() # Checking if folders exists.
        if self.verbose:
            print(f"[*] Files to be uploaded: {self.files}")
        for file in self.files:
            folder = self.__get_folder__(file)
            print(f"[+] Uploading {file}...")
            self.api.upload_file(file, parent_folder_name=folder)

        print(f"[+] Syncing successful.", end='')
        if self.verbose:
            print(f"Transfering all files from {self.folder_name} to {self.post_folder}", end='')
        print()
        self.__post__()
    
    # A "private" method to validate if either the "Drive" or "Uploaded folder exists or not."
    def __validate__(self):
        # Checking if folder_name is an existing directory or not:
        if not os.path.isdir(self.folder_name):
            print(f"[-] Folder {self.folder_name} doesn't exist. Please provide a valid folder name that you want to sync")
            exit(1)
        # Creating a folder named "Uploaded" that will contain all the files from the Drive folder once they're uploaded.
        if not os.path.isdir(self.post_folder):
            os.mkdir(self.post_folder)

    # This method will move each file from "{self.folder_name}" to "{self.post_folder}" directory
    def __post__(self):
        post_path = os.getcwd() + self.delim + self.post_folder + self.delim
        old_path = self.files[0][::-1]
        old_path = old_path[old_path.find(self.delim):][::-1]
        for file in self.files:
            file_name = file[::-1].split(self.delim)[0][::-1]
            os.rename(file, post_path + file_name)
        if self.verbose:
            print(f"[+] Moved {len(self.files)} file(s) from {old_path} to {post_path}")
