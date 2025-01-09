import requests
import json
from typing import Dict


def register(reg_info: Dict):
    headers = {'Content-Type': 'application/json'}
    register_url = 'http://localhost:8000/api/register'
    res = requests.post(register_url, json=reg_info, headers=headers).json()
    return res


def login(creds: Dict):
    headers = {'Content-Type': 'application/json'}
    login_url = 'http://localhost:8000/api/login'
    res = requests.post(login_url, json=creds, headers=headers).json()
    return res['token']


def create_chat(auth_headers: Dict, chat_data: Dict):
    chat_url = 'http://localhost:8000/api/chat'
    res = requests.post(chat_url, json=chat_data, headers=auth_headers).json()
    return res


def get_chat(auth_headers: Dict, guid: str = None):
    params = None
    if guid:
        params = {
            'guid': guid
        }
    chat_url = 'http://localhost:8000/api/chat'
    res = requests.get(chat_url, params=params, headers=auth_headers).json()
    return res


def get_user_chats(auth_headers: Dict):
    chat_url = 'http://localhost:8000/api/chat/user'
    res = requests.get(chat_url, headers=auth_headers).json()
    return res


def get_chat_by_id(auth_headers: Dict, chat_id):
    chat_url = f'http://localhost:8000/api/chat/{chat_id}'
    res = requests.get(chat_url, headers=auth_headers).json()
    return res


def patch_chat_by_id(auth_headers: Dict, chat_id, patch_data):
    chat_url = f'http://localhost:8000/api/chat/{chat_id}'
    res = requests.patch(chat_url, headers=auth_headers, json=patch_data).json()
    return res


def delete_chat_by_id(auth_headers: Dict, chat_id):
    chat_url = f'http://localhost:8000/api/chat/{chat_id}'
    res = requests.delete(chat_url, headers=auth_headers).json()
    return res


def invite_user_to_chat(auth_headers: Dict, chat_id, user_data):
    chat_url = f'http://localhost:8000/api/chat/{chat_id}/invite'
    res = requests.post(chat_url, json=user_data, headers=auth_headers).json()
    return res


