#!/usr/bin/python3
import socket

def show_data(data):
    print (data)


def get_data(conn):
    """
    Recevoir des donnees depuis le serveur
    """
    data=conn.recv(8192)
    return (data.decode())


def get_req():
    """
    Recuperer a la ligne de commande le choix de l'utilisateur
    """
    print("L'URL demande :")
    url=input()
    if url == None:
        print("Choix mualide")
        return None
    else:
        return(('GET' + " " + url + " " + "HTTP/1.0").encode('utf-8'))


def send_get_req():
    return "GET http://www.example.com/index.html HTTP/1.0".encode('utf-8')


def send_choice(chc,sock):
    """
    Envoie le choix de l'utilisateur au serveur
    """
    sock.sendall(chc)

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=('localhost',3000)
sock.connect(server_address)

try:
    req = get_req()
    #req = send_get_req()
    rv = send_choice(req,sock)
     
    res = get_data(sock)
    show_data(res)
finally: 
    sock.close()
