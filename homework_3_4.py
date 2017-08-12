import requests
import os


def get_token():
    authorize_url = 'https://oauth.vk.com/authorize'
    app_id = 6144713
    version = '5.67'
    auth_data = {
        'client_id': APP_ID,
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'display': 'mobile',
        'scope': 'friends',
        'response_type': 'token',
        'v': version
    }
    token = os.getenv('token_vk')
    return token,version


def get_my_friends():
    params = {
        'access_token': get_token()[0],
        'v': get_token()[1],
        'user_id': 199118066
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    my_friends = response.json()['response']['items']
    return my_friends


def get_mutual_friends():
    my_friends = get_my_friends()
    list_of_all_friends = []
    for friend in my_friends:
        params = {
            'access_token': get_token()[0],
            'v': get_token()[1],
            'user_id': friend
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_list = response.json()
        if 'error' in friend_list:  # много несуществующих или забаненных друзей, поэтому выкидывает ошибки.
            pass
        else:
            set_friends = list(friend_list['response']['items'])
            list_of_all_friends.append(set_friends)
    list_of_all_friends.append(my_friends)

    mutual_friends = set.intersection(*[set(item) for item in list_of_all_friends])
    return mutual_friends

print(get_mutual_friends())

