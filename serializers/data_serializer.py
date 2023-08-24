"""Data Serializer Abstraction and Inheritance class objects
Assuming that we are using Python 2.7 for backwards-compatability, please ignore PEP 3107 - Function Annotations"""
# define standard imports
import os
import glob
import imp
import sys
import re
import pprint
import webbrowser
import subprocess
import platform
import importlib
from pathlib import Path


# define default constant variablesimp
TEST_CASES_DIRNAME = "TestCases"
DATA_DIRNAME = "PersonalData"
SERIALIZER_DIRNAME = "serializers"
SERIALZIER_FILENAME = "{}_serializer.py"
DEFAULT_DATA_DICT = {"name": "", "address": "", "phone": ""}
PHONE_NUMBER_RE = re.compile("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")
PERSON_NAME_RE = re.compile(r"[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+")
STREET_ADDRESS_RE = re.compile("^(\\d{1,}) [a-zA-Z0-9\\s]+(\\,)? [a-zA-Z]+(\\,)? [A-Z]{2} [0-9]{5,6}$")

def get_available_serializers():
    """get available serializers for use by this class object
    :returns: available data types to serialize files against
    :rtype: tuple"""
    cur_dir_name = get_default_serializer_path()
    current_files = os.listdir(cur_dir_name)
    data_types = ()
    for f in current_files:
        if "serializer" in f and 'data' not in f:
            data_types += f.split('_')[0],
    return data_types

def get_available_documents():
    """get the available documents for use
    :returns list of available documents
    :rtype: list"""
    documents = ()
    files = [f for f in os.listdir(get_default_data_directory_path()) if "backup" not in f]
    extensions = get_available_serializers()
    for f in files:
        f_name, f_ext = os.path.splitext(f)
        f_ext = f_ext.split('.')[-1]
        if f_ext in extensions:
            documents += f,
    return documents

def get_ext(file_name):
    """get the extension name from the file-path provided
    :returns: extension name
    :rtype: str
    """
    name, ext = os.path.splitext(file_name)
    if not ext:
        raise IOError("Invalid File-Name Given, must containt an extension name!")
    return ext.split('.')[-1]

def set_ext(file_name, ext_name):
    """rename the file-name extension into something else
    :param ext_name: valid extension file name
    :type ext_name: str
    :returns a file_name with a different extension file name
    :rtype: str"""
    path_name, ext = os.path.splitext(file_name)
    return path_name + '.{}'.format(ext_name)

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

def join_and_check_path(dir_name, file_name):
    """join the path of the two file-path and file-name
    :param dir_name: directory name string
    :type dir_name: str
    :param file_name: file-name string, with extension, only
    :type file_name: str
    :returns: successful file path name
    :rtype: str, successful path, else
    :rtype: False boolean, if file path is invalid
    """
    joined_path = os.path.join(dir_name, file_name)
    if not is_file(joined_path):
        print("File-Path does not exist! Do you want to create a new file?")
        input_info = input("Press either `(Y)es` or `(N)o`:\n")
        if 'y' in input_info.lower()[0]:
            # create an empty file
            create_file(joined_path)
        else:
            raise Warning("User has exited this application.")
        if not is_file(joined_path):
            raise IOError("Invalid path:\n{}".format(joined_path))
    return joined_path

def create_file(file_name):
    """creates an empty file
    :param file_name: the file name directory path
    :type file_name: str"""
    dir_name = get_directory_name(file_name)
    if is_dir(dir_name):
        with open(file_name, 'w') as f_name:
            pass # create an empty dummy file
    print('Empty-file created: {}'.format(file_name))

def show_data_as_text(file_name, data):
    """show the data in a human readable format as text file
    :param file_name: the file name to store the temp viewing file
    :param data: self.READ_DATA
    :returns: file name
    :rtype: str
    """
    dir_name = get_directory_name(file_name)
    if is_dir(dir_name):
        file_name = set_ext(file_name, 'txt')
        with open(file_name, 'w') as f_name:
            for read in data:
                for k, v in read.items():
                    f_name.writelines('\n{}\t\t{}'.format(k, v))
                f_name.writelines('\n\n')
    if platform.system() == 'Windows':
        subprocess.run(['notepad.exe', '{}'.format(file_name)])
    elif platform.system() == 'Linux':
        subprocess.run(['gedit', '{}'.format(file_name)])
    elif platform.system() == 'Mac':
        subprocess.run(['TextEdit', '{}'.format(file_name)])
    return file_name

