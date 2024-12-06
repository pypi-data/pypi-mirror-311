import os.path as os_path
import typing

def is_module(path:str):

    if os_path.isfile(path) and path.endswith('.py'): return True

    if not os_path.isdir(path): return False
    
    init_path = os_path.join(path, '__init__.py')
    return os_path.exists(init_path) and \
           os_path.isfile(init_path)

class Enumerator[T]:

    def __init__(self):

        self._managed:list[T] = list()
    
    def E(self, x):

        """
        DEPRECATED - use as callable
        """
        return self(x)
    
    def __call__(self, x):

        self._managed.append(x)
        return x

    def __iter__(self):

        return self._managed.__iter__()

class ChainedCallables:

    def __init__(self, *ff:typing.Callable):

        self._ff = ff

    def __call__(self, *aa, **kaa):

        for f in self._ff: f(*aa, **kaa)

class Raiser:

    def __init__(self, ex:Exception):       self._ex = ex
    def __call__(self)              : raise self._ex

def selfie  [T](v:T): return v # instead of "self" since the latter is widely used for the instance reference in methods

class _Constant[T]:

    def __init__(self, v:T): self._v = v
    def __call__(self, *aa, **kaa): return self._v

def constant[T](v:T): return _Constant(v).__call__
