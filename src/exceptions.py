class Error(Exception):
    # base class for errors
    pass


class NotFound(Error):
    # raised when a stem / track isn't found
    pass


class InvalidStatusCode(Error):
    # raised when a request isn't 200 or any other successful
    pass
