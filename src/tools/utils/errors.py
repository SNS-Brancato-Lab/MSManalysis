"""
Custom error for MSManalysis
"""

class ConversionError(TypeError):

    def __init__(self, file_name: str = None, message: str = None):
        self.file_name = file_name
        self.message = message or "File '{}' could not be converted!".format(self.file_name)
        super().__init__(self.message)

class MissingAttribute(AttributeError):

    def __init__(self, attribute: str = None, message=None):
        self.attribute = attribute
        self.message = message or "{} not loaded or selected!".format(self.attribute)
        super().__init__(self.message)

class CommandError(ValueError):

    def __init__(self, command: str = None, message=None):
        self.command = command
        self.message = message or "Command '{}' not found!".format(self.command)
        super().__init__(self.message)
