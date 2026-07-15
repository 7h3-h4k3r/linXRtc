import threading 
from .linxrtc import linxrtc

Clients = {}

class Clienthandle(threading.Thread):

    def __init__(self,conn,addr):
        super().__init__(daemon=True)
        self.conn = conn 
        self.addr = addr 
        
    def in_conn(self,session):
        username = session.username
        if username in Clients:
            Clients[username].conn.close()
        else:
            Clients[username] = session


    def run(self):
        try:
            session = linxrtc.authentication_syn(self.conn,self.addr)
            print(session)
            self.in_conn(session)
            print(Clients)

            while session.autharized:
            
                data = self.conn.recv(1024)
                print(data.decode())
                if not data:
                    break

        except Exception as e:
            print("connection close",str(e))
            self.conn.close()
            