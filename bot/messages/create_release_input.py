from bot.messages.message import Message


def get_user_input_message(username):
    message = Message.get_base_message(display_footer=False)
    message["attachments"][0]["text"] = "Taking input from <@{}> to create a new release".format(username)
    return message
