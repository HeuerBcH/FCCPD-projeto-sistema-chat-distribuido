import socket
import threading

HOST = '127.0.0.1'
PORT = 50000 
clientes_conectados = []
lock = threading.Lock() # .Lock pra sincronizar o acesso à lista de clientes

def broadcast(message, remetente):
    # Envia uma mensagem para todos os clientes, exceto o remetente
    with lock:
        for cliente in clientes_conectados:
            if cliente != remetente:
                try:
                    cliente.sendall(message)
                except:
                    remover_cliente(cliente)

def remover_cliente(cliente_socket):
    # Remove um cliente da lista de clientes conectados
    if cliente_socket in clientes_conectados:
        clientes_conectados.remove(cliente_socket)

def handle_client(conn, addr):
    # Função executada por cada thread pra lidar com um cliente
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    
    username = ""
    try:
        conn.sendall("Bem-vindo! Por favor, digite seu nome de usuário: ".encode('utf-8'))
        username = conn.recv(1024).decode('utf-8').strip()
        
        with lock:
            clientes_conectados.append(conn)

        broadcast(f"[SERVIDOR]: {username} entrou no chat.\n".encode('utf-8'), conn)
        
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                
                mensagem_formatada = f"[{username}]: {data.decode('utf-8')}"
                print(f"Mensagem recebida de {addr}: {mensagem_formatada}")
                broadcast(mensagem_formatada.encode('utf-8'), conn)

            except ConnectionResetError:
                print(f"[CONEXÃO PERDIDA] Cliente {addr} ({username}) desconectou abruptamente.")
                break 
            
    finally:
        # Com o bloco "finally" n importa se o cliente saiu de forma convencional ou incorreta
        print(f"[CONEXÃO ENCERRADA] {addr} ({username}) desconectou.")
        with lock:
            remover_cliente(conn)

        if username:
            broadcast(f"[SERVIDOR]: {username} saiu do chat.\n".encode('utf-8'), conn)
        
        conn.close()


def main():
    # Função pra iniciar o servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[ESCUTANDO] Servidor está escutando em {HOST}:{PORT}")

    while True:
        # Aceita uma nova conexão
        conn, addr = server_socket.accept()

        # Cria e inicia uma nova thread pra lidar com o cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
