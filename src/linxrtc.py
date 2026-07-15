import struct
import zlib
from . import linxRTCEx
from .Session import Session

PROTO_MAGIC_NUMBER = 0x737269
VERSION = 1
FLAGS = 0
CONN_SYN =0X01
CONN_ACK = 0X02

class linxrtc:

    @staticmethod
    def unpack(header,conn,gtype=False):
        
        magic, version, packet_type, flags, length, recv_checksum = struct.unpack(
        "!HBBBII",
        header)

        payload = conn.recv(length)
        calc_checksum = zlib.crc32(payload)
        if recv_checksum != calc_checksum :
            raise linxRTCEx("[*] Packet Corrupted")
        if gtype:
            return (payload,packet_type)
        else:
            return payload

    
    @staticmethod
    def authentication_ack_send(conn):
        header = struct.pack(
            "!H",
            CONN_ACK
        )

        conn.sendall(header)


    
    @staticmethod 
    def authentication_syn(conn,addr):
        header = conn.recv(13)
        payload = None
        try:
            payload = linxrtc.unpack(header,conn)
            
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
       
        if username == 'admin' and password == '1234':
            linxrtc.authentication_ack_send(conn)
            print("login success")
            return Session.set(username,conn,addr)
                
        else:
            raise linxRTCEx('invalid credentials')
            


            