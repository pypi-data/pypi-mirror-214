import warnings

class MiPCException(Exception):
    """
    MiPCのベースエラー。
    """


class MisskeyAPIException(MiPCException):
    """
    API関連のエラー。
    """
    pass


class MisskeyMiAuthFailedException(MiPCException):
    pass