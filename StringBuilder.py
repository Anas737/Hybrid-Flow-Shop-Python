__author__ = "EL BOUKHARI & EL AATABI"
from io import StringIO


# This class is created to manage strings

class StringBuilder:
    def __init__(self):
        self.data = StringIO()

    def AppendLine(self, value=""):
        self.Append("\n" + str(value))

    def Append(self, value=""):
        self.data.write(str(value))

    def __str__(self):
        return self.data.getvalue()
