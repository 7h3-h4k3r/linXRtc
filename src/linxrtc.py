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
SHARE_GROUP_KEY=0x60

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
        offset +=1
        chipertext_len = payload[offset]
        chipertext = payload[offset:offset+chipertext_len].decode()
        offset+=1
        nonce_len = payload[offset]
        nonce = payload[offset+offset+nonce_len].decode()
        encode_msg = f"{username}:{msg}"

        print(msg,' ',chipertext,' ',nonce)
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
        
        if gtype == GMSG:
            linxrtc.broadcast_message(payload,username)
        elif gtype == PING:
            linxrtc.send_latency_message(username)
        elif gtype == SHARE_GROUP_KEY:
            print("Shared group key i got it")
            pass
        

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

        offset += password_len

        public_key_len = struct.unpack(
            "!H",
            payload[offset:offset+2]
        )[0] 
        
        offset+=2

        public_key = payload[offset:offset+public_key_len].decode("utf-8")
        if ((username == 'admin' or username == 'nimki' or username == 'narso') and (password == '1234' or password == 'pass@123')):
            linxrtc.authentication_ack_send(conn)
            broad_cast_count.notify()
            return Session.set(username,conn,addr,public_key)
                
        else:
            broad_cast_count.stop()
            raise linxRTCEx('invalid credentials')

            


            