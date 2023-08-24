"""read comma separated values files and turn them into a data object"""
# import standard modules

# import custom modules
from modules import serializer_object

class TemplateSerializer(ds.DataSerializer):
    """Template serializer for manipulation of data files"""
    # raw data as read from file
    READ_DATA = []
    # for information only for checking data changes
    UPDATE_DATA = []
    # identify how the file is organized
    DATA_KEYS = None
    ROW_NAMES = None
    FILE_NAME = ""
    EXT_NAME = "template"
    def __init__(self, *args, **kwargs):
        """Constructor method"""
        self.READ_DATA = TemplateSerializer.READ_DATA
        if self.READ_DATA:
            self.UPDATE_DATA = [1]
        self.EXT_NAME = TemplateSerializer.EXT_NAME
        self.ROW_NAMES = TemplateSerializer.ROW_NAMES
        super(ds.DataSerializer, self).__init__(*args, **kwargs)

    def save_file(self, path_name=None):
        """save the updated data to a file if changes are made to the original data
        :param path_name: the data file name to save into
        :returns: True for success.
        :rtype: boolean"""
        return self.READ_DATA
    
    def load_file(self, path_name=None):
        """load the file and read the contents of the file
        :param path_name: provide an alternative path name
        :type path_name: str
        :returns: list of data from the file provided
        :rtype: list
        """
        return self.READ_DATA


#___________________________________________________________________________________________________
# csv_serializer.py    