import os
from pathlib import Path

SERIALIZER_DIRNAME = "serializers"
DATA_DIRNAME = "PersonalData"

class Serializer:
    """Abstract class for use as a base for context-specific data serialization"""
    def __init__(self):
        pass
    def save_file(self):
        pass
    def load_file(self):
        pass
    def append_data(self):
        pass
    def update_data(self):
        pass
    def remove_data(self):
        pass

class DataSerializer(Serializer):
    """A Generalized Data Serializer class for use as a basis of serializing data-extension-context specific files"""
    READ_DATA = None
    UPDATE_DATA = None
    DATA_KEYS = None
    FILE_NAME = ""
    EXT_NAME = ""
    SOURCE_DIR_PATH = ""
    def __init__(self, source_file=None, source_dir_path=None):
        """Constructor method"""
        DataSerializer.FILE_NAME = source_file
        DataSerializer.SOURCE_DIR_PATH = source_dir_path
        self.READ_DATA = DataSerializer.READ_DATA
        if self.READ_DATA:
            self.UPDATE_DATA = [1]
        super(Serializer, self).__init__()

    def update_data_by_name(self, person_name, **kwargs):
        """find and update the existing contents of the data file
        :param person_name: insert data through a person_name
        :type person_name: str
        :returns: changed personal data
        :rtype: dict"""
        name_org = len(self.DATA_KEYS['name'])
        if name_org > 1:
            given_name, sur_name = person_name.split(' ')
            print("Person Name: {} {}".format(given_name, sur_name))
        else:
            sur_name = person_name
            print("Person Name: {}".format(sur_name))
        cur_index = 0
        change_data = None
        # get the index of the data based on name only
        for idx, data in enumerate(self.READ_DATA):
            for d_key, d_value in data.items():
                if sur_name in d_value:
                    cur_index = idx # index where the name is found in the file
                    change_data = data
                    if cur_index not in self.UPDATE_DATA:
                        self.UPDATE_DATA.append(cur_index)
                    break
        if not data:
            raise ValueError("{} Not found in data. Consider appending the information for this person:".format(person_name))
        print("Data found for {}".format(person_name))
        # change the data based on the parameters given
        if "address" in kwargs:
            address = kwargs['address']
            address_key = self.ROW_NAMES[self.DATA_KEYS['address'][0]]
            change_data[address_key] = address
        if "phone" in kwargs:
            phone = kwargs['phone']
            phone_key = self.ROW_NAMES[self.DATA_KEYS['phone'][0]]
            change_data[phone_key] = phone
        self.READ_DATA[cur_index] = change_data
        return change_data

    def _check_path(self, path_name=None):
        """checks if the path name contains a valid file path and associated extension name for loading
        :param path_name: optional file path name
        :type path_name: str"""
        if not path_name:
            path_name = get_default_data_directory_path()
        if not is_file(path_name) or not has_ext(path_name, self.EXT_NAME):
            raise IOError("Invalid Data File-Path Provided! Requires file-type: {}".format(self.EXT_NAME))
        return path_name

    def _check_dir(self, path_name=None):
        """checks if the path name directory is valid for saving over new files
        :param path_name: file path name to check directory strings
        :type path_name: string values"""
        if not path_name:
            path_name = get_default_data_directory_path()
        if not is_dir(get_directory_name(path_name)):
            raise IOError("Invalid Directory Given for file-name:\n{}".format(path_name))

    def _analyze_data_indices(self):
        """For Information only: define how the data from the .csv file will be 
        analyzed based on the original CSV data file rules, (some files have separate naming conventions, for example)
        :returns: {'phone': [0], 'name': [1], 'address': [2]}
        :rtype: dict"""
        # print("Analyzing Data Indices.")
        organizer = {}
        for key_data in self.READ_DATA:
            idx = 0
            for k in key_data.keys():
                if 'name' in k.lower():
                    if 'name' not in organizer:
                        organizer['name'] = []
                    if idx not in organizer['name']:
                        organizer['name'].append(idx)
                if 'phone' in k.lower():
                    if 'phone' not in organizer:
                        organizer['phone'] = []
                    if idx not in organizer['phone']:
                        organizer['phone'].append(idx)
                if 'address' in k.lower():
                    if 'address' not in organizer:
                        organizer['address'] = []
                    if idx not in organizer['address']:
                        organizer['address'].append(idx)
                idx += 1
        self.DATA_KEYS = organizer
        return self.DATA_KEYS

    def append_data(self, **kwargs):
        """add new contents of data to the file
        :param kwargs: name=None, address=None, phone=None
        :returns: appended data
        :rtype: dict"""
        add_data = {}
        if "name" in kwargs:
            person_name = kwargs['name']
        if not len(person_name.split(' ')) == 2:
            raise ValueError("Must enter a proper Given Name, SurName!")
        if not "name" in kwargs:
            raise ValueError("Please Give a name!")
        name_org = len(self.DATA_KEYS['name'])
        if name_org > 1:
            given_name, sur_name = person_name.split(' ')
            add_data[self.ROW_NAMES[self.DATA_KEYS['name'][0]]] = given_name
            add_data[self.ROW_NAMES[self.DATA_KEYS['name'][1]]] = sur_name
        else:
            sur_name = person_name
            add_data[self.ROW_NAMES[self.DATA_KEYS['name'][0]]] = sur_name
        if "address" in kwargs:
            address = kwargs['address']
            add_data[self.ROW_NAMES[self.DATA_KEYS['address'][0]]] = address
        if "phone" in kwargs:
            phone = kwargs['phone']
            add_data[self.ROW_NAMES[self.DATA_KEYS['phone'][0]]] = phone
        # append this data to the main read data variable
        self.READ_DATA.append(add_data)
        # confirm with the class object that the data has been updated succesfully
        self.UPDATE_DATA.append(len(self.READ_DATA) + 1)
        return add_data

    def _get_data_rows_from_data(self):
        """Returns the top-most row names for information
        :param path_name: file-path name
        :type path_name: str
        :returns: row list data"""
        return self.READ_DATA[0].keys()

    @property
    def read_data(self):
        return self.read()
    @property
    def file_name(self):
        return self.FILE_NAME
    @property
    def is_directory_valid(self):
        if has_ext(self.FILE_NAME):
            return is_dir(get_directory_name(self.FILE_NAME))
        return is_dir(self.FILE_NAME)
    @property
    def is_file_valid(self):
        return is_file(self.FILE_NAME)
    @property
    def is_data_valid(self):
        return isinstance(self.READ_DATA, dict)
    @property
    def has_data(self):
        return bool(self.READ_DATA)

