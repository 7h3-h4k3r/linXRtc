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
RECV_GROUP_KEY=0x63
U_JOIN=0x61
I_KEYS=0x62
broad_cast_count = BroadCastCount()
broad_cast_count.start()  


class linxrtc:
    @staticmethod
    def send_latency_message(username):
        print('i am sending latacny ',username)
        Packet.send_packet(Clients[username].conn,PONG,b"")

   
    
    @staticmethod
    def broadcast_message(payload,username,state=GMSG):
        if len(payload) < 28:
            raise ValueError("inValied encryption payload")

    
        try:
            payload = (
                struct.pack("!H",len(username.encode()))
                + username.encode()
                + payload
            )
        except Exception as e:
            print(str(e) + "new one")
        for client_username in Clients:
            if client_username != username:
                Packet.send_packet(Clients[client_username].conn,state,payload)

    @staticmethod
    def send_shared_key(username: str, enc_key: bytes) -> bytes:
        encoded_user = username.encode("utf-8")
        
        if len(encoded_user) > 255:
            raise ValueError("Username cannot exceed 255 bytes.")
        if len(enc_key) > 65535:
            raise ValueError("Payload size cannot exceed 65535 bytes.")

        header = struct.pack("!BBH", 
            1,
            len(encoded_user),
            len(enc_key)
        )

        packet = header + encoded_user + enc_key

        Packet.send_packet(Clients[username].conn,RECV_GROUP_KEY,packet)
        
        return True

    @staticmethod
    def get_user_and_pubkey(payload: bytes):
        name_len = payload[0]
        username = payload[1 : 1 + name_len].decode("utf-8")
        
        key_len_start = 1 + name_len
        key_len = int.from_bytes(payload[key_len_start : key_len_start + 2], byteorder="big")
        

        key_start = key_len_start + 2
        enc_key = payload[key_start : key_start + key_len]

        return username, enc_key

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
            c_username , pub_key = linxrtc.get_user_and_pubkey(payload)
            if (linxrtc.send_shared_key(c_username,payload)):
                print('i am sending my shared key to other user sender{} recv {} '.format(username,c_username))
        

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
        if ((username == 'admin' or username == 'nimki' or username == 'narso' or username == 'da') and (password == '1234' or password == 'pass@123')):
            linxrtc.authentication_ack_send(conn)
            broad_cast_count.notify()
            return Session.set(username,conn,addr,public_key)

                
        else:
            broad_cast_count.stop()
            raise linxRTCEx('invalid credentials')

            


            