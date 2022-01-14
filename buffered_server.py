# TODO: Include any necessary import statements
from socket import *
from struct import pack, unpack
FIXED_HEADER_LENGTH = 4 

class BufferedTCPEchoServer(object):
    def __init__(self, host = '', port = 36001, buffer_size = 1024):
        # Save the buffer size to a variable. You'll need this later
        self.buffer_size = buffer_size

        # This variable is used to tell the server when it should shut down. Our implementation of this server is centered
        # around one or more while loops that keeps the server listening for new connection requests and new messages from
        # a connected client. This should continue forever, or until this self.keep_running is set to False. My testing
        # code will use self.keep_running to shutdown the server for one test case 
        self.keep_running = True

        # TODO: Create and bind the server socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))


    # This function starts the server listening for new connections and new messages. It initiates the core loop of our 
    # server, where we loop continuously listening for a new connection, or if we are already connected, listening for a new 
    # message. I recommend breaking the functionality up into helper functions
    # Remember that this server can only talk to one connected client at a time. We'll implement a server that
    # can connect to multiple clients at once in a future project.
    # TODO: * Listen for new connections
    #       * Accept new connections
    #       * Receive messages from the connected client until it disconnects. 
    #           * Be sure to set the bufsize parameter to self.buffer_size when calling the socket's receive function
    #       * When a message is received, remove the first ten characters and then send it back to the client. 
    #           * You can use the slice operator to remove the first 10 characters: shorter_string = my_string_variable[10:] 
    #           * You will need to package the message using the format discussed in the assignment instructions
    #       * On disconnect, attempt to accept a new connection
    #       * This process should continue until self.keep_running is set to False. (The program doesn't need immediately close when the value changes)
    #       * Shutdown the server's socket before exiting the program
    def start(self):
        
        while self.keep_running:
            print('SERVER: listening...')
            self.server_socket.listen(1)
            new_connection, addr = self.server_socket.accept()
            ifconn = True
            
            print('Accepted New Connection')
            while ifconn:
                try:
                    byte_array = new_connection.recv(FIXED_HEADER_LENGTH)
            
                    if byte_array:
                        lengthOfMessage = unpack("!I", byte_array)[0]
                        buffer = b""

                        while len(buffer) < lengthOfMessage:
                            newBuffer = min(self.buffer_size, lengthOfMessage - len(buffer))
                            byte_array = new_connection.recv(newBuffer)
                            buffer += byte_array

                        messageToSend = buffer.decode()
                        shorter = messageToSend[10:]
                        print(shorter)
                        message2 = shorter.encode()
                        packedMessage = pack("!I" + str(len(shorter)) + "s", len(shorter), message2)
                        new_connection.send(packedMessage)

                    else:
                        new_connection.close() 
                        ifconn = False    

                except ConnectionResetError as exc:
                    new_connection.close()
                    ifconn = False


    # This method is called by the autograder when it is ready to shut down your program. You should clean up your server socket
    # here. Note that all other sockets opened by the server also need to be closed once you are done with them. You should be closing
    # the individual client sockets generated by socket.accept() inside of your start() function 
    # TODO: Clean up your server socket
    def shutdown(self):
        print("SERVER: shutting down...")
        self.server_socket.close()


if __name__ == "__main__":
    BufferedTCPEchoServer(host='', port=36001, buffer_size=1024).start()