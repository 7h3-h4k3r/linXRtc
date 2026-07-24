import socket
from .Clienthandle import Clienthandle
from .linxrtc import linxrtc

linxrtc()

class linxSockEx(Exception):
    pass
    
class linxSock:


    def __init__(self,ip='0.0.0.0',port=7878):
        self.ip = ip
        self.port = port 
        self.server = None
    
    def __set_socket(self):

        print(f"[*] Server start listing {self.ip} - {self.port}")
        try:
            if not self.server:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.server.bind((self.ip,self.port))
            self.server.listen()
        except Exception as e:
            raise linxSockEx(f"Socket Error: {e}")
            


    def run(self):  

        self.__set_socket()
        
        while True:
            
            conn ,addr = self.server.accept()
            
            print(f"[*] Client connection to the server {addr[0]}-{addr[1]}")
            Clienthandle(conn,addr).start()
           
        self.server.close()

        
        
