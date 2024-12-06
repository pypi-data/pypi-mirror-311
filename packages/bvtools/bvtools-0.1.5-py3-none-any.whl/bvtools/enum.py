import enum
import inspect
import types
import typing
from enum import StrEnum, auto
from functools import wraps
from typing import Callable, Union


class Size(StrEnum):
    SMALL = enum.auto()
    BIG = enum.auto()


def func(arg: str | Size):
    print(arg)

def has_union_with_strenum(sig) -> None | tuple[str, enum.EnumType]:
    """
    Function to check if any parameter has a Union type with a StrEnum subclass.
    Returns the first parameter name and class that matches
    """
    for param_name, param in sig.parameters.items():
        annotation = param.annotation
        if typing.get_origin(annotation) is types.UnionType:
            for arg in typing.get_args(annotation):
                if isinstance(arg, type) and issubclass(arg, StrEnum):
                    return param_name, arg
    return None

def str_to_enum(
    ignore_case: bool = True
):
    """
    Automatically converts string arguments to StrEnum. Throws a ValueError if the given string
    if not a member of the Enum class.

    :param directory: Directory where cached files are stored.
    :returns: A decorator that caches function results.
    """

    def decorator(func: Callable):
        @wraps(func)
        sig = inspect.signature(func)
        def inner(*args, **kwargs):

            bind = sig.bind_partial(*args, **kwargs)
            new_kwargs = {}
            for arg, val in bind.arguments.items():
                if sig.parameters[arg].kind == inspect.Parameter.VAR_KEYWORD:
                    # Parameters passed as '**kwargs' are passed through
                    new_kwargs = {**new_kwargs, **val}
                else:
                    annotation = sig.parameters[arg].annotation
                    if (
                    ):
                        try:
                            val = Path(val)
                        except TypeError:
                            pass
                    elif annot in (
                        List[Path],
                        List[PathOrStr],
                        Iterable[Path],
                        Iterable[PathOrStr],
                    ):
                        new_val = []
                        for p in val:
                            try:
                                np = Path(p)
                            except TypeError:
                                np = p
                            new_val.append(np)
                        val = new_val
                    new_kwargs[arg] = val
            # TODO: if we return a function with new type annotations;
            # Path instead of PathOrStr, then mypy won't complain.
            return func(**new_kwargs)

        return inner
    return decorator
