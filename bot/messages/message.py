import time


class Message(object):
    STATUS_FAILURE = "#cb2431"
    STATUS_PENDING = "#dbab09"
    STATUS_SUCCESS = "#28a745"
    XL_RELEASE_BLACK = "#495561"
    XL_RELEASE_FOOTER = "XL Release"
    XL_RELEASE_FOOTER_ICON = "https://avatars0.githubusercontent.com/u/506535" \
                             "?s=400&u=33deea9524c7693dc98a80fd1279216c79da3530&v=4"
    XL_COMPLETED = "#08b153"
    XL_SKIPPED = "#d5d5d5"
    XL_FAILED = "#d94c3d"
    XL_IN_PROGRESS = "#5fcbf4"
    XL_ABORTED = "#d5d5d5"

    @staticmethod
    def get_base_message(author=None, footer=None, display_footer=True):
        attachments = [
            {
                "color": Message.XL_RELEASE_BLACK,
                "mrkdwn_in": ["text", "footer"]
            }
        ]

        if author:
            attachments[0]["author_name"] = author["author_name"]
            attachments[0]["author_icon"] = author["author_icon"]

        if display_footer:
            attachments[0]["ts"] = time.time()
            attachments[0]["footer"] = footer["footer"] if footer else Message.XL_RELEASE_FOOTER
            attachments[0]["footer_icon"] = footer["footer_icon"] if footer else Message.XL_RELEASE_FOOTER_ICON

        message = {
            "attachments": attachments
        }
        return message

    @staticmethod
    def get_task_message_color(status=None):
        if status == "COMPLETED":
            return Message.XL_COMPLETED
        elif status == "SKIPPED":
            return Message.XL_SKIPPED
        elif status == "FAILED":
            return Message.XL_FAILED
        elif status == "ABORTED":
            return Message.XL_ABORTED
        else:
            return Message.XL_IN_PROGRESS
