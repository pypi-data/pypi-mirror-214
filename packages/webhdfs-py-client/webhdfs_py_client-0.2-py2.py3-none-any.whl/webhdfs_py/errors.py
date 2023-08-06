
class WebHdfsException(Exception):
    def __init__(self, msg=str()):
        self.msg = msg
        super(WebHdfsException, self).__init__(self.msg)


class BadRequest(WebHdfsException):
    pass


class Unauthorized(WebHdfsException):
    pass


class FileNotFound(WebHdfsException):
    pass


class MethodNotAllowed(WebHdfsException):
    pass


class ActiveHostNotFound(WebHdfsException):
    pass


class CorrespondHostsNotFound(WebHdfsException):
    pass
