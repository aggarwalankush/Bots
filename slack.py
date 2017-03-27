import time

from slackclient import SlackClient

slack_client = SlackClient("your_slack_token")
BOT_NAME = "your_bot_name"
BOT_ID = ""  # it will be auto generated


def get_bot_id():
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')
    else:
        return None


def handle_command(command, channel):
    if command.strip().lower().startswith(("hello", "hey", "hi")):
        response = "What's up?"
    else:
        response = "Can't help you with that yet"

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_messages(messages):
    if messages and len(messages) > 0:
        for message in messages:
            at_bot = "<@" + BOT_ID + ">"
            if is_valid_message(message) and not is_from_bot(message) \
                    and (at_bot in message.get('text') or is_direct_message(message)):
                split_part = message.get('text').split(at_bot)
                if len(split_part) > 1:
                    return split_part[1], message.get('channel')
                else:
                    return split_part[0], message.get('channel')

    return None, None


def is_direct_message(message):
    return message and message.get('channel', '').startswith('D')


def is_valid_message(message):
    return message and 'text' in message


def is_from_bot(message):
    return message and message.get('user') == BOT_ID


if __name__ == "__main__":
    BOT_ID = get_bot_id()
    if slack_client.rtm_connect():
        print("Slack bot is running")
        while True:
            command, channel = parse_messages(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
