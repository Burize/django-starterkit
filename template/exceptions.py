class CustomException(Exception):
    """
    Base exception for all exceptions in project
    """

    @property
    def message(self):
        return self.args[0] if self.args else ''


class NotFoundException(CustomException):
    pass

class ForbiddenException(CustomException):
    pass


class PermissionException(CustomException):
    pass
