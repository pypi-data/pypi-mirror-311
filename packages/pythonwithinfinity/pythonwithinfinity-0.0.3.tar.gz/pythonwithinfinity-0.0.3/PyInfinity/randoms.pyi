from typing import (overload as __overload__, 
                    Union as __U__, 
                    List as __L__, 
                    Any as __A__, 
                    Tuple as __T__)

@__overload__
def rand(start: int, end: int,
         /, *,
         dtype: object=int,
         randnumber: bool=False) -> int: ...

@__overload__
def rand(start: float, end: float,
         /, *,
         dtype: object=float,
         randnumber: bool=False) -> float: ...

@__overload__
def rand(start: float, end: int,
         /, *,
         dtype: tuple[object, object]=[float, int],
         randnumber: bool=False) -> __U__[int, float]: ...

@__overload__
def rand(start: int, end: float,
         /, *,
         dtype: tuple[object, object]=[int, float],
         randnumber: bool=False) -> __U__[int, float]: ...

def choiseObjectInList(list: __L__[__A__]) -> __A__: ...
def choiseObjectInTuple(tuple: __T__[__A__, ...]) -> __A__: ...
def randList(list: __L__[__A__]) -> __A__: ...
def random() -> __U__[int, float]: ...

__all__: __L__[str]