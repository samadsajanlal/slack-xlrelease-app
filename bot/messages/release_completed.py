from bot.messages.message import Message


def get_release_completed_message(username=None, base_url=None, release_data=None, profile=None):
    url = release_data["id"].replace("Applications/", "").replace("/", "-")
    emoji = ":ballot_box_with_check:" if release_data["status"] == "ABORTED" else ":white_check_mark: Success!"
    author = {
        "author_name": "<@{}>".format(username),
        "author_icon": profile["profile"]["image_24"]
    }
    message = Message.get_base_message(author=author)
    message["attachments"][0]["title"] = release_data["title"]
    message["attachments"][0]["color"] = Message.get_task_message_color(release_data["status"])
    message["attachments"][0]["title_link"] = "{}/#/releases/{}".format(base_url, url)
    message["attachments"][0]["text"] = "{} Release `{}`".format(emoji, release_data["status"])
    return message
