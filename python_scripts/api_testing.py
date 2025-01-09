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
    chat_url = f'http://localhost:8000/api/chat/{chat_id}/invite-user'
    res = requests.post(chat_url, json=user_data, headers=auth_headers).json()
    return res


def remove_user_from_chat(auth_headers: Dict, chat_id, user_data):
    chat_url = f'http://localhost:8000/api/chat/{chat_id}/remove-user'
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

    token1 = login(login1)
    token2 = login(login2)
    print(token1)
    print(token2)

    auth_headers1 = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzY0NTU2NTEsImV4cCI6MTczNjQ1OTI1MSwicm9sZXMiOlsiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoianVodXV1dXV1MSJ9.QPHMjSnlCtmAD9jWYiF4A5Iv0fkMD-k8nc6sqhZeztOnJAe2-CZmrkapAo0knfYB5uprBaIIc5z-UhJ8OUCKjoQ5JTbEJbWkLvSwA9xPrRaDiZqH6p73yNq4e_a5VRZ_2DpzLXSPiCB5zGGBU2cZLwo2AL8HbOJEmTYMKJ4VJBgSeKbsINS8-2jRoH8aPhHHiDvkrpba1tOqXEY5CWKMPhwKJgohtnoWcuks5gusP9Fz9khWYCl6u2XyawPPwRhBcZ6CWmMUqM-9WcBOyehNe-7ZEUuOFyo7yrjpzDIM5ewRDrzMe8LbS78wQVuWRcbn92tTbDnBhjjy9kgsKzMBIA6Nj0PbqUZU4NTfI-DmHkTb-Fm06QccNY9giC8NPGhThCpI5NXeAAJABHN3ftA1dP76PjyTffJneNmLhhgivVHLbaS1qlMgfXVLrZ7Whvffm_g8XnCuzGxLqOKXeSlUpDeuQwxsKqk2DalYTKLMdt_N2fDpNfqRBQLLf84GuWAMXKXmNyKuBgQ0EFHKlvJYF_Qkf8TLNzF8KiqRDgcar2ZefBC919sdjFpZK0pMr-4m8cvc3khl8Cqbk6NiqaCywe5kESvSjEsIAa331KTZeY797OKzk61N-jcUTXCE4lboR8RtqDydwasqf1ltaOurQcQnl9jQBdqTfEx1DawjXrg'
        #'Authorization': f'Bearer {token1}'
    }
    auth_headers2 = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzY0NTU2NTUsImV4cCI6MTczNjQ1OTI1NSwicm9sZXMiOlsiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoianVodXV1dXV1MiJ9.aQ4afM13f_ERRkEvsG3wfCk5J-pd08N9UH8RpRYZjybRM9ekhpTrJrrWkoySjLxcoWP6MUyQnaOexLAKzU6ytexo7AifQb-ImvlUogiv3yiDrYj_B41fQAipR9aJD1Vxhqa4MuWVDn8Y1B7tzskBVVKL6e5L49ooYFwbMhZBB323SYRjm-umpkchRivcDSjTh334Pgz3ibEVNyTzRPXOis3XLXllmnSBD0gQ854b6G87-3ooKwxDmA1Pv5efmSFyQbBXXBGxou4X2HxNMOniCjaib_4PRmLqnvbu7zXgzWlECHWRUOi66wNMqQtakCBKSNYN9CrXH9uVVz00OdLUueu8nQeKvZU7ZWcc9TdJEnMTr5AgHI2yKSwZRUdfh_dWCidiLd1kq5Rqd12CJhiT1D4pYeYLLHqW-e7gik46ZaKl6Q5jJa4H0bShM5JJG-FAn1a95T0_Xw9JetWH9HhGMeJnkGFUomq7rBIw1T6315WsHXQREERL-dWf1mK1kCdSRrUUQ3uy47H6BHr_5ENpc6v0cI4TyivCx4LaMPfEnH01p5uxVyvoCkgyS5up_lgc8ZqACN2-f_IlSCH7o0uIpSQ57vegVBqkM3jGsxA0dxkNNPDGm1MqvbhfazoB5MtujmWmao2KiaM9mg0WZMSW3NNkn0rsWVchrDQ-NjhW_2M'
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
    #invited1 = invite_user_to_chat(auth_headers1, 4, user_data1)
    #invited2 = invite_user_to_chat(auth_headers2, 4, user_data2)
    #print(invited1)
    #print(invited2)

    removed = remove_user_from_chat(auth_headers2, 4, user_data2)
    print(removed)

    exit(1)
    user_chat_url = 'http://localhost:8000/api/chat/user'
    #res = requests.get(user_chat_url, headers=auth_headers)
    res = requests.get(chat_url, headers=auth_headers)
    #res = requests.get(chat_url, params=params, headers=auth_headers)
    print(res)
    print(res.json())

if __name__ == '__main__':
    main()
