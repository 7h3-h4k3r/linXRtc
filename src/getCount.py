import threading
import struct
from . import Clients
from lib.Packetconfig import Packet
COUNT_CONN = 0x56
class BroadCastCount:
    def __init__(self):
        self.event = threading.Event()
        self.running = True

    def broadcast_connection(self):
        payload = struct.pack("!B", len(Clients))

        for client in Clients.values():
            Packet.send_packet(client.conn, COUNT_CONN, payload)

    def worker(self):
        while self.running:
            print("Waiting for an event...")
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
        self.event.set()   # Wake the thread if it's waiting
        self.thread.join()