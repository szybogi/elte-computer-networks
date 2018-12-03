import select
import socket
import sys
import struct
import datetime


class SimpleTCPSelectServer:
    def __init__(self, addr='localhost', port=10001, timeout=1):
        self.server = self.setupServer(addr, port)
        # Sockets from which we expect to read
        self.inputs = [self.server]
        # Wait for at least one of the sockets to be ready for processing
        self.timeout = timeout
        # letrehoz egy udpclient socket-et is
        self.udpserver_address = (addr, 10000)
        self.udpclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # ez lesz a feladat szerinti cache, egyekore ures tomb
        self.cache = {}

    def setupServer(self, addr, port):
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = (addr, port)
        server.bind(server_address)

        # Listen for incoming connections
        server.listen(5)
        return server

    # kicsomagolja a structot es stringkent osszefuzve visszaadja
    def unpack_message(self, data):
        unpacker = struct.Struct('I 1s I')
        unpacked_data = unpacker.unpack(data)
        message = str(unpacked_data[0]) + \
            unpacked_data[1] + str(unpacked_data[2])
        return message

    def handleNewConnection(self, sock):
        # A "readable" server socket is ready to accept a connection
        connection, client_address = sock.accept()
        connection.setblocking(0)  # or connection.settimeout(1.0)
        self.inputs.append(connection)

    # meglevo kapcsolat kezelese
    def handleDataFromClient(self, sock):
        # klienstol kap adatot
        data = sock.recv(1024)
        # meghivja az unpack_message()-t
        message = self.unpack_message(data)
        # ha volt adat
        if data:
            # a kliensnek kuldendo adat letrehozasa
            message_to_client = None
            # kiirja mit kapott a klienstol
            print "TCPServer got messagge:" + message
            # ha a kliens kerese mar a cacheben van
            if message in self.cache:
                # lekeri a megoldast es hogy mikor kerult a cachebe
                result, time = self.cache[message]
                # ha ez kevesebb mint 8 masodperc(a feladat mas idot ker de ez konnyen atirhatp)
                if datetime.datetime.now() - time < datetime.timedelta(seconds=8):
                    # ertekul adja a kliensnek szolo valasznak a cache tartalmat
                    message_to_client = result

            # ha a kliensnek szant valasz meg ures
            if message_to_client is None:
                # kapcsolodik az udpserverhez es elkuldi a ki nem csomagolt eredeti uzenetet
                self.udpclient.connect(self.udpserver_address)
                self.udpclient.sendall(data)
                # var a server valaszara
                udp_data = self.udpclient.recv(4096)
                # ha erkezett valasz
                if udp_data:
                    # a servertol kapott valasz
                    print "TCPServer got messagge:" + udp_data
                    # beallitja a kliens valaszat es a cachehez adja az uj megoldast
                    message_to_client = udp_data
                    self.cache[message] = (
                        message_to_client, datetime.datetime.now())

            # valaszol a kliensnek
            sock.sendall(message_to_client)
        else:
            # Interpret empty result as closed connection
            print >>sys.stderr, 'closing', sock.getpeername(), 'after reading no data'
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    # vegig megy az inputban levo kapcsolatokon az alapjan, hogy uj vagy regi
    def handleInputs(self, readable):
        for sock in readable:
            if sock is self.server:
                self.handleNewConnection(sock)
            else:
                self.handleDataFromClient(sock)

    def handleExceptionalCondition(self, exceptional):
        for sock in exceptional:
            print >>sys.stderr, 'handling exceptional condition for', sock.getpeername()
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    # a kapcsolat letrehozasaert es fenntartasaert felel
    def handleConnections(self):
        # amig van az inputsban, olyan kliens akivel nem bontotta a kapcsolatot
        while self.inputs:
            try:
                readable, writable, exceptional = select.select(
                    self.inputs, [], self.inputs, self.timeout)

                if not (readable or writable or exceptional):
                    #print >>sys.stderr, '  timed out, do some other work here'
                    continue
                # meghivja a handleInputs()-t
                self.handleInputs(readable)
                # meghivja a handleExceptionalCondition()-t
                self.handleExceptionalCondition(exceptional)
            except KeyboardInterrupt:
                print "Close the system"
                for c in self.inputs:
                    c.close()
                self.inputs = []


# tcpserver peldanyositasa
simpleTCPSelectServer = SimpleTCPSelectServer()
# a tcp serveren meghivja a handleConnections()-t
simpleTCPSelectServer.handleConnections()
