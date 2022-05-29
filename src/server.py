import socket  # for networking
from threading import Thread  # for threading

HOST = '127.0.0.1'  # this address is the "localhost"
PORT = 8080  # port to listen on for clients

# set up the server 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)

# set up the client
list_of_clients = []


def client_thread(conn):
    while True:
        try:
            data = conn.recv(1024)
            broadcast(data, conn)
        except:
            continue


def broadcast(data, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(data)
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


# accept a connection from the client
while True:
    client_socket, client_address = s.accept()

    for client in list_of_clients:
        client.close()
    list_of_clients = [client_socket]

    client_socket.send('p1'.encode())
    Thread(target=client_thread, args=(client_socket,)).start()
    print(f"\nConnected to {client_address}!")

    client_socket, client_address = s.accept()
    list_of_clients.append(client_socket)
    client_socket.send('p2'.encode())
    Thread(target=client_thread, args=(client_socket,)).start()
    print(f"\nConnected to {client_address}!")

    print("\nGAME START !!!")
