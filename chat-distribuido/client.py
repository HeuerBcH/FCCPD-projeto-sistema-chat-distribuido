import socket
import threading
import os

def receive_messages(client_socket):
    # Função pra receber mensagens do servidor continuamente
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                # Servidor fechou a conexão ou o cliente desconectou
                print("\n[Conexão com o servidor encerrada.]")
                # Força a saída do programa pra evitar que o input continue esperando
                os._exit(0)
                break
        except:
            # Ocorre quando a conexão é perdida de forma inesperada
            print("\n[Conexão perdida. Pressione Enter para sair.]")
            os._exit(0)
            break

def send_messages(client_socket):
    try:
        # Primeiro envia o nome de usuário
        username = input()
        client_socket.sendall(username.encode('utf-8'))

        # Loop pra enviar mensagens do chat
        while True:
            message = input()
            if message.lower() == 'sair':
                break
            
            # Envia a mensagem se não for o comando de sair
            client_socket.sendall(message.encode('utf-8'))

    except KeyboardInterrupt:
        # Permite saída com Ctrl+C
        print("\nVocê desconectou do chat.")

    finally:
        # Permite que a conexão feche de forma limpa
        print("[Encerrando a conexão...]")
        client_socket.close()

def main():
    HOST = '127.0.0.1'
    PORT = 50000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Verifique se ele está online.")
        return

    # A primeira mensagem do servidor é pedindo o nome de usuário
    welcome_message = client_socket.recv(1024).decode('utf-8')
    print(welcome_message, end="")

    # Cria uma thread pra receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True # Permite que o programa principal saia mesmo que a thread esteja rodando
    receive_thread.start()

    # A thread principal cuidará do envio de mensagens
    send_messages(client_socket)

if __name__ == "__main__":
    main()