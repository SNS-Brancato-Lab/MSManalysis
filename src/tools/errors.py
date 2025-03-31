"""
Custom error for MSManalysis
"""

class ConversionError(TypeError):

    def __init__(self, file_name: str = None, message: str = None):
        self.file_name = file_name
        self.message = message or "File '{}' could not be converted!".format(self.file_name)
        super().__init__(self.message)