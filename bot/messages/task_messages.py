from bot.messages import get_task_actions
from bot.messages.message import Message


def get_task_messages(release_title=None, task=None, task_type=None, all_user_config_meta=None, base_url=None):
    if task["status"] in ["COMPLETED", "SKIPPED", "ABORTED"]:
        actions = []
        attachment_text = "`{}`".format(task["status"])
    else:
        actions = get_task_actions(task)
        attachment_text = "`{}`. Take action!".format(task["status"])
        if "owner" in task:
            attachment_text = "`{}` {}, take action!".format(task["status"], task["owner"])
            for config in all_user_config_meta:
                if config["username"] == task["owner"]:
                    attachment_text = "`{}` <@{}>, take action!".format(task["status"],
                                                                        config["slack_user_id"])
                    break

    if "description" in task:
        append_desc = "\n*Description*\n{}\n".format(task["description"])
        attachment_text += append_desc

    if "comments" in task and task["comments"]:
        append_comments = "\n*Comments ({})*\n".format(len(task["comments"]))
        for comment in task["comments"]:
            append_comments = "{}*Added by : {}*\n{}\n\n".format(append_comments,
                                                                 comment["author"] if "author" in comment else "",
                                                                 comment["text"])
        attachment_text += append_comments

    temp_task_id = task["id"][task["id"].find('Phase'):].replace("/", "-")
    temp_release_id = task["id"][:task["id"].find('/Phase')]\
        .replace("Applications/", "")\
        .replace("/", "-")
    url = "{}?openTaskDetailsModal={}".format(temp_release_id, temp_task_id)
    release_url = "{}/#/releases/{}".format(base_url, temp_release_id)

    author = {
        "author_name": task_type,
        "author_icon": "https://cdn0.iconfinder.com/data/icons/planing-and-organization/100/12-512.png"
    }
    footer = {
        "footer": "<{}|{}>".format(release_url, release_title),
        "footer_icon": "https://cdn2.iconfinder.com/data/icons/scrum-project/100/Release2-512.png"
    }
    message = Message.get_base_message(author=author, footer=footer)
    message["attachments"][0]["title"] = task["title"]
    message["attachments"][0]["title_link"] = "{}/#/releases/{}".format(base_url, url)
    message["attachments"][0]["color"] = Message.get_task_message_color(task["status"])
    message["attachments"][0]["text"] = attachment_text
    message["attachments"][0]["callback_id"] = "task-action"
    message["attachments"][0]["actions"] = actions
    return message
