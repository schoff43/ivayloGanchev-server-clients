#!/usr/bin/python3
import socket
from datetime import datetime
from os import fork
from os import getloadavg
import psutil
import os.path
import magic
class MyTCPServer():
    """
        cette class cree un serveur TCP qui 
        execute un certain nombre d'actions : top(),ser(),date() 
    """
    menu="\nBienvenue \n\
date -affichier la date sur le serveur \n\
top -affichier l'usage cpu sur le serveur \n\
user -affichier les utilisateurs logies \n\
exit - termeneur le session\n\
\n\
Votre choix \n"

    def __init__(self,interface,port,debug):
        self.debug = debug 
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.server_address=(interface,port)
        self.eprint("Initialisation de la socket  \n ")
        
        self.sock.bind(self.server_address)
        self.sock.listen(5)
        self.connection = None
        self.client_address = None
        self.eprint("Initialisation termine")

        self.url = None
        self.protocol = None
        
        self.webroot = "tmp/webroot/" 
    def eprint(self,message):
        if self.debug == 1:
            print(message)

    def send_menu():
        menu="\nBienvenue \n\
      date -affichier la date sur le serveur \n\
      top -affichier l'usage cpu sur le serveur \n\
      user -affichier les utilisateurs logies \n\
      exit - termeneur le session\n\
      \n\
      Votre choix \n"
        return (menu)

    def get_answer(self):
        ans=self.connection.recv(16)
        if ans:
        	cmds=ans.decode()
        	cmd=cmds.rstrip().split("/")[0]
        else:
        	cmd=None
        print(cmd)
        return cmd


    def get_http_req(self):
        ans=self.connection.recv(256)
        if ans:
            req=ans.decode()
            reqs=req.rstrip().split(" ")
            self.url=reqs[1]
            method=reqs[0]
            self.protocol=reqs[2]
            print("method:%s,url:%s,protocol:%s" %(method,self.url,self.protocol))
        else:
        	method=None
        return method


    def send_answer(self,data):
        self.connnection.sendall(data)
    

    def date(self):
        """renvoie le date sur le serveur"""
        x=(datetime.now().strftime('%H:%M:%S %Y/%m/%d '))
        return x


    def user():
        """renoie les utilisateurs ligues sur machine"""
        usr=[]
        for u in psutil.users():
        	usr.append(u[0])
        return (" ".join(usr))
    

    def do_get(self):
        filepath=self.webroot+self.url.rstrip().split("/")[-1]
        print(filepath)
        if os.path.isfile(filepath):
            try:
                html  = open(filepath, 'r')
                content = html.read()
                fileType=magic.from_file(filepath,mime=True)
                fileSize=os.path.getsize(filepath)
                header="Version: "+self.protocol+"\nURL: "+self.url+"\nDate:"+self.date()
                header=header+"\nServer: IFGHTTP 3.0"+"\nFile Type: "+fileType+"\nFile size: "+str(fileSize)
                html.close()
            except:
                content = " "
                header = "403 Erreur access refuse "
        else:
            content=" "
            header="404 Erreur la page n'a pas ete trouve"
        x=header+"\n\n\n"+content 
        return x


    def do_head():
        print("HEADDD CALL")


    def do_put(): 
        print("PUTTTTT CALL")

                    
    def top():
        """renvoie la charge du CPU"""
        return (str(getloadavg()))
    
    
    def send_answer(self,ans):
        self.connection.sendall(ans.encode('utf-8'))
    
    
    commands={"GET":do_get, "PUT":do_put, "HEAD":do_head }
    

    def do_work(self):
        while True:
            self.eprint("Enn attente de nouvelle connection \n")  
            self.connection,self.client_address = self.sock.accept()
            self.eprint("Nouvelle connexion recue")
            pid=fork()
            if pid == 0:
                self.sock.close()
                try:
                    self.eprint("connection depuis %s , pour %s \n" %(self.client_address[0], self.client_address[1]))
                    while True:
                        cmd=self.get_http_req()
                        if cmd is not None and cmd != 'exit':
                            if cmd in self.commands.keys():
                                res=self.commands[cmd](self)
                            else:
                                res = "Command Introuvable \n "
                            self.send_answer(res)
                        else:
                            exit()    
                except Exception as e:
                    print("Problem survenu: %s \n " %str(e)) 
 
                finally:
                    self.eprint("Fermeture de la socket")
                    self.sock.close()
                    exit()
            else:
                self.connection.close()

if __name__ =='__main__':
    tcps=MyTCPServer('localhost',3000,1)
    tcps.do_work()

