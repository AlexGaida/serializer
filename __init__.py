
"""
The purpose of a Serializer for Python module is extended to but not limited to:
    1. Serialization libraries in Python such as pickle, JSON and XML
    2. Serializing objects such as dictionaries in Python
    3. How to use serialization for memoization to reduce function calls

In Python write a module or small library which shows how you would take a set of personal data, where each record contains:
    name
    address
    phone number

And:
    build a simple API allowing you to add new records, filter users (e.g "name=Joe*") 
    based on some simple search syntax like Glob
    support serialisation in 2 or more formats (e.g JSON, Yaml, XML, CSV etc)
    display the data in 2 or more different output formats (no need to use a GUI Framework, 
    use e.g text output/HTML or any other human readable format)
    add a command line interface to add records, and display/convert/filter the whole data set

Write it in such a way that it would be easy for a developer to extend the system e.g

    to add support for additional storage formats
    to query a list of currently supported formats

This should ideally show Object-Oriented Design and Design Patterns Knowledge, 
we're not looking for use of advanced Language constructs.
Please provide reasonable Unit Test coverage and basic API documentation.
Designing a webservice using libraries such as Flask or Django is not required.
The task is designed to allow you some flexibility in how you design and implement it, 
and you should submit something that demonstrates your abilities and/or values as a Software Engineer.
"""