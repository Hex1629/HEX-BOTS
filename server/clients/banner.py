banner_main = """\x1b[38;5;196m    ╔%s%s%s%s%s         ·    %s%s%s%s%s╗     \x1b[38;5;76m%s%s \x1b[38;5;226mW\x1b[38;5;227mE\x1b[38;5;228mL\x1b[38;5;229mC\x1b[38;5;230mO\x1b[38;5;231mM\x1b[38;5;255mE \x1b[38;5;255mT\x1b[38;5;231mO \x1b[38;5;230mH\x1b[38;5;229mE\x1b[38;5;228mX \x1b[38;5;227mB\x1b[38;5;226mO\x1b[38;5;227mT\x1b[38;5;228mN\x1b[38;5;229mE\x1b[38;5;230mT
\x1b[38;5;197m▀ ╔██        ▪            ▪  ██╗ ▀ \x1b[38;5;77m%s%s \x1b[38;5;87mT\x1b[38;5;81mI\x1b[38;5;75mM\x1b[38;5;69mE \x1b[38;5;255m%s \x1b[38;5;63mnow
\x1b[38;5;198m ╔╝    •                       ╚╗  \x1b[38;5;78m%s%s 
\x1b[38;5;199m ▪  ┬ ┬┏━┓═╗ ╦    ╔╗ ┏━┓╔╦╗┌─┐  ▪  \x1b[38;5;79m%s%s \x1b[4;1m\x1b[38;5;87mt.me/\x1b[38;5;81mIDKOTHERHEX1629\x1b[0m
\x1b[38;5;200m    ├─┤┣┫ ╔╩╦╝ ── ╠╩╗┃ ┃ ║ └─┐     \x1b[38;5;80m%s%s 
\x1b[38;5;201m ▪  ┴ ┴┗━┛╩ ╚═    ╚═╝┗━┛ ╩ └─┘  ▪  \x1b[38;5;81m%s%s \x1b[38;5;208m┏ \x1b[38;5;202mS \x1b[38;5;203mT \x1b[38;5;204mA \x1b[38;5;205mT \x1b[38;5;206mU \x1b[38;5;207mS \x1b[38;5;208m━ ━ ━
\x1b[38;5;200m ╚╗ ·                  ·       ╔╝  \x1b[38;5;80m%s%s \x1b[38;5;208m┃ \x1b[38;5;118mbots  \x1b[38;5;112m%s
\x1b[38;5;199m▄ ╚██       ▪                ██╝ ▄ \x1b[38;5;79m%s%s \x1b[38;5;208m┃ \x1b[38;5;119mlogin \x1b[38;5;113m%s
\x1b[38;5;198m    ╚%s%s%s%s%s          •   %s%s%s%s%s╝     \x1b[38;5;78m%s%s \x1b[38;5;208m┗ \x1b[38;5;202mS \x1b[38;5;203mT \x1b[38;5;204mA \x1b[38;5;205mT \x1b[38;5;206mU \x1b[38;5;207mS \x1b[38;5;208m━ ━ ━\x1b[0m"""

banner_help = """ \x1b[38;5;196mDISPLAY  %s  \x1b[38;5;202mBANNER   %s  \x1b[38;5;208mCOM-BOT
\x1b[38;5;197m╔═══════╗ \x1b[38;5;76m%s \x1b[38;5;203m╔═══════╗ \x1b[38;5;76m%s \x1b[38;5;209m╔═══════╗
\x1b[38;5;197m║ CLS   ║ \x1b[38;5;77m%s \x1b[38;5;203m║ HUB   ║ \x1b[38;5;77m%s \x1b[38;5;209m║ BOTS  ║
\x1b[38;5;197m╚═══════╝ \x1b[38;5;78m%s \x1b[38;5;203m╚═══════╝ \x1b[38;5;78m%s \x1b[38;5;209m╚═══════╝
\x1b[38;5;198m╔═══════╗ \x1b[38;5;79m%s \x1b[38;5;204m╔═══════╗
\x1b[38;5;198m║ EXIT  ║ \x1b[38;5;80m%s \x1b[38;5;204m║ HELP  ║
\x1b[38;5;198m╚═══════╝ \x1b[38;5;81m%s \x1b[38;5;204m╚═══════╝
          \x1b[38;5;79m%s \x1b[38;5;205m╔═══════╗
          \x1b[38;5;77m%s \x1b[38;5;205m║ TOTAL ║
          \x1b[38;5;76m%s \x1b[38;5;205m╚═══════╝\x1b[0m"""

ascii_art = ["║","┃","│"]
ascii_art2 = ["═", "━", "─"]
ascii_art3 = ["█","▓","▒","░"]

import random

def create_HELP():
   banner = []
   for a in banner_help.split("\n"):
      try:
         banner.append(a%(random.choice((ascii_art)),random.choice((ascii_art))))
      except:banner.append(a%(random.choice((ascii_art))))
   return banner

def create_banner(type="main",value='idk'):
    line = []
    banner_return = []
    if type == "main":
        line = [0,1,6,7,8]
    count = 0
    i2 = 0
    banner = ''
    if type == "main":
       banner =  banner_main
    for a in banner.split("\n"):
        if count in line:
            if count == 1 or count == 7 or count == 6 and type == "main":
               i = value[i2]
               banner_return.append(a%(random.choice((ascii_art)),random.choice((ascii_art)),i))
               i2 += 1
            else:
             if type == "main":
              banner_return.append(a%(random.choice((ascii_art3)),random.choice((ascii_art2)),random.choice((ascii_art3)),random.choice((ascii_art2)),random.choice((ascii_art3)),random.choice((ascii_art3)),random.choice((ascii_art2)),random.choice((ascii_art3)),random.choice((ascii_art2)),random.choice((ascii_art3)),random.choice((ascii_art)),random.choice((ascii_art))))
        else:
           banner_return.append(a%(random.choice((ascii_art)),random.choice((ascii_art))))
        count += 1
    return banner_return
