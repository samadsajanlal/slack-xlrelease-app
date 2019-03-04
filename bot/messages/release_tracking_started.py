from bot.messages.message import Message


def get_release_tracking_message(username=None, release_data=None, base_url=None, profile=None):
    author = {
        "author_name": "<@{}>".format(username),
        "author_icon": profile["profile"]["image_24"]
    }
    message = Message.get_base_message(author=author)
    url = release_data["id"].replace("Applications/", "").replace("/", "-")
    message["attachments"][0]["title"] = release_data["title"]
    message["attachments"][0]["title_link"] = "{}/#/releases/{}".format(base_url, url)
    message["attachments"][0]["color"] = Message.get_task_message_color(release_data["status"])
    message["attachments"][0]["text"] = "`{}`".format(release_data["status"])
    return message


def get_updated_tracking_message(message=None, release_data=None):
    message["attachments"][0]["color"] = Message.get_task_message_color(release_data["status"])
    message["attachments"][0]["text"] = "`{}`".format(release_data["status"])
    return message
