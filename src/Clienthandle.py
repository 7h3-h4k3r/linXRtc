import threading 
from .linxrtc import linxrtc
from . import linxRTCEx ,Clients
import socket


class Clienthandle(threading.Thread):

    def __init__(self,conn,addr):
        super().__init__(daemon=True)
        self.conn = conn 
        self.addr = addr 
        
    def in_conn(self,session):
        username = session.username
        if username in Clients:
            old = Clients[username]
            old.autharized = False
            try:

                old.conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass 
            old.conn.close()
            
        Clients[username] = session


    def run(self):
        session = None
        try:
            session = linxrtc.authentication_syn(self.conn,self.addr)
  
            self.in_conn(session)
  
            while session.autharized:
                linxrtc.w_route(self.conn,session.username)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print("Client Error",str(e))
        
        finally:
            if session:
                if Clients.get(session.username) is session:
                    del Clients[session.username]
            self.conn.close()
            