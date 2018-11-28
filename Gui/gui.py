"""
All gui related work is located and handled here.

File Name: gui.py
File Version: 0.1.0
Updated: 27/11/2018
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

from Parser.parser import Config


class Gui:
    def __init__(self, frame, config):
        self.config = config
        self._my_msg = None
        self._msg_list = None
        self._messages_frame = None
        self._scrollbar = None
        self._entry_field = None
        self._send_button = None
        self.receive_thread = None
        self.client_socket = None
        self.top = frame

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

    def load(self):
        self.top.title("Chat Encryption")

        self._messages_frame = tk.Frame(self.top)
        self._my_msg = tk.StringVar()  # For the messages to be sent.
        self._my_msg.set("Type your messages here.")
        self._scrollbar = tk.Scrollbar(self._messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        self._msg_list = tk.Listbox(self._messages_frame, height=15, width=50, yscrollcommand=self._scrollbar.set)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self._msg_list.pack()
        self._messages_frame.pack()

        self._entry_field = tk.Entry(self.top, textvariable=self._my_msg)
        self._entry_field.bind("<Return>", self.send)
        self._entry_field.pack()
        self._send_button = tk.Button(self.top, text="Send", command=self.send)
        self._send_button.pack()

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
        tk.mainloop()  # Starts GUI execution.


# FIXME: Crashes when used in the macOS environment.
class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    * Code fetched from https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, scrollregion=(0, 0, 800, 600), width=800, height=600, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * event.delta, 'units')

        #canvas.bind_all('<MouseWheel>', _on_mousewheel)
