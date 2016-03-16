"""
+webApp class
+ Root for hierarchy of classes implementing web applications
+ Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
+ jgb @ gsyc.es
+ TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
+ October 2009 - February 2015
+"""
import socket
import random
class webApp:
    """Root of a hierarchy of classes implementing web applications
    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def minumero(self, request):
        numero = int(request.split(' ')[1][1:])
        return numero

    def suma(self, sumando1, sumando2):
        suma = sumando1 + sumando2
        return suma

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)
        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)
        estado = True
        
        while True:
            print 'Waiting for connections'
            (recvSocket, address) = mySocket.accept()
            print 'HTTP request received (going to parse and process):'
            request = recvSocket.recv(2048)
            print request
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print 'Answering back...'
            if(estado == True):
                entero1 = self.minumero(request)
                recvSocket.send("HTTP/1.1 200 OK\r\n\r\n"
                                + "<html><body><h1>Primer sumando: "
                                + str(entero1) + "</h1></body></html>"
                                + "\r\n")
                estado = False
            else:
                entero2 = self.minumero(request)
                resultado = self.suma(entero2, entero1)
                recvSocket.send("HTTP/1.1 200 OK\r\n\r\n"
                            + "<html><body><h1>Primer sumando: "
                            + str(entero1) + "</h1></body></html>"
                            +"<html><body><h1>Segundo sumando: "
                            + str(entero2) + "</h1></body></html>"
                            +"<html><body><h1>La suma es "
                            + str(resultado)+ "</h1></body></html>"
                            + "\r\n")
                estado = True
            recvSocket.close()

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)
