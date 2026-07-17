import struct
import zlib
from . import linxRTCEx
from .Session import Session

PROTO_MAGIC_NUMBER = 0x737269
VERSION = 1
FLAGS = 0
CONN_SYN =0X01
CONN_ACK = 0X02
GMSG = 0x03
HEADER_FORMAT = "!IBBBII"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)



class linxrtc:

    @staticmethod
    def send_packet(sock, packet_type, payload, flags=0):
        checksum = zlib.crc32(payload)

        header = struct.pack(
            HEADER_FORMAT,
            PROTO_MAGIC_NUMBER,
            VERSION,
            packet_type,
            flags,
            len(payload),
            checksum
        )

        sock.sendall(header + payload)
    @staticmethod
    def recv_exact(sock,size):

        data = b""
        
        while len(data) < size:
            
            chunk = sock.recv(size - len(data))
        
            if not chunk:
                raise linxRTCEx('Connection Error')
            
            data += chunk 
        
        return data 
    
    @staticmethod
    def recv_packet(sock,gtype=False):
        print('packet unpack')
        header = linxrtc.recv_exact(sock,HEADER_SIZE)

        magic, version, packet_type, flags, length, checksum = struct.unpack(
        HEADER_FORMAT,
        header
        )

        if PROTO_MAGIC_NUMBER != magic:
            raise ValueError("invalid magic number")

        payload = linxrtc.recv_exact(sock,length)

        if zlib.crc32(payload) != checksum:
            raise ValueError('Checksum failed')

        if gtype:

            return packet_type,payload
        else:
            return payload
   
    @staticmethod 
    def w_route(conn):
        gtype , payload = linxrtc.recv_packet(conn,gtype=True)
        print(payload,gtype)
    
    @staticmethod
    def authentication_ack_send(conn):
       linxrtc.send_packet(conn, CONN_ACK, b"")

   

    @staticmethod 
    def authentication_syn(conn,addr):
        
        payload = None
        try:
            payload = linxrtc.recv_packet(conn)
          
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
       
        if ((username == 'admin' or username == 'nimki') and password == '1234'):
            linxrtc.authentication_ack_send(conn)
            return Session.set(username,conn,addr)
                
        else:
            raise linxRTCEx('invalid credentials')
            


            