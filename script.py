import datetime
import requests

from bot_handler import BotHandler

# TODO: Move the token to the config file or to the environment variable
myToken = ''

bot = BotHandler(myToken)
# This tuple contains greeting keywords
user_greetings = ('hello', 'hi', 'whats up', 'good afternoon')
bot_greetings = ('Good morning', 'Good afternoon', 'Good evening', 'Hello night owl!')
currentTime = datetime.datetime.now()


# TODO: Make class for Youtube API
def video_search(request_text):
    search_url = 'https://www.youtube.com/results?search_query='
    text = request_text.split()
    converted_text = '+'.join(text)
    response = requests.get(search_url + converted_text)

    return response.url


def answer(mess_text, user, hour):
    if (mess_text.lower()).strip() in user_greetings and 6 <= hour < 12:
        bot.send_message(bot_greetings[0] + ' ' + user)

    elif (mess_text.lower()).strip() in user_greetings and 12 <= hour < 16:
        bot.send_message(bot_greetings[1] + ' ' + user)

    elif (mess_text.lower()).strip() in user_greetings and 16 <= hour < 24:
        bot.send_message(bot_greetings[2] + ' ' + user)

    elif (mess_text.lower()).strip() in user_greetings and 0 <= hour < 6:
        bot.send_message(bot_greetings[3] + '' + user)

    elif ((mess_text.lower()).strip()).find('search') != -1:
        search_text = mess_text.split(' ', 1)
        bot.send_message('Your search result \n' + video_search(search_text[1]))

    else:
        bot.send_message('Sorry but I can\'t answer your message')


def main():
    new_offset = None

    while True:
        current_hour = currentTime.hour
        bot.get_updates(new_offset)

        last_update_id = bot.update_id
        last_chat_user = bot.user_name
        last_chat_message = bot.user_message

        answer(last_chat_message, last_chat_user, current_hour)

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
