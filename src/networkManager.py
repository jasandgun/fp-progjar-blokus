import socket
import pickle

HOST = socket.gethostbyname(socket.gethostname())  # the server's IP address, defaults to the current machine
PORT = 8080  # the port we're connecting to


class NetworkManager:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"\nConnected to {self.client_socket.getsockname()}!")

    def send_to_server(self, client_data):
        try:
            pickled_data = pickle.dumps(client_data)
            self.client_socket.send(pickled_data)
        except:
            print(f"\nConnection already closed")

    def close_connection(self):
        self.client_socket.close()

    def recv_pickle(self):
        unpickled_data = self.client_socket.recv(4096)
        unpickled_data = pickle.loads(unpickled_data)
        return unpickled_data

    def recv_data(self):
        return self.client_socket.recv(4096).decode()
