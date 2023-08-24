"""A simple, human-friendly command-line interface for exposing available Data Serializer commands"""
# standard imports
import sys
import pprint
import subprocess
# custom imports
from serializers import data_serializer

if __name__ == '__main__':
    global document_name
    document_name = None
    while True:
        if not document_name:
            documents = data_serializer.get_available_documents()
            serializers = data_serializer.get_available_serializers()
            confirm = input("Welcome to the record-keeper human friendly interface!\nThere are {0} available documents, "
                            "and {1} available serializers.\nPress `Enter` to continue or enter `Q` to quit this program: "
                            "".format(len(documents), len(serializers)))
            if confirm:
                if confirm[0].lower() == 'q':
                    sys.exit(0)
        message = ("\n\nAvailable commands: \n"
                   "Show (D)ocuments        \n"
                   "Show (S)erializers      \n"
                   "`(C)hoose` Document: `Document_Name.ext` \n"
                   "`(R)ead` Document       \n"
                   "`(S)earch` Document: `aA-zZLetters*` \n"
                   "`(A)ppend` Data         \n"
                   "`(U)pdate` Data         \n"
                   "`(E)rase` Data: `Given_Name` \n"
                   "`(F)ile Save As`             \n"
                   "`(O)pen Data`           \n"
                   "`(Q)uit`                \n")
        answer = input(message)
        if not answer:
            continue
        if answer[0].lower() == 'q': # (Q)uit
            sys.exit(0)
        if "show" in answer and answer[5].lower() == 'd': # Show (D)ocuments
            print(documents)
            continue
        elif "show" in answer and answer[5].lower() == 's': # Show (S)erializers
            print(serializers)
            continue
        if not "show" in answer.lower():
            if answer[0].lower() == 'c': # (C)hoose Document:
                document_name = answer.split(' ')[-1]
                print("Document chosen: {}".format(document_name))
                if document_name not in documents:
                    print("Please choose one of the following: \n\n{}".format(documents))
                    continue
            elif answer[0].lower() == 'r': # (R)ead Document
                if not document_name:
                    print("Please Choose a document.")
                    continue
                serial_obj = data_serializer.SerializeData(document_name)
                serial_obj.load_file()
                serial_obj.show_current_data()
                continue
            elif answer[0].lower() == 's': # (S)earch Document:
                if not document_name:
                    print("Please Choose a document.")
                    continue
                serial_obj = data_serializer.SerializeData(document_name)
                serial_obj.load_file()
                answer = input("Please choose filter by type: `phone`, `name`, `address`")
                if answer == 'name':
                    search_name = input("input name to search:")
                    print(serial_obj.filter_names(search_name))
                if answer == 'address':
                    search_name = input("input address to search:")
                    print(serial_obj.filter_address(search_name))
                if answer == 'phone':
                    search_name = input("input phone to search:")
                    print(serial_obj.filter_phones(search_name))
                continue
            elif answer[0].lower() == 'a': # (A)ppend Data
                if not document_name:
                    print("Please Choose a document.")
                    continue
                serial_obj = data_serializer.SerializeData(document_name)
                serial_obj.load_file()
                serial_obj.append_names_as_user()
                serial_obj.save_file()
            elif answer[0].lower() == 'u': # (U)pdate Data
                if not document_name:
                    print("Please Choose a document.")
                    continue
                serial_obj = data_serializer.SerializeData(document_name)
                serial_obj.load_file()
                serial_obj.update_data_by_user()
                serial_obj.save_file()
            elif answer[0].lower() == 'e': # (E)rase Data:
                if not document_name:
                    print("Please Choose a document.")
                    continue
                search_name = answer.split(' ')[:-2]
                serial_obj = data_serializer.SerializeData(document_name)
                serial_obj.load_file()
                serial_obj.remove_data_by_user()
                serial_obj.save_file()
                continue
            elif answer[0].lower() == 'o': # (O)pen Document
                if not document_name:
                    print("Please Choose a document.")
                    continue
                serial_obj = data_serializer.SerializeData(document_name)
                serial_obj.load_file()
                answer = input("html or text: \n")
                answer = answer.split("\n")[-1]
                if answer == 'text':
                    serial_obj.show_data_as_text()
                if answer == 'html':
                    serial_obj.show_data_as_html()
                continue
            elif answer[0].lower() == 'f': # (F)ile Save As
                if not document_name:
                    print("Please Choose a document.")
                    continue
                serial_obj = data_serializer.SerializeData(document_name)
                serial_obj.load_file()
                answer = input("Choose an Extension: {}\n".format(", ".join(serializers)))
                answer = answer.split("\n")[-1]
                if answer in serializers:
                    serial_obj.save_file_as(answer)
                else:
                    print("could not save file.")
                continue
# ___________________________________________________________________________________________
# main.py        