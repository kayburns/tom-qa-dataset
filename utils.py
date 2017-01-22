from argparse import ArgumentTypeError
import errno
import os


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
