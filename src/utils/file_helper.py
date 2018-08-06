from os import listdir
from os.path import isfile, join


class filerHelper:
    def __int__(self):
        pass

    @staticmethod
    def get_files_from_a_dir(target_dir):
        return [f for f in listdir(target_dir) if isfile(join(target_dir, f))]
