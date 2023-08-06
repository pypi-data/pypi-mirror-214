import socket
def connect(ip='127.0.0.1',port=58000,most_connected=3):
    LSC=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LSC.bind((ip,port))
    LSC.listen(most_connected)
    print(f'Server started successfully with port:{port}.')
    DS,addr = LSC.accept()
    print('User connected with ip:', addr[0])
    return DS

def recieve(ds:socket.socket,buflen=1024,end_code='exit',none_code=1,ended_code=2): 
    message=ds.recv(buflen)
    if not message:return none_code
    text=message.decode()
    if text==end_code:return ended_code
    return text

def send_to(ds:socket.socket,text):
    ds.send(text.encode())

def re_ce(ds:socket.socket,function_,buflen=1024,end_code='exit',none_code=1,ended_code=2):
    while True:
        got=recieve(ds=ds,buflen=buflen,end_code=end_code,none_code=none_code,ended_code=ended_code)
        if got==none_code:return none_code
        if got==ended_code:return ended_code
        new=function_(got)
        send_to(ds=ds,text=new)

def example(data):
    print(data)
    return data
"""
ds=connect(ip='')
get=re_ce(ds,example,512)
print(get) 
"""