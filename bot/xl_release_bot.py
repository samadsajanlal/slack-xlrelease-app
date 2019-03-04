import json
import logging
import os
import threading

from bot import logger
from bot.db.db_client import DBClient
from bot.db.vault_client import VaultClient
from bot.helper import get_random_string
from bot.helper.config_helper import ConfigHelper
from bot.helper.release_helper import ReleaseHelper
from bot.helper.release_tracker import ReleaseTracker
from bot.helper.task_helper import TaskHelper
from bot.messages.show_help import get_help
from bot.slack.client import Client


class XLReleaseBot(object):
    """ Instanciates a Bot object to handle Slack interactions."""

    def __init__(self):
        super(XLReleaseBot, self).__init__()
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      "scope": "bot,commands,chat:write:bot,channels:write,users.profile:read,team:read",
                      "state": ""}
        self.verification = os.environ.get("SIGNING_SECRET")
        self.slack_client = Client(access_token="", bot_token="")
        self.db_client = DBClient(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))
        self.vault_client = VaultClient(url=os.environ.get("VAULT_URL"), token=os.environ.get("VAULT_TOKEN"))
        self.release_channel_meta = {}
        self.xl_release_config = {}
        self.logger = logging.getLogger(__name__).setLevel(logging.DEBUG)
        self.polling_time = 2

    def new_state(self):
        self.oauth["state"] = get_random_string(string_length=30)
        return self.oauth["state"]

    def auth(self, code=None, state=None):
        """
        A method to exchange the temporary auth code for an OAuth token
        which is then saved it in memory on our Bot object for easier access.
        """
        if state != self.oauth["state"]:
            return False

        auth_response = self.slack_client.oauth_access(client_id=self.oauth['client_id'],
                                                       client_secret=self.oauth['client_secret'],
                                                       code=code)
        self.slack_client = Client(access_token=auth_response["access_token"],
                                   bot_token=auth_response["bot"]["bot_access_token"])

        self.vault_client.set_secret(path="access_token",
                                     secret=auth_response["access_token"])
        self.vault_client.set_secret(path="bot_token",
                                     secret=auth_response["bot"]["bot_access_token"])

        # self.slack_client.post_message(channel=auth_response["user_id"], kwargs=get_slack_installed())
        return True

    def show_help(self, channel_id=None, user_id=None):
        """
        A method to show help!
        """
        self.slack_client.post_ephemeral(channel=channel_id, user=user_id, kwargs=get_help())

    def handle_config_command(self, request_form=None):
        trigger_id = request_form.get('trigger_id')
        config_helper = ConfigHelper(slack_client=self.slack_client,
                                     db_client=self.db_client,
                                     vault_client=self.vault_client)
        config_helper.show_config_dialog(trigger_id=trigger_id)

    def handle_config_dialog_trigger(self, request_form=None):
        payload = json.loads(request_form.get("payload"))
        config_helper = ConfigHelper(slack_client=self.slack_client,
                                     db_client=self.db_client,
                                     vault_client=self.vault_client)
        xl_release_config = {
            "slack_user_id": payload["user"]["id"],
            "xl_release_url": payload["submission"]["xl_release_url"],
            "username": payload["submission"]["username"]
        }
        config_helper.add_configuration(user=payload["user"],
                                        channel=payload["channel"],
                                        xl_release_config=xl_release_config,
                                        secret=payload["submission"]["password"])

    def handle_create_release_command(self, request_form=None):
        user_id = request_form.get('user_id')
        channel_id = request_form.get('channel_id')
        release_helper = ReleaseHelper(slack_client=self.slack_client,
                                       db_client=self.db_client,
                                       vault_client=self.vault_client)

        release_helper.show_templates(user_id=user_id,
                                      channel_id=channel_id)

    def handle_template_callback(self, request_form=None):
        payload = json.loads(request_form.get("payload"))
        template_id = payload["actions"][0]["selected_options"][0]["value"]
        trigger_id = payload["trigger_id"]

        release_helper = ReleaseHelper(slack_client=self.slack_client,
                                       db_client=self.db_client,
                                       vault_client=self.vault_client)

        release_helper.show_template(template_id=template_id,
                                     trigger_id=trigger_id,
                                     user=payload["user"],
                                     channel=payload["channel"],
                                     ts=payload["message_ts"])

    def handle_track_release_command(self, request_form=None):
        user_id = request_form.get('user_id')
        channel_id = request_form.get('channel_id')
        release_tracker = ReleaseTracker(slack_client=self.slack_client,
                                         db_client=self.db_client,
                                         vault_client=self.vault_client)

        release_tracker.show_releases(user_id=user_id,
                                      channel_id=channel_id)

    def handle_release_create_callback(self, request_form=None):
        payload = json.loads(request_form.get("payload"))
        release_helper = ReleaseHelper(slack_client=self.slack_client,
                                       db_client=self.db_client,
                                       vault_client=self.vault_client)

        release = release_helper.create_release(user=payload["user"],
                                                channel=payload["channel"],
                                                data=payload["submission"])
        if release.status_code == 200:
            release_data = release.json()
            release_tracker = ReleaseTracker(slack_client=self.slack_client,
                                             db_client=self.db_client,
                                             vault_client=self.vault_client)
            tracker_thread = threading.Thread(target=release_tracker.track_release,
                                              args=(payload["user"], payload["channel"], release_data["id"], self.polling_time))
            tracker_thread.start()

    def handle_release_track_callback(self, request_form=None):
        payload = json.loads(request_form.get("payload"))
        release_id = payload["actions"][0]["selected_options"][0]["value"]

        release_tracker = ReleaseTracker(slack_client=self.slack_client,
                                         db_client=self.db_client,
                                         vault_client=self.vault_client)

        release_tracker.send_release_track_message(user=payload["user"],
                                                   channel=payload["channel"],
                                                   release_id=release_id,
                                                   ts=payload["message_ts"])
        tracker_thread = threading.Thread(target=release_tracker.track_release,
                                          args=(payload["user"], payload["channel"], release_id, self.polling_time))
        tracker_thread.start()

    def handle_task_trigger(self, request_form=None):
        payload = json.loads(request_form.get("payload"))
        task_action = payload["actions"][0]["name"]
        task_id = payload["actions"][0]["value"]
        trigger_id = payload["trigger_id"]
        task_helper = TaskHelper(slack_client=self.slack_client,
                                 db_client=self.db_client,
                                 vault_client=self.vault_client)
        if task_action == "assign":
            task_helper.assign_to_me_action(user=payload["user"],
                                            channel=payload["channel"],
                                            task_id=task_id,
                                            ts=payload["message_ts"])
        elif task_action in ["complete", "fail", "retry", "skip"]:
            task_helper.show_task_action_dialog(user=payload["user"],
                                                trigger_id=trigger_id,
                                                task_id=task_id,
                                                task_action=task_action)
        else:
            pass

    def handle_task_action(self, request_form=None):
        payload = json.loads(request_form.get("payload"))
        task_data = payload["callback_id"].split(":")
        task_helper = TaskHelper(slack_client=self.slack_client,
                                 db_client=self.db_client,
                                 vault_client=self.vault_client)
        task_helper.task_action(user=payload["user"],
                                task_id=task_data[3],
                                action=task_data[2],
                                comment=payload["submission"]["comment"])

    def recover_restart(self):
        access_token = self.vault_client.get_secret(path="access_token")
        bot_token = self.vault_client.get_secret(path="bot_token")

        if access_token and bot_token:
            self.slack_client = Client(access_token=access_token,
                                       bot_token=bot_token)
            release_tracker = ReleaseTracker(slack_client=self.slack_client,
                                             db_client=self.db_client,
                                             vault_client=self.vault_client)
            release_tracker.restart_tracking(self.polling_time)
