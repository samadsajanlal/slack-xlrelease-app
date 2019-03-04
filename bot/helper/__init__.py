import random
import string

from bot.xlrelease.xl_release_client import XLReleaseClient


def get_task_name(xl_release=None, type_name=None):
    response = xl_release.get_task_definitions()
    if response.status_code == 200:
        type_definitions = response.json()
        for type_definition in type_definitions:
            if type_definition["typeName"] == type_name:
                return "{} : {}".format(type_definition["displayGroup"], type_definition["displayName"])
    return type_name


def get_random_string(string_length=30):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


class Helper(object):
    def __init__(self, slack_client=None, db_client=None, vault_client=None):
        self.slack_client = slack_client
        self.db_client = db_client
        self.vault_client = vault_client

    def get_xl_release(self, user_id=None):
        xl_release_config = self.db_client.get_xl_release_config(user_id=user_id)
        secret = self.vault_client.get_secret(path=user_id)
        return XLReleaseClient(xl_release_config=xl_release_config,
                               secret=secret)
