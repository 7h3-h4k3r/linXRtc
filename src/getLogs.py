import threading
import struct
from . import Clients
from lib.Packetconfig import Packet
SEND_LOG = 0x60

class BroadCastLogs:
    def __init__(self):
        self.event = threading.Event()
        self.running = True

    def broadcast_connection(self,msg):
        payload = struct.pack(
            "!B", 
            len(msg) + msg.encode()
        )

        for client in Clients.values():
            Packet.send_packet(client.conn,SEND_LOG, payload)

    def worker(self):
        while self.running:
            print("Waiting for anv  log sending  event...")
            self.event.wait()
            self.event.clear()

            if not self.running:
                break
            print("Client list changed")
            self.broadcast_connection()

    def start(self):
        self.thread = threading.Thread(target=self.worker, daemon=True)
        self.thread.start()

    def notify(self):
        self.event.set()

    def stop(self):
        self.running = False
        self.event.set()
        self.thread.join()