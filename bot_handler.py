import requests


# Class which describes main functionality of the bot
class BotHandler:
    # Class constructor. Parameter "token" is your bot token
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        self.getUpdates = 'getUpdates'
        self.update_id = 1
        self.chat_id = 1
        self.user_name = 'user_name'
        self.user_message = 'user_message'

    # Main method which returns updates off your bot in the json format
    def get_updates(self, offset=None, timeout=100):
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + self.getUpdates, params)
        result_json = response.json()['result']
        return result_json

    # Method which returns last update with information about user who send message to your bot
    def get_last_update(self):
        get_result = self.get_updates()
        last_update = get_result[-1]

        self.chat_id = last_update['message']['chat']['id']
        self.update_id = last_update['update_id']
        self.user_name = last_update['message']['chat']['first_name']
        self.user_message = last_update['message']['text']

        return last_update

    # Method which send message to the user
    def send_message(self, message_text):
        method = 'sendMessage'
        params = {'chat_id': self.chat_id, 'text': message_text}

        response = requests.post(self.api_url + method, params)
        return response
