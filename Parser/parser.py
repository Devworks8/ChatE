"""
All parsing related work is located and handled here.

File Name: parser.py
File Version: 0.0.2
Updated: 27/11/2018
"""


# TODO: Implement Config class.
class Config:
    """
    All config functionality is handled by the Config class.
    """

    def __init__(self):
        super().__init__()
        self.host = '127.0.0.1'
        self.port = 1060
        self.max_connections = 100
        self.welcome = 'Welcome to the Cave! Type {quit} to exit.'
        self.buff_size = 1024
        self.encoding = "utf8"
        self.alias = "Krunk"
