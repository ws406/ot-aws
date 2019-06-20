import collections


class SortDictByKey:
    def __init__ (self):
        pass

    @staticmethod
    def sort(unsorted_dict):
        return sorted(unsorted_dict.items(), key=lambda x: int(x[0]))
