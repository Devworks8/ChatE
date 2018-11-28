"""
All network related work is located and handled here.

File Name: network.py
File Version: 0.2.0
Updated: 27/11/2018
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from Encryption.encryption import Encrypt
from Parser.parser import Config


class Server(Encrypt):
    """
    All hosting functionality is handled by the Server class.
    """

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.ip_address = ""
        self.port = config.port
        self.clients = {}
        self.addresses = {}
        self.server = None

    def accept_incoming_connections(self):
        """
        Sets up handling for incoming clients.
        :return:
        """
        while True:
            client, client_address = self.server.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes("Welcome to the Cave! Press enter to use the default alias; %s, or enter a new alias." % self.config.alias, self.config.encoding))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        """
        Handles a single client connection.
        :param client: socket
        :return:
        """

        name = client.recv(self.config.buff_size).decode(self.config.encoding)
        client.send(bytes(self.config.welcome, self.config.encoding))
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, self.config.encoding))
        self.clients[client] = name
        while True:
            msg = client.recv(self.config.buff_size)
            if msg != bytes("{quit}", self.config.encoding):
                self.broadcast(msg, name + ": ")
            else:
                client.send(bytes("{quit}", self.config.encoding))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("%s has left the chat." % name, self.config.encoding))
                break

    def broadcast(self, msg, prefix=""):
        """
        Broadcasts a message to all the clients.
        :param msg: message string
        :return:
        """

        for sock in self.clients:
            sock.send(bytes(prefix, self.config.encoding) + msg)

    def run(self, kill=False):
        self.ip_address = self.config.host
        self.port = self.config.port
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.ip_address, self.port))
        self.server.listen(self.config.max_connections)
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.server.close()


# TODO: Implement Client Class
class Client(Encrypt, Config):
    """
    All client functionality is handled by the Client class.
    """

    def __init__(self):
        Encrypt.__init__()
        Config.__init__()




