import requests
import time


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
