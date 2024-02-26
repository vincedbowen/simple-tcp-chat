import threading
import socket


class Server:
    def __init__(self):
        # local host ip address for ipv6
        self.host = '::1'
        # port for this pseudo web application
        self.port = 8080
        self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.client_addrs = []
        self.aliases = []

    def send_message_to_clients(self, message):
        for client in self.client_addrs:
            client.send(message)

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(512)
                self.send_message_to_clients(message)
            except socket.error as e:
                self.client_addrs.remove(client)
                client.close()
                nickname = self.aliases[self.client_addrs.index(client)]
                self.aliases.remove(nickname)
                self.send_message_to_clients(('{} has disconnected due to {}'.format(nickname, e)).encode('utf-8'))
                break

    def receive_connections(self):
        while True:
            print("Server is listening for connections...")
            client, addr = self.server.accept()
            self.client_addrs.append(client)
            print("Connection established from {}".format(str(addr)))
            client.send('Welcome to chat!'.encode('utf-8'))
            nickname = client.recv(512)
            self.aliases.append(nickname)
            self.send_message_to_clients('{} has joined the chat!'.format(nickname).encode('utf-8'))
            self.create_thread_for_client(client)

    def create_thread_for_client(self, client):
        thread = threading.Thread(target=self.handle_client, args=(client,))
        thread.start()


def main():
    server = Server()
    server.receive_connections()

if __name__ == "__main__":
    main()
