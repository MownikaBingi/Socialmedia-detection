import smtplib
import requests

def get_public_ip():
    try:

        response = requests.get("https://httpbin.org/ip")

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

def get_location(ip_address):
    api_key = "2774678e1fd30a"

    api_url = f"http://ipinfo.io/{ip_address}/json"

    if api_key:
        api_url += f"?token={api_key}"

    response = requests.get(api_url)

    print(response.text)
    if response.status_code == 200:
        data = response.json()
        location = f'{data.get("city")}, {data.get("region")}, {data.get("country")}'
    else:
        print(f"Error: Unable to fetch location data. Status code: {response.status_code}")
    
    return location

public_ip = get_public_ip()
location = get_location(public_ip)


smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()

smtpserver.login("demoemail19122001@gmail.com", "reuwczxzmjfvabie")

message = f"Some one is trying to create a twitter account with your email id. \nIP ADDRESS: {public_ip}\nLOCATION: {location}"

smtpserver.sendmail("demoemail19122001@gmail.com", "vimalkeerthi.goudu@gmail.com", message)

smtpserver.quit()


