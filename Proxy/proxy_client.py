import socket
import sys
import struct


class SimpleTCPSelectClient:
    def __init__(self, serverAddr='localhost', serverPort=10001):
        self.setupClient(serverAddr, serverPort)

    def setupClient(self, serverAddr, serverPort):
        server_address = (serverAddr, serverPort)

        # Create a TCP/IP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.client.connect(server_address)

    def create_messagge(self):
        message = raw_input("Add meg az egyenletet: ").split()
        value = (int(message[0]), message[1], int(message[2]))
        packer = struct.Struct('I 1s I')
        packed_data = packer.pack(*value)
        return packed_data

    def handleIncomingMessageFromRemoteServer(self):
        data = self.client.recv(4096)
        if not data:
            print '\nDisconnected from server'
            sys.exit()
        else:
            print data

    def handleConnection(self):
        while True:
            message = self.create_messagge()
            self.client.send(message)
            self.handleIncomingMessageFromRemoteServer()


simpleTCPSelectClient = SimpleTCPSelectClient()
simpleTCPSelectClient.handleConnection()
