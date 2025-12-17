import requests

r = requests.get("https://httpbin.org/get")
print("Status:", r.status_code)
print("Headers OK")
