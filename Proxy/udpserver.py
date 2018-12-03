import socket
import sys
import struct


class UDPServer:
    def __init__(self, addr='localhost', port=10000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (addr, port)
        # Bind the socket to the port
        self.server.bind(self.server_address)
        # Sockets from which we expect to read
        self.inputs = [self.server]

    def calculate(self, oper, first, second):
        return {
            '+': first + second,
            '-': first - second,
            '*': first * second,
            '/': first / second
        }[oper]

    # kezeli a kapcsolatokat
    def handleConnections(self):
        while self.inputs:
            try:
                # megkapja az adatot es a cimet az udp clienstol
                data, address = self.server.recvfrom(4096)
                # kicsomagolja a strukturat
                unpacker = struct.Struct('I 1s I')
                unpacked_data = unpacker.unpack(data)
                # a tuple-t 3 valtozonak adja ertekul
                first, oper, second = unpacked_data
                # kiszamolja a feladat megoldasat es a resultnak adja
                result = self.calculate(oper, first, second)
                # valaszol a kliensnek
                self.server.sendto(str(result), address)
                # kiirja mit kapott es mit kuldott
                print "UDPServet got message: " + \
                    str(first) + oper + str(second)
                print "Sent: " + str(result)

            except KeyboardInterrupt:
                print "Close the system"
                for c in self.inputs:
                    c.close()
                self.inputs = []


# udp servert peldanyosit
udpServer = UDPServer()
# meghivja a handleConnections()-t
udpServer.handleConnections()
