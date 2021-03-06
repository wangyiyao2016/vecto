import fnmatch
import os
from vecto.utils.metadata import WithMetaData


class Dataset(WithMetaData):
    """
    Container class for stock datasets.
    Arguments:
        path (str): local path to place files
    """

    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("test dataset dir does not exist:" + path)
        super().__init__(path)
        self.path = path

    def file_iterator(self):
        for root, _, filenames in os.walk(self.path):
            for filename in fnmatch.filter(sorted(filenames), '*'):
                if filename.endswith('json'):
                    continue
                yield(os.path.join(root, filename))


def get_dataset(name):
    # TODO: get dataset dir from config
    dir_datasets = "/home/blackbird/.vecto/datasets"
    path_dataset = os.path.join(dir_datasets, name)
    dataset = Dataset(path_dataset)
    return dataset
    # TODO: check if it seats locally
    # TODO: download
