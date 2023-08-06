import os
from pathlib import Path
import logging
import shutil


class NTTFileSystem():
    @classmethod
    def create_folder(cls, folder_name: str) -> None:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)        
        else:
            logging.warn(f"The {folder_name} exists.")

    @classmethod
    def clone_file(cls, src_path: str, des_path: str) -> None:
        path = Path(des_path)
        if path.is_dir():
            final_path = os.path.join(des_path, os.path.split(src_path)[-1])
        else:
            final_path = des_path

        shutil.copy2(src_path, final_path)