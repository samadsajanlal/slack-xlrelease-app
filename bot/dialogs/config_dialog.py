def get_config_dialog():
    elements = [
        {
            "label": "URL",
            "type": "text",
            "name": "xl_release_url",
            "placeholder": "Enter XL Release URL",
            "subtype": "url",
            "hint": "XL Release URL to connect"
        },
        {
            "label": "Username",
            "type": "text",
            "name": "username",
            "placeholder": "Enter XL Release username",
            "hint": "Login username to connect XL Release Server"
        },
        {
            "label": "Password",
            "type": "text",
            "name": "password",
            "placeholder": "Enter XL Release password",
            "hint": "Login password for entered username"
        }
    ]

    dialog = {
        "title": "Configure XL Release",
        "submit_label": "Submit",
        "callback_id": "add-xl-release-configuration",
        "elements": elements
    }

    return dialog
