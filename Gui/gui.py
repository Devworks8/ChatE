"""
All gui related work is located and handled here.

File Name: gui.py
File Version: 0.2.1
Updated: 1/12/2018
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk


class Client:
    def __init__(self, config):
        self.config = config
        self._my_msg = None
        self._msg_list = None
        self._usr_list = None
        self._messages_frame = None
        self._user_frame = None
        self._btm_frame = None
        self._entry_field = None
        self._send_button = None
        self.receive_thread = None
        self.client_socket = None
        self.top = None

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.config.buff_size).decode(self.config.encoding)
                self._msg_list.insert(tk.END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        msg = self._my_msg.get()
        self._my_msg.set("")  # Clears input field.
        self.client_socket.send(bytes(msg, self.config.encoding))
        if msg == "{quit}":
            self.client_socket.close()
            self.top.quit()

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self._my_msg.set("{quit}")
        self.send()

    def load(self, version):
        self.top = tk.Tk()
        self.top.configure(bg='black')
        self.top.title("Encrypted Chat - Version %s" % version)
        self.top.geometry('600x800')

        # FIXME: Need to finish structuring the gui.
        # Setup the window
        self.top.grid_columnconfigure(0, weight=3)
        self.top.grid_rowconfigure(1, weight=3)

        # Create labels
        lbl1 = tk.Label(self.top, text="Chat", bg="black", fg="white")
        lbl2 = tk.Label(self.top, text="Users", bg="black", fg="white")
        lbl1.grid(row=0, column=0, sticky="w")
        lbl2.grid(row=0, column=1, sticky="w")

        # Create Message frame
        self._messages_frame = tk.Frame(self.top, bg="black", relief=tk.SUNKEN)
        self._messages_frame.grid_rowconfigure(1, weight=20)
        self._messages_frame.grid_columnconfigure(0, weight=3)
        self._messages_frame.grid(column=0, row=1, sticky="nsew")
        _msg_scrollbar = tk.Scrollbar(self._messages_frame, orient="vertical", bg="black")  # To navigate through past messages.
        _msg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._msg_list = tk.Listbox(self._messages_frame, yscrollcommand=_msg_scrollbar.set, bd=2, bg="black", fg="white")
        self._msg_list.pack(expand=True, fill=tk.BOTH)
        _msg_scrollbar.config(command=self._msg_list.yview)

        # Create User frame
        self._user_frame = tk.Frame(self.top, bg="black", relief=tk.SUNKEN)
        self._messages_frame.grid_rowconfigure(1, weight=8)
        self._user_frame.grid(column=1, row=1, sticky="nsew")
        _usr_scrollbar = tk.Scrollbar(self._user_frame, orient="vertical", bg="black")  # To navigate through users.
        _usr_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self._usr_list = tk.Listbox(self._user_frame, yscrollcommand=_usr_scrollbar.set, bd=2, bg="black", fg="white")
        self._usr_list.pack(expand=True, fill=tk.Y)
        _usr_scrollbar.config(command=self._usr_list.yview)

        # Create variable to store user input
        self._my_msg = tk.StringVar(self._messages_frame)  # For the messages to be sent.
        self._my_msg.set("Type your messages here.")

        # Create input field, and send button.
        self._entry_field = tk.Entry(self.top, textvariable=self._my_msg, width=300, bg="black", fg="white")
        self._entry_field.bind("<Return>", self.send)
        self._entry_field.grid(column=0, row=2)
        self._send_button = tk.Button(self.top, text="Send", command=self.send, bg="black", fg="white")
        self._send_button.grid(column=1, row=2)

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        #----Now comes the sockets part----

        HOST = input('Enter host: ')
        PORT = input('Enter port: ')
        if not PORT:
            PORT = self.config.port
        else:
            PORT = int(PORT)

        ADDR = (HOST, PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

        self.top.mainloop()  # Starts GUI execution.


# TODO: Implement settings window.
class Settings:
    pass
