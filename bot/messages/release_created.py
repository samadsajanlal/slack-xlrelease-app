from bot.messages.message import Message


def get_release_created_message(username=None, base_url=None, response=None, profile=None):
    author = {
        "author_name": "<@{}>".format(username),
        "author_icon": profile["profile"]["image_24"]
    }
    message = Message.get_base_message(author=author)
    if response.status_code == 200:
        release_data = response.json()
        url = release_data["id"].replace("Applications/", "").replace("/", "-")
        message["attachments"][0]["title"] = release_data["title"]
        message["attachments"][0]["title_link"] = "{}/#/releases/{}".format(base_url, url)
        message["attachments"][0]["text"] = "`{}`".format(release_data["status"])
        message["attachments"][0]["color"] = Message.get_task_message_color(release_data["status"])
    else:
        message["attachments"][0]["title"] = ":x: Can not create release!"
        message["attachments"][0]["text"] = "Status Code : `{}` \nError :\n" \
                                            "```{}```".format(response.status_code, response.text)
        message["attachments"][0]["color"] = Message.STATUS_FAILURE
    return message
