"""TestCase file for Serializing files"""
# import standard modules
import os
import sys
import unittest
from pathlib import Path
import tracemalloc

# append file path for relative module imports
this_directory = os.path.dirname(os.path.dirname(__file__))
if this_directory not in sys.path:
    sys.path.append(this_directory)

# import custom packages
from serializers import data_serializer as data_s
print(data_s)

class TestCases(unittest.TestCase):
    def test_a_addNewDataContentsToACSVFile(self):
        tracemalloc.start()

        print("Running test: addNewDataContentsToACSVFile()")
        serial_obj = data_s.SerializeData("PersonalData_1.csv")
        data_dict = {'name': "Corian Onst", "address": "345 Winchester Ave.", "phone": "604-454-3453"}
        serial_obj.append_names_by_dict(**data_dict)
        data_dict = {'name': "Fawley Sakes", "address": "340-5465 Astormos St.", "phone": "675-645-5673"}
        serial_obj.append_names_by_dict(**data_dict)
        serial_obj.save_file_as('csv')

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        print("\n[ tracemalloc: Top 10 ]")
        for stat in top_stats[:10]:
            print(stat)
        print("[ Finished ]\n\n")
        self.assertTrue(os.stat(serial_obj.FILE_NAME).st_size != 0)

    def test_b_addNewDataContentsToAXMLFile(self):
        tracemalloc.start()

        print("Running test: addNewDataContentsToAXMLFile()")
        serial_obj = data_s.SerializeData("PersonalData_1.xml")
        data_dict = {'name': "Corian Onst", "address": "345 Winchester Ave.", "phone": "604-454-3453"}
        serial_obj.append_names_by_dict(**data_dict)
        data_dict = {'name': "Fawley Sakes", "address": "340-5465 Astormos St.", "phone": "675-645-5673"}
        serial_obj.append_names_by_dict(**data_dict)
        serial_obj.save_file_as('xml')

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        print("\n[ tracemalloc: Top 10 ]")
        for stat in top_stats[:10]:
            print(stat)
        print("[ Finished ]\n\n")
        self.assertTrue(os.stat(serial_obj.FILE_NAME).st_size != 0)

    def test_c_addNewDataContentsToAPickleFile(self):
        tracemalloc.start()

        print("Running test: addNewDataContentsToAPickleFile()")
        serial_obj = data_s.SerializeData("PersonalData_1.pickle")
        data_dict = {'name': "Corian Onst", "address": "345 Winchester Ave.", "phone": "604-454-3453"}
        serial_obj.append_names_by_dict(**data_dict)
        data_dict = {'name': "Fawley Sakes", "address": "340-5465 Astormos St.", "phone": "675-645-5673"}
        serial_obj.append_names_by_dict(**data_dict)
        serial_obj.save_file_as('pickle')

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        print("\n[ tracemalloc: Top 10 ]")
        for stat in top_stats[:10]:
            print(stat)
        print("[ Finished ]\n\n")
        self.assertTrue(os.stat(serial_obj.FILE_NAME).st_size != 0)

    def test_d_updateCSVDictionaryContents(self):
        print("Running test: updateCSVDictionaryContents()")
        serial_obj = data_s.SerializeData("PersonalData_1.csv")
        serial_obj.load_file()
        serial_obj.update_data_by_name("Fawley Sakes", address="567 Galactic Way")
        serial_obj.save_file()
        self.assertTrue(serial_obj.READ_DATA[1]['address'] == "567 Galactic Way")

    def test_e_searchDictionaryContents(self):
        print("Running test: searchPickleDictionaryContents()")
        serial_obj = data_s.SerializeData("PersonalData_1.pickle")
        serial_obj.load_file()
        results = serial_obj.filter_names("Faw")
        self.assertTrue(len(results) > 0)

    def test_f_convertFileFromCSVToXML(self):
        print("Running test: convertFileFromCSVToXML()")
        serial_obj = data_s.SerializeData("PersonalData_1.csv")
        serial_obj.load_file()
        serial_obj.save_file_as('xml')
        self.assertTrue(os.stat(serial_obj.FILE_NAME).st_size != 0)

    def test_g_convertFileFromXMLToPickle(self):
        print("Running test: convertFileFromXMLToPickle()")
        serial_obj = data_s.SerializeData("PersonalData_1.xml")
        serial_obj.load_file()
        serial_obj.save_file_as('pickle')
        self.assertTrue(os.stat(serial_obj.FILE_NAME).st_size != 0)

    def test_h_convertFileFromPickleToCSV(self):
        print("Running test: convertFileFromPickleToCSV()")
        serial_obj = data_s.SerializeData("PersonalData_1.pickle")
        serial_obj.load_file()
        serial_obj.save_file_as('csv')
        self.assertTrue(os.stat(serial_obj.FILE_NAME).st_size != 0)

    def test_i_showAvailableSerializers(self):
        print("Running test: showAvailableSerializers()")
        self.assertTrue(len(data_s.get_available_serializers()) > 0)

if __name__ == '__main__':
    unittest.main()
# ______________________________________________________________________________________________________________________
# run.py
