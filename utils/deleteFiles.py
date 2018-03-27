# delete-files.py
# Author: Moises Marin
# Date: November 27, 2017
# Purpose: To delete files from a folder
#
#
import shutil
import os

def empty_folder(folder_path):
    if folder_path:
        shutil.rmtree(folder_path)
        os.system("mkdir "+folder_path)
        return "Removing: " + folder_path
    else:
        return "No arguments!"
