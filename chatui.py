#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *

firstclick = True

def on_entry_click(event):
    global firstclick

    if firstclick:
        firstclick = False
        entry_field.delete(0, "end")


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break
def reverse(s):
    return s[::-1]


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        root.quit()

    if msg == reverse(msg):
        client_socket.send(bytes(msg + " is a pallindrome" ,encoding="utf8"))
    else:
        client_socket.send(bytes(msg + " is a not pallindrome", encoding="utf8"))



def on_closing(event=None):
    my_msg.set("{quit}")
    send()

root = Tk()
root.title("ChatIO")

messages_frame = Frame(root)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = Entry(root, textvariable=my_msg)
entry_field.bind('<FocusIn>', on_entry_click)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(root, text="Send", command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)

#----Socket code----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33002
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(AF_INET, SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
root.mainloop()
