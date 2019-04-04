#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from vishesh chat room! Now type your name and press enter!",encoding="utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome,encoding="utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg,encoding="utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}",encoding="utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", encoding="utf8"))
            client.close()
            del clients[client]
            if len(clients) == 0:
                SERVER.close()
                sys.exit(0)
                break
            broadcast(bytes("%s has left the chat." % name,))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        print("broadcast")
        sock.send(bytes(prefix,encoding="utf8")+msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33002
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
