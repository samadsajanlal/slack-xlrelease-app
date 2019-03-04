from bot.dialogs.config_dialog import get_config_dialog
from bot.helper import Helper
from bot.messages.configuration_added import get_configuration_added_message
from bot.xlrelease.xl_release_client import XLReleaseClient


class ConfigHelper(Helper):

    def __init__(self, slack_client=None, db_client=None, vault_client=None):
        super(ConfigHelper, self).__init__(slack_client=slack_client, db_client=db_client, vault_client=vault_client)

    def show_config_dialog(self, trigger_id=None):
        """
        A method to configure XL Release URL, username and password
        """
        dialog = get_config_dialog()
        self.slack_client.open_dialog(trigger_id=trigger_id, dialog=dialog)

    def add_configuration(self, user=None, channel=None, xl_release_config=None, secret=None):
        self.db_client.insert_xl_release_config(user_id=user["id"], xl_release_config=xl_release_config)
        self.vault_client.set_secret(path=user["id"], secret=secret)
        xl_release = XLReleaseClient(xl_release_config=xl_release_config,
                                     secret=secret)
        response = xl_release.get_user()

        user_profile = self.slack_client.get_user_profile(user_id=user["id"])
        message = get_configuration_added_message(username=user["name"],
                                                  xl_release_url=xl_release_config["xl_release_url"],
                                                  response=response,
                                                  profile=user_profile)
        self.slack_client.post_message(channel=channel["id"],
                                       kwargs=message)
