import sys

_SYS_ARGV_ITER = iter(sys.argv[1:])

def a():

    next(_SYS_ARGV_ITER)

def is_this_windows():

    return sys.platform == 'win32'
