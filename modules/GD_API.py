from imports import *

class GD_API:
    def __init__(self, client_token_file='client_secret.json', verbose=True):
        self.verbose = verbose
        if self.verbose:
            print("[+] Initiliazing API...")
        CLIENT_SECRET_FILE = client_token_file
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPE = ['https://www.googleapis.com/auth/drive']
        self.service_handler = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)
        if not self.service_handler:
            exit(1)
        if self.verbose:
            print("[+] API Successfully Initiliazed")

    # returns all the name of the files as a list
    def get_files_list(self):
        return self.service_handler.files().list().execute()['files']

    # returns a folder id based on the name
    def get_folder_id(self, folder_name):
        for item in self.get_files_list():
            if item['name'] == folder_name:
                return item['id']
        return None

    # Returns a folder name based on id:
    def get_folder_name(self, folder_id):
        if not folder_id:
            return "root"
        for item in self.get_files_list():
            if item['id'] == folder_id:
                return item['name']
        return None

    # Check if a folder exists based on id or name
    def check_folder_exists(self, folder_name=None, folder_id=None):
        if not folder_id and not folder_name:
            return False
        for item in self.get_files_list():
            if folder_name:
                if item['name'] == folder_name:
                    return True
            if folder_id:
                if item['id'] == folder_id:
                    return True
        return False
    
    # This function checks if the parent_folder_name of id has been provided
    # and returns the id if name is provided as a list, or id if the id is provided,
    # if neither are provided, returns None.
    def check_if_parent(self, parent_folder_name, parent_folder_id):
        if parent_folder_name and parent_folder_id:
            print("[x] Provide either ID or name. Both will not work!")
            return

        parent_id = None
        if parent_folder_id:
            parent_id = parent_folder_id
        elif parent_folder_name:
            parent_id = self.get_folder_id(folder_name=parent_folder_name)
        parent_id = [parent_id] if parent_id else None
        return parent_id
    
    # This method will create a folder. If the parent folder doesn't exists, returns None
    # The folder_name can either be a list or string, it will work either way.
    def create_folder(self, folder_name, parent_folder_name=None, parent_folder_id=None):
        
        parent_id = self.check_if_parent(parent_folder_name, parent_folder_id)
        meta_data = {'name' : '', 'mimeType' : 'application/vnd.google-apps.folder', 'parents' : parent_id}

        if type(folder_name) == list:
            for folder in folder_name:
                meta_data['name'] = folder
                self.service_handler.files().create(body=meta_data).execute()
            if self.verbose:
                print(f"[+] Succesfully created {len(folder_name)} folders")
        elif type(folder_name) == str:
            meta_data['name'] = folder_name
            self.service_handler.files().create(body=meta_data).execute()
            if self.verbose:
                print(f"[+] Succesfully created {folder_name}", end='')
        if self.verbose:
            print(f" inside '{self.get_folder_name(parent_id[0])}' folder!") if parent_id else print('!')

    # This method will upload files. Note, pass the full path to the file to upload the file.
    # You can also the pass the folder name or id to upload the file inside a specific folder.
    def upload_file(self, file_name, parent_folder_name=None, parent_folder_id=None):
        parent_id = self.check_if_parent(parent_folder_name, parent_folder_id)
        if type(file_name) == str:
            files = [file_name]
        elif type(file_name)  == list or type(file_name) == tuple:
            files = file_name
        else:
            print(f"[-] Invalid file name {file_name} provided")
            exit(1)
        mime_types = list()

        # Setting only the file name of each file
        file_names = list()

        delim = '\\' if os.name == 'nt' else '/'
        for file in files:
            file_names.append(file[::-1].split(delim)[0][::-1])

        # Getting the mime type for each file_name
        for file in files:
            mime_types.append(get_mime_type(file))
        parent_name = parent_folder_name if not parent_folder_id else self.get_folder_name(parent_folder_id)
        for file, name, mime_type in zip(files, file_names, mime_types):
            meta_data = { 'name' : name, 'parents' : parent_id }
            mediaObj = MediaFileUpload(file,mimetype=mime_type)
            self.service_handler.files().create(body=meta_data, media_body=mediaObj, fields='id').execute()
            if self.verbose:
                print(f"[*] Uploaded {name} to {parent_name}.")
        if self.verbose:
            print(f"[+] Uploaded {len(files)} file(s) succesfully!")