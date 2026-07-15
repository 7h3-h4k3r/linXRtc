from . import linxRTCEx



class Session:

    def __init__(self,username,conn,addr):
        self.username = username
        self.autharized = True
        self.conn = conn
        self.addr = addr

    @staticmethod
    def set(username,conn,addr):
        if not username:
            raise linxRTCEx('username is not found ')

        if not conn:
            return linxrtc('connection is null') 
        
        return Session(username,conn,addr)
        
        
        
    def get():
        pass

        

        
        