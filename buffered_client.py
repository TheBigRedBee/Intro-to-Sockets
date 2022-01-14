# TODO: add any import statements required
from socket import *
from struct import pack, unpack
from buffered_server import FIXED_HEADER_LENGTH

class BufferedTCPClient:

    def __init__(self, server_host='localhost', server_port=36001, buffer_size=1024):
        self.buffer_size = buffer_size

        # TODO: Create a socket and establish a TCP connection with server 
        self.connection_socket = socket(AF_INET, SOCK_STREAM)
        self.connection_socket.connect((server_host, server_port))



    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should accept a message
    # from the user, which is packed according to the format specified for this assignment and then sent into the socket.
    # TODO: * Send a message to the server containing the message passed in to the function. 
    #           * Remember to pack it using the format defined in the instructions. 
    def send_message(self, message):
        print("CLIENT: Attempting to send a message...")
        print(message)
        packed_data = pack("!I" + str(len(message)) + "s", len(message), message.encode())
        self.connection_socket.send(packed_data)


    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should wait to receive a 
    # message from the socket, which is then returned to the user. It should return two values: the message received and whether or not it was received 
    # successfully. In the event that it was not received successfully, return an empty string for the message.
    # TODO: * Return the *string* sent back by the server. This should be the same string you sent, except that first 10 characters will have been removed
    #           * Be sure to set the bufsize parameter to self.buffer_size when calling the socket's receive function
    #           * Remember that we're sending packed messages back and forth, for the format defined in the assignment instructions. You'll have to unpack
    #             the message and return just the string. Don't return the raw response from the server.
    #       * Handle any errors associated with the server disconnecting
    def receive_message(self):
        print("CLIENT: Attempting to receive a message...")
        response = self.connection_socket.recv(FIXED_HEADER_LENGTH)
        data_received = True
        buffer = b""

        if response: 
            lengthOfMessage = response[:4]
            lengthOfMessage = unpack("!I", lengthOfMessage)[0]
            message = response[4:]
            while len(message) < lengthOfMessage:
                newBuffer = min(self.buffer_size, lengthOfMessage - len(message))
                response = self.connection_socket.recv(newBuffer)
                message += response
            
            return message.decode(), data_received

        else:
            data_received = False
            return buffer.decode(), data_received

    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should close your socket.
    # TODO: Close your socket
    def shutdown(self):
        print("Client: Attempting to shut down...")
        self.connection_socket.close()

        
if __name__ == "__main__":
    l = BufferedTCPClient(server_host="localhost", server_port=36001)

    l.send_message("Four score and seven years ago")
    response = l.receive_message()
    print(response)
