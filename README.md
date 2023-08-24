# Data Serializer :: Technical Task from Animal Logic
>Name, Address, Phone Number
## Simple Instructions:
1. Build a Simple API allowing the user to add new records, filter users
(e.g "name=Joe*")  based on some simple search syntax like Glob
2. Support serialization in 2 or more formats (e.g JSON, Yaml, XML, CSV etc)
3. Display the data in 2 or more different output formats; use text output/HTML
or any other human readable format)
4. Add a command-line interface to add records, and display/ convert/ filter
the whole data set

## Write it in such a way that it would be easy for a developer to extend the system:
1. to add support for additional storage formats:
>Please create a new python object inside "..\serializer\serializers" directory
following the naming convention: "{dtype}_serializer.py"
>The class inside the module should always be named as "Serializer" and must
contain the following template functions:
```
class Serializer:
    """Abstract class for use as a base for context-specific data
    serialization/ deserialization"""
    def __init__(self):
        pass
    def save_file(self):
        pass
    def load_file(self):
        pass
    def remove_data(self):
        pass
    def update_data(self):
        pass
```
_and_ inherits the data_serializer.DataSerializer class object, such as:
```
class XMLSerializer(ds.DataSerializer):
```
2. to query a list of currently supported formats:
>import data_serializer as ds;
>print(ds.get_available_serializers())

3. this tool's data is stored as a list of dictionaries

## Steps needed to achieve this goal:
1. The first order of business is to have access to data: so I've generated
synthetic data from generatedata.com/  Fakenamegenerator.com.
2. Understand what terminology is used in association to the definitions of
Data Serialization, using the Python programming language.
3. Data serialization is the process of converting an object into a stream of
bytes to more easily save or transmit it.
4. Serialization and deserialization work together to transform/recreate data
objects to/from a portable format.
5. Sketch out the design of the program (I've looked up and have used
https://lucid.app/lucidchart) to create a .PNG plan of this program's design.
6. Create Abstraction classes to flesh out the basic functionalities of this program.
7. Define the functions inside the class objects inherited from the abstraction
class object: save_file(), load_file(), update_data(),
append_data(), delete_data() function calls.
8. Run the class functions through TestCase methods, and perform all the function calls repeatedly so as to be thorough on testing.
9. Submit the finished project file to a special link supplied by the recruiter
working at Animal Logic before *Wednesday 23rd*.
10. Await further instructions.

## Pitfalls, main challenges tackled, while performing this test:
1. Combating assumptions from rarely-used python libraries
2. Cleaning the data from the original .csv files provided
3. Counter-acting against tunnel vision work, researching modules such as XML, CSV file parsers, beforehand was crucial.
4. test, test, test each function call to make certain that the tool functions as it should.
5. dealt with import failures: "ModuleNotFoundError: spec not found for the module" had to separate and create a new 'serializer_object' as a work-around.
6. dealt with ResourceWarning: "Enable tracemalloc to get the object allocation traceback" by printing the tracemalloc snapshot statistics inside the TestCases
7. _Uncertainty over studios' expectations of this test, so I wrote enough to cover basic assumptions around the design *and* the functionality of this tool to the best of my knowledge._

# BASIC API DOCUMENTATION
________________________________________________________________________________
```
import data_serializer as data_s
# to show available documents
data_s.get_available_documents()

# to open and read a data file:
serial_obj = data_s.SerializeData("PersonalData.csv")
serial_obj.load_file()
serial_obj.show_current_data()

# to filter names contained inside the data file
serial_obj = data_s.SerializeData("PersonalData.csv")
serial_obj.load_file()
serial_obj.filter_names('A*')

# append information and save
serial_obj = data_s.SerializeData("PersonalData.csv")
serial_obj.load_file()
data_dict = {'name': "Corian Onst", "address": "345 Winchester Ave.", "phone": "604-454-3453"}
serial_obj.append_names_by_dict(**data_dict)
data_dict = {'name': "Fawley Sakes", "address": "340-5465 Astormos St.", "phone": "675-645-5673"}
serial_obj.append_names_by_dict(**data_dict)
serial_obj.save_file()

# update information and save
serial_obj = data_s.SerializeData("PersonalData.csv")
serial_obj.load_file()
serial_obj.update_data_by_name("Fawley Sakes", address="567 Galactic Way")
serial_obj.save_file()

# to show available serializers
data_s.get_available_serializers()

# to save as a different data type
serial_obj = data_s.SerializeData("PersonalData.csv")
serial_obj.load_file()
serial.obj.save_file_as('xml')

# to open the data as a text-file
serial_obj = data_s.SerializeData("PersonalData_1.csv")
serial_obj.load_file()
serial_obj.show_data_as_text()

# to open the data as a html-file
serial_obj = data_s.SerializeData("PersonalData.csv")
serial_obj.load_file()
serial_obj.show_data_as_html()
```
# Running the interface
1. please double-click on run.bat file or run the main.py module in the command terminal.

###### The command line interface has the following options when run:
```
Welcome to the record-keeper human friendly interface!
There are 5 available documents, and 3 available serializers:
Press `Enter` to continue or press (Q) to quit this program:

Available commands:
Show (D)ocuments,
Show (S)erializers
`(C)hoose` Document: `Document_Name.ext`
`(R)ead` Document
`(S)earch` Document: `aA-zZLetters*`
`(A)ppend` Data
`(U)pdate` Data
`(E)rase` Data: `Given_Name`
`(O)pen Document`
`(Q)uit`
```
