import time, functools
from typing import Callable, Type, Iterable 

def retrys(exceptions: Iterable[Type[BaseException]]=(Exception,), tries: int=3, delay: float=0.5, backoff: float=2.0):
    
    
    
    def deco(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return fn(*args, **kwargs)
        return wrapper
    return deco
