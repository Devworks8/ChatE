"""
ChatE is a chat client/server that encrypts all messages and sent. Only those who have the key will
have the ability to read the message.

File Name: chate.py
File Version: 0.0.1
Updated: 26/11/2018
"""

from tkinter import Toplevel as tkToplevel

from Gui import gui


if __name__ == '__main__':
    class ChatE:
        def __init__(self, master):
            self.gui = gui.Gui(master)

        def run(self):
            master.mainloop()

    master = tkToplevel()
    master.title('Chat Encryption')
    chatE = ChatE(master)
    chatE.run()
    