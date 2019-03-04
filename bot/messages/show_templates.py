from bot.messages.message import Message


def get_templates_message(templates=None):
    message = Message.get_base_message(display_footer=False)
    options = []
    for template in templates:
        options.append({"text": "{}".format(template["title"]), "value": "{}".format(template["id"])})

    actions = [
        {
            "name": "template_list",
            "text": "Select a template...",
            "type": "select",
            "placeholder": "Select a template...",
            "options": options
        }
    ]

    message["attachments"][0]["text"] = "Which template you want to use?"
    message["attachments"][0]["callback_id"] = "create-release-dialog"
    message["attachments"][0]["actions"] = actions
    return message
