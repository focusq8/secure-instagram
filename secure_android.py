from uuid import uuid4
import requests

def login_api():
    global req_login, headers_login , username  

    username = input('\n\nEnter Your Username: ')
    password = input('\nEnter Your Password: ') 

    url = 'https://i.instagram.com/api/v1/accounts/login/'

    headers_login = {

        'X-Pigeon-Session-Id': str(uuid4()),
        'X-IG-Device-ID': str(uuid4()),
        'User-Agent': 'Instagram 159.0.0.40.122 Android (25/7.1.2; 240dpi; 1280x720; samsung; SM-G977N; beyond1q; qcom; en_US; 245196089)',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Capabilities': '3brTvx8=',
        "Connection" : 'keep-alive',
        "Accept-Language": "en-US",
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "Accept-Encoding": "gzip, deflate",
        'Host': 'i.instagram.com',
        'Cookie': 'mid=YqejMwABAAExc4QmMCMsnq5YVuEw; csrftoken=BE0qlaD88tnB3vjkLhGksva9WFE2LPYB'
        }
        
    data = {
        'username': username,
        'enc_password': f"#PWD_INSTAGRAM:0:&:{password}",
        "adid": uuid4(),
        "guid": uuid4(),
        "device_id": uuid4(),
        "phone_id": uuid4(),
        "google_tokens": "[]",
        'login_attempt_count': '0'
        }

    req_login = requests.post(url, headers=headers_login, data=data)
    if 'logged_in_user' in req_login.text:
        print(f"[+] Api Logged in with {username}")

    elif "The password you entered is incorrect. Please try again." in req_login.text:
            print(f"{username} ===> password is wrong\n")
            login_api()

    elif "challenge_required" in req_login.text:
        print(f"{username} is secured")
        send_code()

    else:
        input(req_login.text)


def send_code():
    global api_path_url
    api_path_url = req_login.json()['challenge']['api_path']
   
    url_send_code = f"https://i.instagram.com/api/v1{api_path_url}"
    req_send_code = requests.get(url=url_send_code,headers=headers_login).json()
     

    if "phone_number" in req_send_code["step_data"] and "email" in req_send_code["step_data"]:
        print(f'[0] Phone_Number: {req_send_code["step_data"]["phone_number"]} \n[1] Email: {req_send_code["step_data"]["email"]}')
        get_code()

    elif 'contact_point' in req_send_code["step_data"]:
        print(f'[1] Email: {req_send_code["step_data"]["contact_point"]}')
        get_code()
    
    elif 'email' in req_send_code["step_data"]:
        print(f'[1] Email: {req_send_code["step_data"]["email"]}')
        get_code()
            
    elif "phone_number" in req_send_code["step_data"]:
        print(f'[0] Phone_Number: {req_send_code["step_data"]["phone_number"]}')
        get_code()
    
    elif  "phone_number" not in req_send_code["step_data"] and "email" not in req_send_code["step_data"]:
        print("Account needs to confirm it's you ")
    
    else:
        input(req_send_code)
     
def get_code():

    choice = input('choose a number: ')
    url_get_code = f"https://i.instagram.com/api/v1{api_path_url}"
    get_code_data = {
        'choice': str(choice),
        'device_id': uuid4(),
        'guid': uuid4(),
        '_csrftoken': "BE0qlaD88tnB3vjkLhGksva9WFE2LPYB"
        }
    req_get_code = requests.post(url= url_get_code,headers=headers_login,data=get_code_data)
  
    if "step_data" in req_get_code.text:
        print( f'code sent to: {req_get_code.json()["step_data"]["contact_point"]}')
    else:
        input(req_get_code.text)
    security_code = input('\nEnter the security code: ')
    send_code_data = {
            'security_code': str(security_code),
            'device_id': uuid4(),
            'guid': uuid4(),
            '_csrftoken': "BE0qlaD88tnB3vjkLhGksva9WFE2LPYB"
            }
    url_send_code = f"https://i.instagram.com/api/v1{api_path_url}"
    req_send_code = requests.post(url=url_send_code,headers=headers_login, data=send_code_data)

    if "logged_in_user" in req_send_code.text:
        print(f'logged in with {username}')
        get_session = req_send_code.cookies["sessionid"]
        with open(f'{username}.txt', 'w') as file:
            file.write(f'{get_session}')
            print(get_session)
            input(f"[$] Saved as {username}.txt")
        
    elif "Please check the code we sent you and try again." in req_send_code.text:
        print('you entered wrong code , try again')
        get_code()

    elif "This field is required." in req_send_code.text:
        print("Enter the code!")
        get_code()

    elif '"lock":true'  in req_send_code.text:
        input("you need to active code and change password")                                  
    else:
        input(req_send_code.text)
        get_code()


login_api()