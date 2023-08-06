class LotrProtocolError(Exception):
    ...


class LotrApiException(Exception):
    ...


class LotrApiBusy(LotrApiException):
    ...


class LotrServerError(LotrApiException):
    ...


class LotrNotFound(LotrApiException):
    ...


class LotrClientException(LotrApiException):
    ...
