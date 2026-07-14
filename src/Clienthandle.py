import threading 

Clients = []


class Clienthandle(threading.Thread):

    def __init__(self,conn,addr):
        super().__init__()
        self.conn = conn 
        self.addr = addr 



    def setClient(self):
        Client.append(
            {
                'conn':conn,
                'addr':addr
            }
        )

    

    def run(self):

        while True:
            
            data = self.conn.recv(1024)

            if not data:
                break
            
        self.conn.close()
        