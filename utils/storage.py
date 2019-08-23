from pathlib import PurePath

from utils.config import STORAGE_DIR


def local_directory(bucket, file_id):
    if '/' in file_id:
        id_folders = PurePath(file_id).parent
    else:
        id_folders = ''
    return STORAGE_DIR / bucket / id_folders


def build_local_path(bucket_id: str, object_id: str):
    return local_directory(bucket_id, object_id) / PurePath(object_id).name
