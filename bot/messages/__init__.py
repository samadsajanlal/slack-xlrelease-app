def get_task_actions(task):
    actions = [
        {
            "name": "assign",
            "text": "Assign to me",
            "type": "button",
            "value": task["id"]
        }
    ]
    if task["type"] == "xlrelease.Task":
        if task["status"] != "FAILED":
            actions.append(
                {
                    "name": "complete",
                    "text": "Complete",
                    "type": "button",
                    "value": task["id"]
                }
            )
            actions.append(
                {
                    "name": "fail",
                    "text": "Fail",
                    "type": "button",
                    "value": task["id"]
                }
            )

    actions.append(
        {
            "name": "skip",
            "text": "Skip",
            "type": "button",
            "value": task["id"]
        }
    )

    if task["status"] == "FAILED":
        actions.append(
            {
                "name": "retry",
                "text": "Retry",
                "type": "button",
                "value": task["id"]
            }
        )
    return actions
