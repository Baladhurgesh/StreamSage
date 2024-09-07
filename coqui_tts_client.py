import requests

url = "http://172.20.252.102:7777/generate_speech"
params = {"text": "Hello,world!"}
response = requests.post(url, params=params)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio saved as output.wav")
else:
    print(f"Error: {response.status_code}")
    print(response.text)