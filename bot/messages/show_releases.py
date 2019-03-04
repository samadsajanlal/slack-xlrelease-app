from bot.messages.message import Message


def get_releases_message(releases=None):
    message = Message.get_base_message(display_footer=False)
    options = []
    for release in releases:
        options.append({"text": "{}".format(release["title"]), "value": "{}".format(release["id"])})

    actions = [
        {
            "name": "release_list",
            "text": "Select a release...",
            "type": "select",
            "placeholder": "Select a release...",
            "options": options
        }
    ]

    message["attachments"][0]["text"] = "Which release you want to track?"
    message["attachments"][0]["callback_id"] = "track-release"
    message["attachments"][0]["actions"] = actions
    return message
