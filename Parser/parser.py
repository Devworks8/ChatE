"""
All parsing related work is located and handled here.

File Name: parser.py
File Version: 0.0.1
Updated: 26/11/2018
"""


# TODO: Implement Config class.
class Config:
    """
    All config functionality is handled by the Config class.
    """

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 1060
        self.active_Connections = 100
        self.welcome = 'Welcome to the Cave'
        self.recv_size = 2048
