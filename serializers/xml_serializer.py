"""read eXtensible Markup Language files and turn them into a python data object"""
# import standard modules
import os
import imp
import warnings
import xml.etree.cElementTree as ET

# import custom modules
# from modules import serializer_object
module_path = os.path.dirname(__file__)
fp, pathname, description = imp.find_module('serializer_object', [module_path + '/modules'])
serializer_object = imp.load_module('serializer_object', fp, pathname, description)

class XMLSerializer(serializer_object.DataSerializer):
    """XML serializer for manipulation of data files"""
    # raw data as read from the XML file
    READ_DATA = []
    # for information only, shows which indices have been updated inside the XML file
    UPDATE_DATA = []
    # identify how the XML file is organized, this is important as each XML data file is written differently!
    DATA_KEYS = None
    ROW_NAMES = None
    FILE_NAME = ""
    EXT_NAME = "xml"
    def __init__(self, *args, **kwargs):
        """Constructor method"""
        self.READ_DATA = XMLSerializer.READ_DATA
        if self.READ_DATA:
            self.UPDATE_DATA = [1]
        self.EXT_NAME = XMLSerializer.EXT_NAME
        self.ROW_NAMES = XMLSerializer.ROW_NAMES
        self._pretty_indentation = "\n" + " "
        super(serializer_object.DataSerializer, self).__init__(*args, **kwargs)

    def save_file(self, path_name=None):
        """save the updated data to a file if changes are made to the original data
        :param path_name: the data file name to save into
        :returns: list of dictionaries.
        :rtype: list"""
        self._check_dir(path_name)
        if not self.UPDATE_DATA:
            warnings.warn("No changes are made to the file!")
            return []
        else:
            root = ET.Element("root" + self._pretty_indentation )
            for idx, row in enumerate(self.READ_DATA):
                doc = ET.SubElement(root, "doc_{}".format(idx) + self._pretty_indentation)
                for k, v in row.items():
                    ET.SubElement(doc, "field_{}".format(k), name=k).text = v + self._pretty_indentation 
            tree = ET.ElementTree(root)
            tree.write(path_name)
        return self.READ_DATA
    
    def load_file(self, path_name=None):
        """loads and reads the contents of the XML file
        :param path_name: provide an alternative path name
        :type path_name: str
        :returns: list of dictionaries from the file provided
        :rtype: list
        """
        self._check_path(path_name)
        dict_data = []
        # pass the path of the xml document 
        tree = ET.parse(path_name)
        # get the parent tag 
        root = tree.getroot()
        for idx in range(len(root)):
            data_dict = {}
            for n in range(len(root[idx])):
                field = root[idx][n]
                data_dict.update({field.get('name').strip(self._pretty_indentation): field.text.strip(self._pretty_indentation)})
            dict_data.append(data_dict)
        self.READ_DATA = dict_data
        self.ROW_NAMES = self._get_data_rows_from_data()
        self._analyze_data_indices()
        return dict_data

    def get_data_rows(self, path_name):
        """Returns the top-most row names for information from a file
        :param path_name: file-path name
        :type path_name: str
        :returns: row list data"""
        self._check_path(path_name)
        # pass the path of the xml document 
        tree = ET.parse(path_name)
        # get the parent tag 
        root = tree.getroot()
        for idx in range(len(root)):
            data_dict = {}
            for n in range(len(root[idx])):
                field = root[idx][n]
                data_dict.update({field.get('name').strip(self._pretty_indentation): field.text.strip(self._pretty_indentation)})
            return data_dict.keys()

#___________________________________________________________________________________________________
# xml_serializer.py