def get_default_serializer_path():
    """returns a default location of serializer directory path
    :return: directory path name
    :rtype: str"""
    cur_dir_name = get_directory_name(get_directory_name(__file__))
    module_path = Path("{}\\{}".format(cur_dir_name, SERIALIZER_DIRNAME)).__str__()
    return module_path

def get_default_data_directory_path():
    """
    return the _relative_ directory path name for data.
    :return: directory path name
    :rtype: str
    """
    current_path = get_directory_name(get_directory_name(__file__))
    win_path = Path("{}\\{}".format(current_path, DATA_DIRNAME))
    if not win_path.exists():
        raise IOError("TestCases Folder Does Not Exist!")
    return win_path.__str__()

def get_directory_name(file_name):
    """
    return the directory name from the file name.
    :param: file_name directory path to file
    :type file_name: str
    :return: directory path name
    :rtype: str
    """
    return os.path.dirname(file_name)

def is_file(file_name):
    """
    checks if the file name is valid
    :param file_name: check this file name for validity
    :type file_name: str
    :return: True for success. False for failure
    :rtype: boolean
    """
    return os.path.isfile(file_name)

def is_dir(file_name):
    """
    checks if the directory name is valid
    :param file_name: check this directory name for validity
    :type file_name: str
    :return: True for success. False for failure
    :rtype: boolean
    """
    return os.path.isdir(file_name)

def has_ext(file_name, ext_name=""):
    """
    check if the file name string contains the extension name
    :param file_name: <str> file name to check
    :param ext_name: <str> check this extension string name
    :return: True for yes. False for no
    :rtype: boolean"""
    if "." not in ext_name:
        ext_name = '.{}'.format(ext_name)
    name, ext = os.path.splitext(file_name)
    if ext_name and ext_name != ext:
        return False
    elif not ext:
        return False
    return True

def set_ext(file_name, ext_name):
    """rename the file-name extension into something else
    :param ext_name: valid extension file name
    :type ext_name: str
    :returns a file_name with a different extension file name
    :rtype: str"""
    path_name, ext = os.path.splitext(file_name)
    return path_name + '.{}'.format(ext_name)

# ___________________________________________________________________
# serializer_object.py