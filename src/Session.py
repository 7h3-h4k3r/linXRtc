from . import linxRTCEx



class Session:

    def __init__(self,username,conn,addr):
        self.username = username
        self.autharized = True
        self.conn = conn
        self.addr = addr
        self.last_ping = 0
        self.next_ping = 0

    @staticmethod
    def set(username,conn,addr):
        if not username:
            raise linxRTCEx('username is not found ')

        if not conn:
            return linxrtc('connection is null') 
        
        return Session(username,conn,addr)
        
        
        
    def get():
        pass

        

        
        