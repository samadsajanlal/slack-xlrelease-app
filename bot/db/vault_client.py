import hvac


class VaultClient(object):
    BASE_PATH = "secret"

    def __init__(self, url='http://localhost:8200', token=None):
        self.vault_client = hvac.Client(url=url, token=token)

    def set_secret(self, path=None, secret=None):
        self.vault_client.write("{}/{}".format(self.BASE_PATH, path),
                                value=secret)

    def get_secret(self, path=None):
        record = self.vault_client.read("{}/{}".format(self.BASE_PATH, path))
        return record["data"]["value"] if record else None
