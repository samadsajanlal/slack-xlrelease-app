def get_release_dialog(template=None):
    elements = [
        {
            "label": "Release Name",
            "type": "text",
            "name": "release_title",
            "placeholder": "Enter Release Name"
        }
    ]

    for variable in template["variables"]:
        if variable["showOnReleaseStart"]:
            if variable["type"] == "xlrelease.StringVariable":
                elements.append(
                    {
                        "label": variable["key"].capitalize() if "label" not in variable else variable["label"],
                        "type": "text",
                        "name": variable["key"],
                        "placeholder": variable["key"].capitalize() if "label" not in variable else variable[
                            "label"],
                        "optional": not variable["requiresValue"],
                        "hint": "" if "description" not in variable else variable["description"],
                        "value": "" if "value" not in variable else variable["value"]
                    }
                )

    dialog = {
        "title": "Create new release",
        "submit_label": "Submit",
        "callback_id": "create-release-submit",
        "elements": elements
    }

    return dialog
