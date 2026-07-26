from . import linxRTCEx ,Clients
from .Session import Session
import struct
from lib.Packetconfig import Packet
from .getCount import BroadCastCount 

CONN_SYN =0X01
CONN_ACK = 0X02
GMSG = 0x03
COUNT_CONN = 0x56
PONG=0x58
PING=0X57
SET_LATANCY=0X59

broad_cast_count = BroadCastCount()
broad_cast_count.start()  


class linxrtc:
    @staticmethod
    def send_latency_message(username):
        print('i am sending latacny ',username)
        Packet.send_packet(Clients[username].conn,PONG,b"")

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
        elif gtype == PING:
            linxrtc.send_latency_message(username)
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
            broad_cast_count.notify()
            return Session.set(username,conn,addr)
                
        else:
            broad_cast_count.stop()
            raise linxRTCEx('invalid credentials')

            


            