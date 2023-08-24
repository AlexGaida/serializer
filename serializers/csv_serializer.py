"""read comma separated values files and turn them into a data object"""
# import standard modules
import csv
import os
import imp

# import custom modules
# from modules import serializer_object #ModuleNotFoundError
module_path = os.path.dirname(__file__)
fp, pathname, description = imp.find_module('serializer_object', [module_path + '/modules'])
serializer_object = imp.load_module('serializer_object', fp, pathname, description)

class CSVSerializer(serializer_object.DataSerializer):
    """CSV serializer for manipulation of data files"""
    # raw data as read from the CSV file
    READ_DATA = []
    # for information only, shows which indices have been updated inside the CSV file
    UPDATE_DATA = []
    # identify how the CSV file is organized, this is important as each CSV data file is written differently!
    DATA_KEYS = None
    ROW_NAMES = None
    FILE_NAME = ""
    EXT_NAME = "csv"
    def __init__(self, *args, **kwargs):
        """Constructor method"""
        self.READ_DATA = CSVSerializer.READ_DATA
        if self.READ_DATA:
            self.UPDATE_DATA = [1]
        self.EXT_NAME = CSVSerializer.EXT_NAME
        self.ROW_NAMES = CSVSerializer.ROW_NAMES
        super(serializer_object.DataSerializer, self).__init__(*args, **kwargs)

    def save_file(self, path_name=None):
        """save the updated data to a file if changes are made to the original data
        :param path_name: the data file name to save into
        :returns: True for success.
        :rtype: boolean"""
        path_name = self._check_path(path_name)
        if not self.ROW_NAMES:
            self.ROW_NAMES = self._get_data_rows_from_data()
        if not self.UPDATE_DATA:
            print("No changes are made to the file!")
            return []
        else:
            with open(path_name, 'w', newline='') as csvfile:
                fieldnames = self.ROW_NAMES
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for data in self.READ_DATA:
                    writer.writerow(data)
        csvfile.close() # precaution
        return self.READ_DATA
    
    def load_file(self, path_name=None):
        """load the file and read the contents of the file
        :param path_name: provide an alternative path name
        :type path_name: str
        :returns: list of data from the file provided
        :rtype: list
        """
        path_name = self._check_path(path_name)
        # open file and organize the data
        dict_data = []
        self.ROW_NAMES = self.get_data_rows(path_name)
        with open(path_name, newline='') as csvfile:
            load_reader = csv.DictReader(csvfile)
            for row in load_reader:
                # clean the data of the NoneType keys
                if None in row:
                    for k in row.keys():
                        if None == k:
                            continue
                        if 'address' in k.lower():
                            row[k] += ' '.join(row[None])
                            dict_data.append(row)
                            continue
                    row.pop(None)
                # precautionary check against duplicate append items
                if row not in dict_data:
                    dict_data.append(row)
        csvfile.close() # precaution
        # store the data
        self.READ_DATA = dict_data
        # conform to the original .CSV-file rules!
        self._analyze_data_indices()
        return self.READ_DATA

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

    def get_data_rows(self, path_name):
        """Returns the top-most row names for information
        :param path_name: file-path name
        :type path_name: str
        :returns: row list data"""
        with open(path_name, newline='') as csvfile:
            load_reader = csv.reader(csvfile)
            for row in load_reader:
                return row
#___________________________________________________________________________________________________
# csv_serializer.py    