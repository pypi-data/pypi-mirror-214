class Ci:

    def __init__(self, Host='50.1', tr=1024):
        import socket
        self.trans = tr
        self.HOST = '192.168.' + Host  # Endereço IP do servidor
        self.PORT = 1234  # Porta para comunicação

        # Cria o socket TCP/IP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(None)
        # Conecta-se ao servidor
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_socket.settimeout(300)

    def send(self, data):
        try:
            self.client_socket.settimeout(5)
            message = str({1: 1, 'inf': data, 0: 0})
            self.client_socket.send(message.encode())
            self.client_socket.settimeout(None)
        except:
            self.ence()

    def recv(self):
        from util import validator
        try:
            message = self.client_socket.recv(self.trans).decode()
            if not message:
                self.ence()
            self.client_socket.settimeout(None)
            va, me = validator(message)
            if not va:
                return me['inf']
        except:
            self.ence()

    def ence(self):
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_socket.settimeout(300)