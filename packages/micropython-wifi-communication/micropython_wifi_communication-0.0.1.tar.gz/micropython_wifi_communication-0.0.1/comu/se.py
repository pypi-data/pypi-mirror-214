class Se:

    def __init__(self, net=None, Host='50.1', tr=1024):
        self.trans = tr
        import socket
        self.HOST = '192.168.' + Host  # Endereço IP do servidor
        self.PORT = 1234  # self.PORTa para comunicação
        if net:
            if type(net) != dict:
                net = {}
            import network
            SSID = 'MinhaRedeWiFI'  # Nome da rede Wi-Fi
            if 'SSID' in net:
                SSID = net['SSID']
            PASSWORD = 'MinhaSenha123'  # Senha da rede Wi-Fi
            if 'PASSWORD' in net:
                PASSWORD = net['PASSWORD']

            # Configura o ponto de acesso Wi-Fi
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            if PASSWORD != '':
                ap.config(essid=SSID, authmode=network.AUTH_WPA2_PSK, password=PASSWORD)
            else:
                ap.config(essid=SSID)

            network_config = ap.ifconfig()

            # Atualiza o endereço IP do ponto de acesso para o valor de self.HOST
            ap_config = (self.HOST, '255.255.0.0', self.HOST, '255.255.0.0')
            ap.ifconfig(ap_config)

        # Cria o socket TCP/IP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Associa o socket ao endereço IP e self.PORTa
        self.server_socket.bind((self.HOST, self.PORT))

        # Aguarda por conexões
        self.server_socket.listen(1)

        # Aceita uma nova conexão
        self.client_socket, self.client_address = self.server_socket.accept()
        self.client_socket.settimeout(300)
        print("cliente aceito")

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
        # self.client_socket.close()
        self.server_socket.listen(1)
        # Aceita uma nova conexão
        self.client_socket, self.client_address = self.server_socket.accept()
        self.client_socket.settimeout(300)
        print("cliente aceito")