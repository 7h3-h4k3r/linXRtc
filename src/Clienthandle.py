import threading 
from .linxrtc import linxrtc , U_JOIN,I_KEYS
from . import linxRTCEx ,Clients, public_keys
from lib.Packetconfig  import Packet
import socket
import json

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

            if not session or not getattr(session, "autharized", False):
                print(f"Authentication failed for {self.addr}")
                return

            self.in_conn(session)

            linxrtc.broadcast_message(session.public_key.encode(),session.username,U_JOIN)
            Packet.send_packet(self.conn,I_KEYS,json.dumps({"keys": public_keys}).encode())
            while session.autharized:
                linxrtc.w_route(self.conn,session.username)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print("Client Error",str(e))
        
        finally:
            username = getattr(session, "username", None)
            if username and Clients.get(username) is session:
                del Clients[username]
                print(f"Cleaned up session for {username}")
            
            try:
                print('Connection closed')
                self.conn.close()
            except Exception:
                pass
            