from os import listdir
from os.path import isfile, join
import json
import numpy as np


class filerHelper:
    def __int__(self):
        pass

    @staticmethod
    def get_files_from_a_dir(target_dir):
        return [f for f in listdir(target_dir) if isfile(join(target_dir, f))]

    @staticmethod
    def save_file(file_name, data):
        data_type = type(data)
        print(data_type)
        if data_type is np.ndarray:
            np.savetxt(file_name, data, delimiter=",")
        elif data_type is json:
            file = open(file_name, 'w+')
            file.write(json.dumps(data))
            file.close()
        else:
            raise TypeError
