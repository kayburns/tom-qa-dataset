from argparse import ArgumentTypeError
import errno
import os


<<<<<<< HEAD
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr # input expression in which the error occurred
        msg  # explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


=======
>>>>>>> cc6d1cf8d6beb38522c8f72354439128485d129f
def is_file(f):
    try:
        open(f, 'r')  # return an open file handle
    except IOError:
        raise ArgumentTypeError("{0} does not exist".format(f))
    return f



def mkdir_p(path):
    # Copied from http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return path



def remove_extension(path):
    return os.path.splitext(os.path.basename(path))[0]
