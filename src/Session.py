from . import linxRTCEx 
from . import  public_keys


class Session:

    def __init__(self,username,conn,addr,public_key):
        self.username = username
        self.autharized = True
        self.conn = conn
        self.addr = addr
        self.public_key = public_key
        self.last_ping = 0
        self.next_ping = 0

    @staticmethod
    def set(username,conn,addr,public_key):
        if not username:
            raise linxRTCEx('username is not found ')

        if not conn:
            return linxRTCEx('connection is null') 
        
        if username in public_keys:
            return linxRTCEx('username is alreay in connection')
        public_keys[username] = public_key
        return Session(username,conn,addr,public_key)
        
        
        
    def get_keys():
        return public_keys

        

        

        
        