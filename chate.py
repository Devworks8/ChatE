"""
ChatE is a chat client/server that encrypts all messages and sent. Only those who have the key will
have the ability to read the message.

File Name: chate.py
File Version: 0.1.2
Updated: 28/11/2018
"""

from tkinter import Toplevel as tkToplevel

from Parser import parser
from Gui import gui
from Network import network

__VERSION__ = "0.0.2"


class ChatE:
    def __init__(self):
        self.config = parser.Config()
        self.client = gui.Client(self.config)

    def run(self):
        self.client.load(__VERSION__)


if __name__ == '__main__':
    chatE = ChatE()
    chatE.run()
