# 💬 Sistema de Chat Distribuído com Sockets e Threads

Este projeto é uma implementação acadêmica de um sistema de chat multi-cliente, desenvolvido para a disciplina de Fundamentos de Computação Concorrente, Paralela e Distribuída. A solução utiliza a arquitetura **cliente-servidor** em Python, com foco na aplicação prática de conceitos de concorrência e sincronização.

## 🎯 Objetivo

O objetivo principal é demonstrar o funcionamento de um sistema distribuído simples, onde múltiplos clientes podem se conectar a um servidor central para trocar mensagens em tempo real. Cada cliente é gerenciado de forma concorrente, e o acesso a recursos compartilhados no servidor é devidamente sincronizado para garantir a consistência dos dados.

## 🛠️ Arquitetura e Conceitos Aplicados

* **Arquitetura Cliente-Servidor:** Um servidor central (`server.py`) gerencia as conexões e a lógica de comunicação, enquanto múltiplos clientes (`client.py`) podem se conectar para interagir.
* **Comunicação via Sockets TCP:** A comunicação em rede entre cliente e servidor é estabelecida e mantida através de sockets TCP, garantindo uma entrega de mensagens confiável e ordenada.
* **Concorrência com Threads:** O servidor adota o modelo **thread-per-client**, onde cada cliente conectado é gerenciado por uma `threading.Thread` dedicada. Isso permite que o servidor atenda a todos os clientes de forma simultânea e responsiva.
* **Sincronização com `Lock`:** A lista de clientes conectados é um recurso compartilhado entre as threads do servidor. Para evitar condições de corrida, o acesso a essa lista é protegido por um `threading.Lock`, garantindo que apenas uma thread possa modificá-la por vez.

## Funcionalidades

* Conexão de múltiplos clientes simultaneamente.
* Broadcast de mensagens em tempo real para todos os participantes do chat.
* Notificações automáticas do servidor para entradas e saídas de usuários.
* Tratamento de desconexões limpas (via comando `sair`) e abruptas.

## 📁 Estrutura do Projeto

```
sistema-chat-distribuido/
├── server.py      # O script do servidor
└── client.py      # O script do cliente
```

## 🚀 Como Executar

### 1. Pré-requisitos

* Python 3.7 ou superior.

### 2. Iniciar o Servidor

Abra um terminal e execute o seguinte comando para iniciar o servidor. Ele ficará aguardando por conexões na porta `50000`.

```bash
python server.py
```

Você deverá ver a mensagem: `[ESCUTANDO] Servidor está escutando em 127.0.0.1:50000`

### 3. Iniciar os Clientes

Abra **um novo terminal para cada cliente** que você deseja conectar. Execute o comando abaixo em cada um deles.

```bash
python client.py
```

* O programa pedirá que você digite um nome de usuário.
* Após fornecer o nome, você estará conectado ao chat e poderá enviar e receber mensagens.

## 💬 Comandos do Cliente

* **Para enviar uma mensagem:** Simplesmente digite sua mensagem e pressione `Enter`.
* **Para sair do chat (desconexão limpa):** Digite `sair` e pressione `Enter`.

## 🧪 Testes Recomendados

1.  Execute o servidor e conecte 3 ou mais clientes.
2.  Envie mensagens de diferentes clientes e verifique se todos os outros as recebem.
3.  Desconecte um cliente usando o comando `sair` e observe a notificação do servidor nos outros clientes.
4.  Feche a janela de um terminal cliente abruptamente e verifique se o servidor lida com a desconexão e notifica os demais.