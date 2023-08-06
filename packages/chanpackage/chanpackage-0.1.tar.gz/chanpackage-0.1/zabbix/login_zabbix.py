import requests
import urllib3
import time
from datetime import datetime
import requests
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login(url,user,password,new_login: bool=False):
    get_cokie = authorization()
    if get_cokie == False or new_login:
        URL = url
    
        payload = { 
            "name": str(user), 
            "password": str(password) ,
            "autologin":1,
            "enter":"Sign in",
        } 

        s = requests.session()
        response = s.post(URL, data=payload) 
        # print(response.status_code) # If the request went Ok we usually get a 200 status. 
        # print(response.cookies.values()[0])
        save_cookie(str(response.cookies.values()[0]))
        return str(response.cookies.values()[0])
    else:
        return get_cokie

def authorization():
    
    try:
            # Opening JSON file
        with open('cookie.json', 'r') as openfile:
        
            # Reading from json file
            json_object = json.load(openfile)
        
        if time.time() - json_object['time'] <= 86400:
            return json_object['cookie']
        else:
            return False
    except:
        return False
    
def save_cookie(cookie_save):
    # Data to be written
    dictionary = {
        "name": "cookie",
        "rollno": 56,
        "cgpa": 8.6,
        "cookie": cookie_save,
        "time":time.time(),
        "date_time":datetime.utcfromtimestamp(time.time()+25200).strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    
    # Writing to sample.json
    with open("cookie.json", "w") as outfile:
        outfile.write(json_object)
 