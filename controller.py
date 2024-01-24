import requests
import zipfile
import io
import os

def controller_files(controller_type, theromfs_folder):
    import getpass
    import shutil
    username = getpass.getuser()
    directory_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/smo/Controllers"

    if controller_type.lower() == "xbox":
        # Navigate into the Xbox folder, then into romfs
        copy_source_folder = os.path.join(directory_path, 'Xbox', 'romfs', 'LocalizedData')
    elif controller_type.lower() == "playstation":
        # Navigate into the Playstation folder, then into romfs
        copy_source_folder = os.path.join(directory_path, 'Playstation', 'romfs', 'LocalizedData')
    else:
        print(f"Unsupported controller type: {controller_type}")
        return

    # Copy the specified folder to theromfs_folder
    shutil.copytree(copy_source_folder, os.path.join(theromfs_folder, "LocalizedData"))

    print(f"Controller files for {controller_type} successfully downloaded and copied to {theromfs_folder}")



#this fiel should:
# define function and pass in controller_type
#if  controller type is switch, do nothing return to function
#if controller type = "Xbox", download the file and put it in the right place
#if controller type = "Playstation", download the file and put it in the right place

#the files for controller and xbox are in the same place, on github, and need to be fetched from requests. you need to download zip_url = "https://github.com/fayaz12g/aar-files/raw/main/smo/Controllers.zip", which contains one folder called Xbox and one called Playstation. then the function needs to take the correct one and copy it over to "input_folder" which is a variavel path passed in
