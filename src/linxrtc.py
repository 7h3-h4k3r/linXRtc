from . import linxRTCEx ,Clients
from .Session import Session
import struct
from lib.Packetconfig import Packet
import json
from .getCount import BroadCastCount 
from . import public_keys

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
    def send_shared_key(sender_name: str, target_user: str, enc_key: bytes) -> bool:
        encoded_sender = sender_name.encode("utf-8")
        
        if len(encoded_sender) > 255:
            raise ValueError("Sender username cannot exceed 255 bytes.")
        if len(enc_key) > 65535:
            raise ValueError("Key size cannot exceed 65535 bytes.")

        # 4-byte header: version (1B), sender_name_len (1B), key_len (2B)
        header = struct.pack("!BBH", 
            1, 
            len(encoded_sender), 
            len(enc_key)
        )

        packet = header + encoded_sender + enc_key

        # Send to target client's connection
        Packet.send_packet(Clients[target_user].conn, RECV_GROUP_KEY, packet)
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
            target_user , enc_key = linxrtc.get_user_and_pubkey(payload)
            
            if target_user in Clients:
                linxrtc.send_shared_key(
                    sender_name=username,
                    target_user=target_user,
                    enc_key=enc_key
                )
                print(f"Relayed shared key from {username} -> {target_user}")
        

        print(payload,gtype)
    

    @staticmethod
    def authentication_ack_send(conn):
       Packet.send_packet(conn, CONN_ACK, b"")

    @staticmethod 
    def share_pub_keys(conn):
        payload_data = {
            "type": "init_keys",
            "keys": public_keys
        }
        payload = json.dumps(payload_data).encode("utf-8")

        Packet.send_packet(
            sock=conn,
            packet_type=I_KEYS,
            payload=payload
        )

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

            


            