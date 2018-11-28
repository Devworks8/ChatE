"""
ChatE is a chat client/server that encrypts all messages and sent. Only those who have the key will
have the ability to read the message.

File Name: chate.py
File Version: 0.0.2
Updated: 27/11/2018
"""

from tkinter import Toplevel as tkToplevel

from Parser import parser
from Gui import gui
from Network import network


class ChatE:
    def __init__(self, master):
        self.config = parser.Config()
        self.gui = gui.Gui(master, self.config)

    def run(self, server=False):
        if not server:

            self.gui.load()
        else:
            server = network.Server(self.config)
            server.run()


if __name__ == '__main__':
    master = tkToplevel()
    chatE = ChatE(master)
    #chatE.run(server=True)
    chatE.run(server=False)
