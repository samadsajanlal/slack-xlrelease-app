def get_task_action_dialog(task=None, action=None):
    elements = [
        {
            "label": "Comment",
            "type": "textarea",
            "name": "comment",
            "placeholder": "Give feedback or place a comment..."
        }
    ]

    dialog = {
        "title": task["title"] if len(task["title"]) < 24 else "{}...".format(task["title"][:20]),
        "submit_label": action.capitalize(),
        "callback_id": "task-action:submit:{}:{}".format(action, task["id"]),
        "elements": elements
    }

    return dialog
