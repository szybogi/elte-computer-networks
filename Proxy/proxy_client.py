import socket
import sys
import struct


class SimpleTCPSelectClient:
    # TCP cliens letrehozasa
    def __init__(self, serverAddr='localhost', serverPort=10001):
        self.setupClient(serverAddr, serverPort)

    def setupClient(self, serverAddr, serverPort):
        server_address = (serverAddr, serverPort)

        # TCP/IP socket keszitese
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.client.connect(server_address)

    # ez a fugveny kesziti el a servernek elkuldendo uzenetet
    def create_messagge(self):
        # standard inputrol olvas be, majd spacenkent szetsplittel
        message = raw_input("Add meg az egyenletet: ").split()
        # a message tomb elemeibol tuple-t keszit
        value = (int(message[0]), message[1], int(message[2]))
        # int 1char int formatomu strukturat csinal es ezt becsomagolja majd visszater ezzel a fuggveny
        packer = struct.Struct('I 1s I')
        packed_data = packer.pack(*value)
        return packed_data

    # ez a fuggveny kezeli a servertol jovo uzeneteket
    def handleIncomingMessageFromRemoteServer(self):
        data = self.client.recv(4096)
        # ha nem kapott semmit, akkor error-t dob es megszakitja a folyamatot
        if not data:
            print '\nDisconnected from server'
            sys.exit()
        # egyebkent kiirja amit kapott adatot
        else:
            print data

    # ez a fuggveny felel azert, hogy fenntarsa a kapcsolatot a serverrel
    def handleConnection(self):
        while True:
            # meghivom a create_messagge()-t
            message = self.create_messagge()
            # elkuldom a servernek az uzenetet
            self.client.send(message)
            # meghivom a handleIncomingMessageFromRemoteServer()-t
            self.handleIncomingMessageFromRemoteServer()
        # mivel a feladat nem szabott hatart, annak egy kliens hanyszor kerdezhet ezert itt a while vegtelen ciklusban van
        # de egyebkent lehet olyan feladat, amiben nem while True-t, adok
        # ilyenkor a cliens socketet mindenkepp close()-oljuk a vegen
        self.client.close()


# az osztalyt peldanyositom
simpleTCPSelectClient = SimpleTCPSelectClient()
# meghivom a handleConnection()-t
simpleTCPSelectClient.handleConnection()
