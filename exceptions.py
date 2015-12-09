class DuplicateError(Exception):
    ''' exception raised when a duplicate hash is attempted to be created '''
    pass


class NotFoundError(Exception):
    ''' raised when an object is not found in the database '''
    pass
