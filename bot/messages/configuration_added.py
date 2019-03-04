from bot.messages.message import Message


def get_configuration_added_message(username=None, xl_release_url=None, response=None, profile=None):
    author = {
        "author_name": "<@{}>".format(username),
        "author_icon": profile["profile"]["image_24"]
    }
    message = Message.get_base_message(author=author)
    if response.status_code == 200:
        message["attachments"][0]["title"] = ":white_check_mark: Success!"
        message["attachments"][0]["text"] = "<@{}> is now connected to <{}|XL Release>".format(username, xl_release_url)
        message["attachments"][0]["color"] = Message.STATUS_SUCCESS
    else:
        message["attachments"][0]["title"] = ":x: Failure!"
        message["attachments"][0]["text"] = "Status Code : `{}` \nError :\n" \
                                            "```{}```".format(response.status_code, response.text)
        message["attachments"][0]["color"] = Message.STATUS_FAILURE
    return message
