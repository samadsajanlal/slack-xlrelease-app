"Core exceptions raised by the Bot"


class BotError(Exception):
    pass


class AuthenticationError(BotError):
    pass


class ConnectionError(BotError):
    pass


class TimeoutError(BotError):
    pass


class InvalidResponse(BotError):
    pass


class ResponseError(BotError):
    pass


class DataError(BotError):
    pass
