import requests
import datetime
from time import sleep


# Class which describes main functionality of the bot
class BotHandler:
    # Class constructor. Parameter "token" is your bot token
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    # Main method which returns updates off your bot in the json format
    def get_updates(self, offset=None, timeout=100):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, params)
        result_json = response.json()['result']
        return result_json

    # Method which returns last update with information about user who send message to your bot
    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

    # Method which returns chat id
    def get_chat_id(self):
        chat_id = self.get_last_update()['message']['chat']['id']
        return chat_id

    # Method which returns update id
    def get_update_id(self):
        update_id = self.get_last_update()['update_id']
        return update_id

    # Method which returns first name of the person who send last message
    def get_user_name(self):
        user_name = self.get_last_update()['message']['chat']['first_name']
        return user_name

    # Method which returns text of the last message from user
    def get_message_text(self):
        user_message = self.get_last_update()['message']['text']
        return user_message

    # Method which send message to the user
    def send_message(self, message_text):
        method = 'sendMessage'
        params = {'chat_id': self.get_chat_id(), 'text': message_text}

        response = requests.post(self.api_url + method, params)
        return response


myToken = 'There should be yor bot Token'

bot = BotHandler(myToken)
# This tuple contains greeting keywords
user_greetings = ('hello', 'hi', 'whats up', 'good afternoon')
currentTime = datetime.datetime.now()


def main():
    new_offset = None
    current_day = currentTime.day
    current_hour = currentTime.hour

    bot_greetings = ('Good morning', 'Good afternoon', 'Good evening', 'Hello night owl!')

    while True:
        bot.get_updates(new_offset)

        last_update_id = bot.get_update_id()
        last_chat_user = bot.get_user_name()
        last_chat_message = bot.get_message_text()

        # Greeting for morning
        if (last_chat_message.lower()).strip() in user_greetings and 6 <= current_hour < 12:
            bot.send_message(bot_greetings[0] + ' ' + last_chat_user)

        # Greeting for afternoon
        elif (last_chat_message.lower()).strip() in user_greetings and 12 <= current_hour < 16:
            bot.send_message(bot_greetings[1] + ' ' + last_chat_user)

        # Greeting for evening
        elif (last_chat_message.lower()).strip() in user_greetings and 16 <= current_hour < 24:
            bot.send_message(bot_greetings[2] + ' ' + last_chat_user)

        # Greeting for night
        elif (last_chat_message.lower()).strip() in user_greetings and 0 <= current_hour < 6:
            bot.send_message(bot_greetings[3] + '' + last_chat_user)

        # Case which called if user send message without greeting
        else:
            bot.send_message('Sorry, but right now I can only greet you')

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
