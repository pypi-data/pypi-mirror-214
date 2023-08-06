from src.ens_sdk.utils import config


class ENS:

    def __init__(self):
        self._CLIENT_ID = config('ENCIPHER_CLIENT_ID')
        self._CLIENT_SECRET = config('ENCIPHER_CLIENT_SECRET')
        self._ENS_SERVER = config('ENCIPHER_ENS_SERVER')
        self._ENS_PORT = config('ENCIPHER_ENS_PORT')
        self._API_VERSION = config('ENCIPHER_API_VERSION')

    def build_notification(self):
        ...

    def _send(self, payload=None):
        ...
