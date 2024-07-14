import smtplib
import requests

import socket

def get_public_ip():
    try:
        # Make a request to httpbin.org to get your public IP address
        response = requests.get("https://httpbin.org/ip")

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            public_ip = data.get("origin")
            return public_ip
        else:
            print(f"Error: Unable to fetch public IP address. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Get your public IP address
public_ip = get_public_ip()

hostname = socket.gethostname()
print(hostname)
IPAddr = socket.gethostbyname(hostname)
print(IPAddr)

ip_add = get_public_ip()


ip_address = str(IPAddr)
def get_location(ip_address):
    api_key = "2774678e1fd30a"

    api_url = f"http://ipinfo.io/{ip_address}/json"

    if api_key:
        api_url += f"?token={api_key}"
    response = requests.get(api_url)

    print(response.text)
    if response.status_code == 200:
        data = response.json()
        print(data)
        location = f'{data.get("city")}, {data.get("region")}, {data.get("country")}'
        print("IP Address:", data.get("ip"))
        print("Location:", location)
        print("Coordinates:", data.get("loc"))
    else:
        print(f"Error: Unable to fetch location data. Status code: {response.status_code}")
    
    return location

location = get_location(ip_add)