def show_data_as_html(file_name, data):
    """show the data in a human readable format as html file
    :param file_name: the file name to store the temp viewing file
    :param data: self.READ_DATA
    :returns: file name
    :rtype: str
    """
    dir_name = get_directory_name(file_name)
    if is_dir(dir_name):
        file_name = set_ext(file_name, 'html')
        with open(file_name, 'w') as f_name:
            f_name.writelines('<!DOCTYPE html>\n')
            f_name.writelines('<html>\n')
            f_name.writelines('<body>\n')
            f_name.writelines('\n')
            for idx, read in enumerate(data):
                f_name.writelines('<h1> --- </h1>')
                for k, v in read.items():
                    f_name.writelines('<p>{}:\t\t\t{}</p>'.format(k, v))
                f_name.writelines('\n')
            f_name.writelines('\n')
            f_name.writelines('</html>\n')
            f_name.writelines('</body>\n')
    webbrowser.open_new_tab(file_name)
    return file_name

def remove_file(file_name):
    """
    removes this file from disk
    :param file_name: <str> file path name
    :return: True for success
    :rtype: boolean
    :raises: <OSError> invalid file path
    """
    os.unlink(file_name)
    return True

def get_files(path_name, file_ext='json'):
    """
    get the list of files in the path name
    :param path_name: <str> file path name to search
    :param file_ext: <str> file extension to save
    :return: <list> array of files found
    """
    return glob.glob(path_name + '/*{}'.format(file_ext))

def get_serializer_module(ext_name):
    """return the serializer module based on extension name
    :param ext_name: extension name to find
    :type ext_name: str
    :returns: serializer module object
    :rtype: python module object
    """
    module_path = get_default_serializer_path()
    module_name = SERIALZIER_FILENAME.format(ext_name).split('.')[0]
    module_path.replace('\\', '/')
    fp, pathname, description = imp.find_module(module_name, [module_path])
    _mod = imp.load_module(module_name, fp, pathname, description)
    # importlib.reload(_mod) # this causes ModuleNotFoundError: spec not found for the module
    return _mod

def get_serializer_class(module_obj):
    """return the serializer class inside the module object
    :param module_obj: python object to find the class object from
    :type module_obj: python module object
    """
    methods = dir(module_obj)
    for method in methods:
        if "Serializer" in method:
            return method

def get_default_testcases_directory_path():
    """
    return the _relative_ directory path name for test-cases
    :return: directory path name
    :rtype: str
    """
    current_path = get_directory_name(get_directory_name(__file__))
    win_path = Path("{}\\{}".format(current_path, TEST_CASES_DIRNAME))
    if not win_path.exists():
        raise IOError("TestCases Folder Does Not Exist!")
    return win_path.__str__()

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

