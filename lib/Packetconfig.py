import struct
import zlib
from src import linxRTCEx

PROTO_MAGIC_NUMBER = 0x737269
VERSION = 1
FLAGS = 0
HEADER_FORMAT = "!IBBBII"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

class Packet:

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
        
        header = Packet.recv_exact(sock,HEADER_SIZE)

        magic, version, packet_type, flags, length, checksum = struct.unpack(
        HEADER_FORMAT,
        header
        )

        if PROTO_MAGIC_NUMBER != magic:
            raise ValueError("invalid magic number")

        payload = Packet.recv_exact(sock,length)


        if zlib.crc32(payload) != checksum:
            raise ValueError('Checksum failed')

        if gtype:

            return packet_type,payload
        else:
            return payload