def main():

    user1 = {
        'username': 'juhuuuuuu1',
        'password': 'testipassu1',
        'email': 'testi1@gmail.com'
    }
    user2 = {
        'username': 'juhuuuuuu2',
        'password': 'testipassu2',
        'email': 'testi2@gmail.com'
    }
    #register(user1)
    #register(user2)

    login1 = {
        'username': 'juhuuuuuu1',
        'password': 'testipassu1',
    }
    login2 = {
        'username': 'juhuuuuuu2',
        'password': 'testipassu2',
    }

    #token1 = login(login1)
    #token2 = login(login2)
    #print(token1)
    #print(token2)

    auth_headers1 = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzY0NTEyNjQsImV4cCI6MTczNjQ1NDg2NCwicm9sZXMiOlsiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoianVodXV1dXV1MSJ9.XptqO04vFHvDUberg4PCGhk5cFWX4KTFRenK48mc512OUJQlFsyFqoioMtNcfAwNTIwic1WMn1_j7BXJJTB27mbWEIIZLo_bWqSSQZ5rg4oA5tO-F_EoX5lJ348G4dWblx7WSfUXqbLYnvwQqDJBuj3oJbn-oD1Ghet_QGXWQCPQPUX3SD0HyBy2R479vlKAQJlPgdYJ7W4NLONVoCGAF-R6duiTZi-eUZGbfvr9F_2qNqi6Gwbze-GK4hjxXxh9VqhMO0BJ0HiRoR5QpzudpRCLpPx1duhx7A1rUearrwEioyPkPjXRknWVsTDsulHf328_3-OYqv88TO031n84pKH1lCS5R8H-PULzQfm3HATUcRnsg5wnBil6jZTtTY7pxscINHZjK1S1LsNPAiR72OLCBBG9aa1BQqmkpr4Es9ZDmqoyR7-audYM21OVjRRYo158gdgd9lC2Kwpx0BqfxeidDYPtwC49qfScl_pBDolADuffnbeP-doBAUANZ6Kxi6v9inrssJMFffuBIemGl2hi2xtnw84e8i0r9ZokK-9IQaYer4IA3iEOe5eePJSHlqlz1_lAW5g7nLHrYJhlLuRF48aGtZaxCeK5t65LDXqZJwXDU_0jcr8A68JAj3aFcVJXVsNwMTUVdDhvJUtoLCD-xQiHBtAL3Lx70rSKNN0'
        #'Authorization': f'Bearer {token1}'
    }
    auth_headers2 = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzY0NTEyNjgsImV4cCI6MTczNjQ1NDg2OCwicm9sZXMiOlsiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoianVodXV1dXV1MiJ9.ab04DkVbJm-cQuj2Ho8cHDGYFjy09FsxP46MC7fFoXLMYT8DXs96jsYA6yVs_9wvKCw4gqha2lrI5vNDSvFwJKKqR5zfWkclOfrx8aOwQYsdyR2nEYAabgp58bz4_TMKJWLGrwZOIgRuATlraYYsGPA_tC6pTIcO8gbXM0TQd434JIZvy52FRmEZH5zexvyGPeVTWk2IXpOE28dQaPyBwhn5JEd5wv8zLpxXnmvuqv6xBk_Fdsh_1a_OgKx8lf-jm94C8iRHVS-4B2Eva8h2jAw1-QqsjRM5IdQfR5ERMB0giT59TXtUW-BXBUoen-kw-FNDGn2btiP7p3Z1SEjdPl1qJH7vywdqRuqVggDxiHG1NKe20RzzY162tw_EOnNPo1_EF7FLcPw-doRKDabHW2O8YbNoiQf6sooOXOsY099xNtjoyaoWf4Xb3DBkU7-l4cbfpnxseP89T8b-D3BhJwR1ReSBe4AGAj9JdpO2yfYHdFfmblC8fdCrU5v2tgbNGG2tC1-VvJDY8MQugf7L706MCzQxZdK-zRK-_LMCPBUiRKOeI-ZLb8QeJykMLXMLHgE9a3-aKyr3YDYklISw2Upra5SbeXj-dHZAJTxeOiOd85AjTOuWUQlgdsIJAGL66PfETdcBgz11NWc0XhVrfySxDE8PnrDYO-PvVIkXOfQ'
        #'Authorization': f'Bearer {token2}'
    }

    chat_data1 = {
        'name': 'public_chat',
        'is_private': False
    }
    chat_data2 = {
        'name': 'private_chat',
        'is_private': True
    }
    #chat1 = create_chat(auth_headers2, chat_data1)
    #chat2 = create_chat(auth_headers2, chat_data2)
    #print(chat1)
    #print(chat2)

    #chats1 = get_user_chats(auth_headers1)
    #chats2 = get_user_chats(auth_headers2)
    #print(chats1)
    #print(chats2)

    #guid1 = 'e08c6ec4-b77a-4c63-a19f-1859ee84ccd1'
    #guid2 = '5560e892-002f-4395-8301-84da92cb32d6'
    #chat1 = get_chat(auth_headers2, guid=guid1)
    #chat2 = get_chat(auth_headers2, guid=guid2)
    #print(chat1)
    #print(chat2)

    #{'id': 11, 'name': 'public_chat', 'is_private': False, 'chat_owner': {'id': 2}, 'guid': 'e08c6ec4-b77a-4c63-a19f-1859ee84ccd1', 'created_at': '2025-01-09T19:34:33+00:00'}  
    #{'id': 12, 'name': 'private_chat', 'is_private': True, 'chat_owner': {'id': 2}, 'guid': '5560e892-002f-4395-8301-84da92cb32d6', 'created_at': '2025-01-09T19:34:37+00:00'}  

    #chat1 = get_chat_by_id(auth_headers1, 4)
    #chat2 = get_chat_by_id(auth_headers2, 4)
    #print(chat1)
    #print(chat2)
    patch_data = {
        'name': 'chat_patch'
    }

    #chat1 = patch_chat_by_id(auth_headers1, 4, patch_data)
    #chat2 = patch_chat_by_id(auth_headers2, 4, patch_data)
    #print(chat1)
    #print(chat2)

    #chat1 = delete_chat_by_id(auth_headers1, 5)
    #chat2 = delete_chat_by_id(auth_headers2, 6)
    #print(chat1)
    #print(chat2)

    user_data1 = {
        'username': 'juhuuuuuu2'
    }
    user_data2 = {
        'username': 'juhuuuuuu1'
    }
    invited1 = invite_user_to_chat(auth_headers1, 4, user_data1)
    invited2 = invite_user_to_chat(auth_headers2, 4, user_data2)
    print(invited1)
    print(invited2)

    exit(1)
    user_chat_url = 'http://localhost:8000/api/chat/user'
    #res = requests.get(user_chat_url, headers=auth_headers)
    res = requests.get(chat_url, headers=auth_headers)
    #res = requests.get(chat_url, params=params, headers=auth_headers)
    print(res)
    print(res.json())

if __name__ == '__main__':
    main()