class SerializeData():
    """Main class for use of identifying, reading, loading and saving the data files"""
    DIRECTORY_NAME = ""
    DEFAULT_DATA_DICT = DEFAULT_DATA_DICT
    AVAILABLE_SERIALIZERS = get_available_serializers()
    AVAILABLE_DOCUMENTS = get_available_documents()
    SERIALIZER = {}
    DATA_KEYS = []
    FILE_NAME = ""
    ROW_NAMES = []
    EXT_NAME = None
    READ_DATA = None
    DATA_TEMP = None
    def __init__(self, personal_data_file=None):
        """Class constructor object
        :param personal_data_file: read this data file otherwise use the default data path
        :type personal_data_file: <str>
        """
        self.file_name = personal_data_file or SerializeData.FILE_NAME
        self.directory_name = SerializeData.DIRECTORY_NAME
        self.SERIALIZER = SerializeData.SERIALIZER
        self.READ_DATA = SerializeData.READ_DATA
        self.DATA_TEMP = SerializeData.READ_DATA
        self.EXT_NAME = SerializeData.EXT_NAME
        if not personal_data_file:
            self.directory_name = get_default_data_directory_path()
            available_files = os.listdir(self.directory_name)
            print("Please choose a file from this directory:\n{}\n\nAvailable data:\n{}".format(self.directory_name, available_files))
        elif not get_directory_name(personal_data_file):
            self.directory_name = get_default_data_directory_path()
            self.file_name = join_and_check_path(self.directory_name, personal_data_file)
            self.initiate_serializer(self.file_name)
        else:
            self.initiate_serializer(self.file_name)
        self.FILE_NAME = self.file_name

    def initiate_serializer(self, personal_data_file=None):
        """initializer method
        :param personal_data_file: data file to exploit
        :type personal_data_file: str
        """
        if not personal_data_file:
            personal_data_file = self.file_name
        self.EXT_NAME = get_ext(personal_data_file)
        # check if ext-names matches with the available serializers
        if not self.EXT_NAME in get_available_serializers():
            raise IOError("No available serializers found for this file: {}".format(personal_data_file))
        # dynamically load the correct serializer class object associated with the extension file-name given  
        serializer_object = get_serializer_module(self.EXT_NAME)
        serializer_class = get_serializer_class(serializer_object)
        class_obj = getattr(serializer_object, serializer_class)
        # instantiate the READ_DATA variable prior to loading the class object
        class_obj.READ_DATA = self.DATA_TEMP
        self.SERIALIZER[self.EXT_NAME] = class_obj()

    def load_file(self):
        """load and read the file based the given file name containing a valid extension"""
        self.DATA_TEMP = self.READ_DATA = self.SERIALIZER[self.EXT_NAME].load_file(self.file_name)

    def save_file(self):
        """save the file based the given file name containing a valid extension"""
        self.SERIALIZER[self.EXT_NAME].READ_DATA = self.READ_DATA
        self.DATA_TEMP = self.READ_DATA = self.SERIALIZER[self.EXT_NAME].save_file(self.file_name)

    def save_file_as(self, ext_name, data=None):
        """allow for saving the file into a different file format
        :param ext_name: choose a different ext format to save
        :type ext_name: str
        :param data: optional, the data that you wish to write
        :type data: list of dictionaries"""
        if not data:
            data = self.DATA_TEMP
        if ext_name not in self.AVAILABLE_SERIALIZERS:
            raise ValueError("Invalid serializer chosen, available formats are:\n{}".format(self.AVAILABLE_SERIALIZERS))
        self.file_name = set_ext(self.file_name, ext_name)
        self.initiate_serializer(self.file_name)
        print("Saving file as: {}".format(self.EXT_NAME))
        self.save_file()
    
    def _get_row_data(self):
        """get the current data key information from READ_DATA, else get data keys from DEFAULT_DATA_DICT
        :returns: data dictionary
        :rtype: dict"""
        if self.READ_DATA:
            keys = list(self.READ_DATA[0].keys())
        else:
            keys = self.DEFAULT_DATA_DICT.keys()
            self.READ_DATA = []
            self.DATA_TEMP = []
        self.ROW_NAMES = keys
        return keys

    def append_names_by_dict(self, **kwargs):
        """append names programmatically
        :param **kwargs: keyword arguments to satisfy the record-keeper"""
        data_dict = {}
        keys = self._get_row_data()
        for k, v in kwargs.items():
            if k in keys:
                data_dict[k] = v
        if data_dict not in self.READ_DATA:
            self.READ_DATA.append(data_dict)
            self.DATA_TEMP.append(data_dict)
            self.SERIALIZER[self.EXT_NAME].READ_DATA = self.READ_DATA
            self.SERIALIZER[self.EXT_NAME].UPDATE_DATA = [1]
        else:
            print("Data already exists in file.")            
        return data_dict

    def append_names_as_user(self, **kwargs):
        """append new records as a human-user using the data keys stored in the READ_DATA, DEFAULT_DATA_DICT
        :returns: False for exiting the while loop
        :rtype: boolean"""
        data_dict = {}
        keys = self._get_row_data()
        while True:
            print("Welcome to the record-keeping!\nThere will be {} fields, {} to complete a single record.".format(len(keys), keys))
            for k in keys:
                information = input("Please enter information for {}:\n".format(k))
                if 'phone' in k.lower():
                    if not PHONE_NUMBER_RE.search(information):
                        input("Please enter a valid phone number for this field.")
                if 'adddress' in k.lower():
                    if not STREET_ADDRESS_RE.search(information):
                        input("Please enter a valid address for this field.")
                data_dict[k] = information
            if data_dict not in self.READ_DATA:
                self.READ_DATA.append(data_dict)
                self.DATA_TEMP.append(data_dict)
                self.SERIALIZER[self.EXT_NAME].READ_DATA = self.READ_DATA
                self.SERIALIZER[self.EXT_NAME].UPDATE_DATA = [1]
            else:
                print("Data already exists in file.")
            return data_dict
        
    def show_current_data(self):
        """shows the current data stored in this class object in a pretty-print text format"""
        printer = pprint.PrettyPrinter(indent=4)
        if not self.DATA_TEMP:
            self.load_file()
        data_length = len(self.DATA_TEMP)
        for idx, data in enumerate(self.DATA_TEMP):
            printer.pprint(data)
            if (data_length - 1) == idx:
                input("You've reached the end of this data document. Press `Enter` to exit.\n")
            else:
                input("Press enter to continue.\n")

    def filter_address(self, key_name):
        """filter the name searches using the fnmatch syntax for the currently provided READ_DATA
        :param key_name: provide a string search to read through the data
        :type key_name: str
        :returns: a list of matching names based on filter key_name
        :rtype: list of names"""
        self._analyze_data_indices()
        dict_list = self.READ_DATA
        names = []
        for data in dict_list:
            for k, v in data.items():
                if 'address' in k.lower():
                    if re.search(key_name, v):
                        names.append(v)
        return names

    def filter_phones(self, key_name):
        """filter the name searches using the fnmatch syntax for the currently provided READ_DATA
        :param key_name: provide a string search to read through the data
        :type key_name: str
        :returns: a list of matching names based on filter key_name
        :rtype: list of names"""
        self._analyze_data_indices()
        dict_list = self.READ_DATA
        names = []
        for data in dict_list:
            for k, v in data.items():
                if 'phone' in k.lower():
                    if re.search(key_name, v):
                        names.append(v)
        return names

    def filter_names(self, key_name):
        """filter the name searches using the fnmatch syntax for the currently provided READ_DATA
        :param key_name: provide a string search to read through the data
        :type key_name: str
        :returns: a list of matching names based on filter key_name
        :rtype: list of names"""
        self._analyze_data_indices()
        dict_list = self.READ_DATA
        name_org = len(self.DATA_KEYS['name'])
        names = []
        for data in dict_list:
            person_name = ""
            for k, v in data.items():
                if name_org == 1:
                    if 'name' in k.lower():
                        person_name = '{}'.format(v)
                elif name_org == 2:
                    if 'name' in k.lower():
                        if person_name:
                            person_name += ' {}'.format(v)
                        else:
                            person_name += v
            if re.search(key_name, person_name):
                names.append(person_name)
        return names

    def remove_data_by_user(self):
        """friendlier user-method of removing data by name"""
        given_name = input("Please provide a given name:")
        sur_name = input("Please provide a sur-name:")
        name = '{} {}'.format(given_name, sur_name)
        self.remove_data_by_name(name=name)

    def remove_data_by_name(self, **kwargs):
        """remove an entire row based on SurName"""
        self._analyze_data_indices()
        if "name" in kwargs:
            person_name = kwargs['name']
        if not len(person_name.split(' ')) == 2:
            raise ValueError("Must enter a proper Given Name, SurName!")
        if not "name" in kwargs:
            raise ValueError("Please Give a name!")
        name_org = len(self.DATA_KEYS['name'])
        if name_org > 1:
            given_name, sur_name = person_name.split(' ')
        else:
            sur_name = person_name
        cur_index = 0
        # get the index of the data based on name only
        for idx, data in enumerate(self.READ_DATA):
            for d_key, d_value in data.items():
                if sur_name in d_value:
                    cur_index = idx # index where the name is found in the file
        self.READ_DATA.pop(cur_index)
        self.SERIALIZER[self.EXT_NAME].UPDATE_DATA = [1]

    def update_data_by_user(self):
        """friendlier user-method of removing data by name"""
        given_name = input("Please provide a given name: ")
        sur_name = input("Please provide a sur-name: ")
        name = '{} {}'.format(given_name, sur_name)
        kwargs = {}
        address = input("Please provide an address: ")
        if address:
            kwargs['address'] = address
        phone = input("Please provide a phone number: ")
        if phone:
            kwargs['phone'] = phone
        self.update_data_by_name(name, **kwargs)

    def update_data_by_name(self, person_name, **kwargs):
        """find and update the existing contents of the data file
        :param person_name: insert data through a person_name
        :type person_name: str
        :returns: changed personal data
        :rtype: dict"""
        self._analyze_data_indices()
        self._get_row_data()
        name_org = len(self.DATA_KEYS['name'])
        if name_org > 1:
            given_name, sur_name = person_name.split(' ')
            print("Updated Person Name: {} {}".format(given_name, sur_name))
        else:
            sur_name = person_name
            print("Updated Person Name: {}".format(sur_name))
        cur_index = 0
        change_data = None
        # get the index of the data based on name only
        for idx, data in enumerate(self.READ_DATA):
            for d_key, d_value in data.items():
                if sur_name in d_value:
                    cur_index = idx # index where the name is found in the file
                    change_data = data
                    if cur_index not in self.SERIALIZER[self.EXT_NAME].UPDATE_DATA:
                        self.SERIALIZER[self.EXT_NAME].UPDATE_DATA.append(cur_index)
                    break
        if not data:
            raise ValueError("{} Not found in data. Consider appending the information for this person:".format(person_name))
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

    def show_data_as_html(self):
        show_data_as_html(self.file_name, self.READ_DATA)

    def show_data_as_text(self):
        show_data_as_text(self.file_name, self.READ_DATA)
#___________________________________________________________________________________________________
# data_serializer.py