import socket
import struct
import sys
def receiver(name):
    # Configurações
    MULTICAST_GROUP = '224.3.29.71'
    MULTICAST_PORT = 5007
    # Criar socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
    socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    # Grupo multicast
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
    mreq)
    # Receber e exibir mensagens
    while True:
        print(f"Receptor {name}, aguardando mensagens...")
        data, addr = sock.recvfrom(1024)
        msg, addr = sock.recvfrom(1024)

        if msg.decode('utf-8') == "sair":
            break
        else:
            print(f"Recebido de {addr}: {data.decode('utf-8')}")
        

def sender(name):
    # Configurações
    MULTICAST_GROUP = '224.3.29.71'
    MULTICAST_PORT = 5007
    # Criar socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
    socket.IPPROTO_UDP)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    # Enviar mensagem
    message = 0
    while message != "sair":
        message = input("Digite uma mensagem (ou 'sair' para encerrar): ")
        messageComplete = f"Mensagem de {name}: {message}"
        sock.sendto(messageComplete.encode('utf-8'), (MULTICAST_GROUP, MULTICAST_PORT))
        sock.sendto(message.encode('utf-8'), (MULTICAST_GROUP, MULTICAST_PORT))
    

def main(peer_type, user_name):
    if peer_type == "receptor":
        receiver(user_name)
    if peer_type == "emissor":
        sender(user_name)
    
if __name__ == '__main__':
    peer_type = sys.argv[1]
    user_name = sys.argv[2]

    main(peer_type, user_name)

