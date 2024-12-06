__all__ = (
    "QuicksException",
    "PathExistsError",
)


class QuicksException(Exception):
    pass


class PathExistsError(QuicksException):
    pass
