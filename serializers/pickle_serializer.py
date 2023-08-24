"""read binary protocols for serializing and de-serializing a Python object structure files and turn them into a python data object"""
# import standard modules
import os
import imp
import warnings
import pickle

# import custom modules
# from modules import serializer_object
module_path = os.path.dirname(__file__)
fp, pathname, description = imp.find_module('serializer_object', [module_path + '/modules'])
serializer_object = imp.load_module('serializer_object', fp, pathname, description)

class PickleSerializer(serializer_object.DataSerializer):
    """Pickle serializer for manipulation of pickle data files, It is a non-human-readable format!"""
    READ_DATA = []
    # for information only, shows which indices have been updated inside the Pickle file
    UPDATE_DATA = []
    # identify how the Pickle file is organized, this is important as each Pickle data file is written differently!
    DATA_KEYS = None
    ROW_NAMES = None
    FILE_NAME = ""
    EXT_NAME = "pickle"
    def __init__(self, *args, **kwargs):
        """Constructor method"""
        self.READ_DATA = PickleSerializer.READ_DATA
        if self.READ_DATA:
            self.UPDATE_DATA = [1]
        self.EXT_NAME = PickleSerializer.EXT_NAME
        self.ROW_NAMES = PickleSerializer.ROW_NAMES
        super(serializer_object.DataSerializer, self).__init__(*args, **kwargs)

    def save_file(self, path_name):
        """save the updated data to a file if changes are made to the original data
        :param path_name: the data file name to save into
        :returns: True for success.
        :rtype: boolean"""
        if not self.UPDATE_DATA:
            warnings.warn("No changes are made to the file!")
            return []
        self._check_dir(path_name)
        serializer_object.set_ext(path_name, self.EXT_NAME)
        with open(path_name, 'wb') as pickle_file:
            pickle.dump(self.READ_DATA, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
        pickle_file.close() # precaution
        return self.READ_DATA

    def load_file(self, path_name):
        """loads and reads the contents of the XML file
        :param path_name: provide an alternative path name
        :type path_name: str
        :returns: list of dictionaries from the file provided
        :rtype: list
        """
        self._check_path(path_name)
        with open(path_name, 'rb') as pickle_file:
            self.READ_DATA = data_dict = pickle.load(pickle_file)
        pickle_file.close() # precaution
        self.ROW_NAMES = self._get_data_rows_from_data()
        self._analyze_data_indices()
        return data_dict

    def get_data_rows(self, path_name):
        """Returns the top-most row names for information
        :param path_name: file-path name
        :type path_name: str
        :returns: row list data"""
        self._check_path(path_name)
        with open(path_name, 'rb') as pickle_file:
            data_dict = pickle.load(pickle_file)
        return data_dict[0].keys()
#___________________________________________________________________________________________________
# pickle_serializer.py