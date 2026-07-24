from . import linxRTCEx ,Clients
from .Session import Session
import struct
from lib.Packetconfig import Packet
import threading
CONN_SYN =0X01
CONN_ACK = 0X02
GMSG = 0x03
COUNT_CONN = 0x56

event = threading.Event()

def broadcast_connection():

    payload = struct.pack("!B", len(Clients))
    for client in Clients:
        Packet.send_packet(Clients[client].conn,COUNT_CONN, payload)

def boradcast_event():
    while True:
        print('waiting for a event....')
        event.wait()
        event.clear()
        print('Client list changed')
        broadcast_connection()
class linxrtc:

    def __init__(self):
        threading.Thread(target=boradcast_event,daemon=True).start()

    @staticmethod
    def broadcast_message(payload,username):
        offset = 0

        msg_length = payload[offset]
        offset += 1
        msg = payload[offset:offset+msg_length].decode()

        encode_msg = f"{username}:{msg}"


        payload = (
            struct.pack("!B", len(encode_msg)) +
            encode_msg.encode()
        )

        for client_username in Clients:
            if client_username != username:
                Packet.send_packet(Clients[client_username].conn,GMSG,payload)
             

    @staticmethod 
    def w_route(conn,username):
        session = Clients[username]
        
        if not session.autharized:
            raise linxRTCEx('Bad request')
        
        gtype , payload = Packet.recv_packet(conn,gtype=True)
        
        if gtype == 3:
            linxrtc.broadcast_message(payload,username)
        print(payload,gtype)
    

    @staticmethod
    def authentication_ack_send(conn):
       Packet.send_packet(conn, CONN_ACK, b"")

   

    @staticmethod 
    def authentication_syn(conn,addr):
        
        payload = None
        try:
            payload = Packet.recv_packet(conn)
          
        except Exception as e:
            conn.close()
            print(f"[*] Client disconnected {addr[0]}{addr[1]} Err: {str(e)}")
            return
        
        offset = 0

        username_len = payload[offset]
        offset += 1 

        username = payload[offset:offset+username_len].decode()
        offset += username_len
    
        password_len = payload[offset]
        offset +=1 

        password = payload[offset:offset+password_len].decode()
       
        if ((username == 'admin' or username == 'nimki' or username == 'narso') and (password == '1234' or password == 'pass@123')):
            linxrtc.authentication_ack_send(conn)
            event.set()
            return Session.set(username,conn,addr)
                
        else:
            raise linxRTCEx('invalid credentials')
            


            