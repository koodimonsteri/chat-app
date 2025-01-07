import requests
import json

def main():

    user_data = {
        'username': 'juhuuuuuu2',
        'password': 'testipassu2',
        'email': 'testi2@gmail.com'
    }
    headers = {'Content-Type': 'application/json'}
    register_url = 'http://localhost:8000/api/register'
    #res = requests.post(register_url, data=json.dumps(user_data), headers=headers)
    #print(res)
    #print(res.json())

    login_url = 'http://localhost:8000/api/login'
    login_data = {
        'username': 'juhuuuuuu2',
        'password': 'testipassu2',
    }
    login_req = requests.post(login_url, data=json.dumps(login_data), headers=headers)
    print(login_req)
    login_res = login_req.json()
    print(login_res)
    token = login_res['token']
    auth_headers = {
        'Content-Type': 'application/json',
        #'Authorization': f'Bearer xxx'
        'Authorization': f'Bearer {token}'
    }
    chat_url = 'http://localhost:8000/api/chats'
    res = requests.get(chat_url, headers=auth_headers)
    print(res)
    print(res.json())

if __name__ == '__main__':
    main()
