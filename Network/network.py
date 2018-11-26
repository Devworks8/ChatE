"""
All network related work is located and handled here.

File Name: network.py
File Version: 0.1.0
Updated: 26/11/2018
"""

import socket
import select
import sys
from threading import *

from Encryption.encryption import Encrypt
from Parser.parser import Config


# TODO: Implement Server Class
class Server(Encrypt, Config):
    """
    All hosting functionality is handled by the Server class.
    """

    def __init__(self):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip_address = Config.host
        self.port = Config.port
        self.server.bind((self.ip_address, self.port))
        self.server.listen(Config.active_Connections)
        self.list_of_clients = []

    def clientthread(self, conn, addr):
        """
        Client Handler

        :param conn: Socket Object
        :param addr: IP Address
        :return: None
        """
        # Send a welcome message to new connections.
        conn.send(Config.welcome)

        while True:
            try:
                message = conn.recv(2048)
                if message:
                    # Print the message
                    print("->" ) + message

                else:
                    # Remove the connection if broken.
                    self.remove(conn)

            except:
                continue

    def broadcast(self, message, connection):
        """
        Broadcast the message to all clients who's object is not the same of the one sending the message.

        :param message: Message sent
        :param connection: Socket Object
        :return: None
        """
        for clients in self.list_of_clients:
            if clients != connection:
                try:
                    clients.send(message)
                except:
                    clients.close()

                    # If the link is broken, remove the client
                    self.remove(clients)

    def remove(self, connection):
        """
        Removes the object from the list that was created at the beginning.
        :param connection: Socket Object
        :return: None
        """

        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

    def state(self, run=True):
        while True:
            """
            Accept a connection request and stores two parameters, 
            conn, which is a socket object for that user, 
            and addr which contains the IP address of the client that just connected.
            """

            conn, addr = self.server.accept()

            """
            Maintain a list of clients for ease of broadcasting a message to all available people in the chatroom.
            """

            self.list_of_clients.append(conn)

            # Create an individual thread for every user that connects.
            start_new_thread(clientthread, (conn, addr))

        conn.close()
        self.server.close()


# TODO: Implement Client Class
class Client(Encrypt):
    """
    All client functionality is handled by the Client class.
    """

    pass

