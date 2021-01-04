import threading, requests, time
import time
 
def getHtml(url):
    while(1):
        resp = requests.get(url)
        time.sleep(1)
        print(url, len(resp.text), ' chars')
        
 
# 데몬 쓰레드
t1 = threading.Thread(target=getHtml, args=('http://google.com',))
t1.daemon = True 
t1.start()

while(1):
    time.sleep(2)
    print("main")