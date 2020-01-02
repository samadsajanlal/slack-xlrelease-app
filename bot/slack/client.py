from slack import WebClient


class Client(object):

    def __init__(self, access_token=None, bot_token=None):
        self.user_client = WebClient(token=access_token)
        self.bot_client = WebClient(token=bot_token)

    def open_dialog(self, trigger_id=None, dialog=None):
        return self.bot_client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog=dialog
        )

    def post_message(self, channel=None, kwargs=None):
        return self.bot_client.api_call(
            "chat.postMessage",
            channel=channel,
            **kwargs
        )

    def update_message(self, channel=None, ts=None, kwargs=None):
        return self.bot_client.api_call(
            "chat.update",
            channel=channel,
            ts=ts,
            **kwargs
        )

    def delete_message(self, channel=None, ts=None):
        return self.bot_client.api_call(
            "chat.delete",
            channel=channel,
            ts=ts
        )

    def post_ephemeral(self, channel=None, user=None, kwargs=None):
        return self.bot_client.api_call(
            "chat.postEphemeral",
            channel=channel,
            user=user,
            **kwargs
        )

    def oauth_access(self, client_id=None, client_secret=None, code=None):
        return self.bot_client.api_call("oauth.access",
                                        client_id=client_id,
                                        client_secret=client_secret,
                                        code=code)

    def get_user_profile(self, user_id=None):
        return self.user_client.api_call("users.profile.get",
                                         user=user_id)
