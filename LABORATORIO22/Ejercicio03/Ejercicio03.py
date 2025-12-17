import requests
url =  "https://httpbin.org/get"
response = requests.get(url)
data = response.json()
print("IP:")
print(data["origin"])
print("\nHeaders:")
for key, value in data["headers"].items():
    print(f"{key}: {value}")
print("\nArgs:")
print(data["args"]) 