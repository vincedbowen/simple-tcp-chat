import threading
import socket


class Client:
    def __init__(self):
        self.alias = input("What is your nickname? \n")
        self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.connect()
        self.create_thread_for_client()

    def connect(self):
        self.client.connect(('::1', 8080))

    def client_receive(self):
        while True:
            try:
                message = self.client.recv(512).decode('utf-8')
                if message == 'Welcome to chat!':
                    self.client.send(self.alias.encode('utf-8'))
                else:
                    print(message)
            except socket.error as e:
                print("Disconnected because of {}".format(e))
                self.client.close()
                break

    def client_send(self):
        while True:
            message = self.alias + input(": ")
            self.client.send(message.encode('utf-8'))

    def create_thread_for_client(self):
        receiver_thread = threading.Thread(target=self.client_receive)
        receiver_thread.start()
        sender_thread = threading.Thread(target=self.client_send)
        sender_thread.start()


def main():
    Client()


if __name__ == "__main__":
    main()
