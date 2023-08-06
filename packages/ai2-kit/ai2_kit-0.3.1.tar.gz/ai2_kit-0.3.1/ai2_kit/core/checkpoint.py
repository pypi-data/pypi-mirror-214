from typing import TypeVar, Union, Callable, NamedTuple, Optional
from threading import Lock
import functools
import cloudpickle
import os
import types

from .future import IFuture

_lock = Lock()
_checkpoint_file: Optional[str] = None
_checkpoint_data: Optional[dict] = None


class FnInfo(NamedTuple):
    fn_name: str
    args: tuple
    kwargs: dict


KeyFn = Callable[[FnInfo], str]

EMPTY = object()


def set_checkpoint_file(path: str):
    global _checkpoint_file
    if _checkpoint_file is not None:
        raise RuntimeError(
            "checkpoint path has been set to {}".format(_checkpoint_file))
    _checkpoint_file = path


def checkpoint(key_fn: Union[str, KeyFn], disable = False):
    """
    Checkpoint for function.

    Note: This checkpoint implementation doesn't support multiprocess.
    To support multiple process we need to have a dedicated background process to read/write checkpoint,
    which will require message queue (e.g. nanomsg or nng) to implement it.

    Example:

    >>> set_checkpoint_file('/tmp/test.ckpt')
    >>> task_fn = lambda a, b: a + b
    >>> checkpoint('task_1+2')(task_fn)(1, 2)
    """

    T = TypeVar('T', bound=Callable)
    def _checkpoint(fn: T) -> T:

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if isinstance(key_fn, str):
                key = key_fn
            else:
                fn_info = FnInfo(
                    fn_name=fn.__name__,
                    args=args,
                    kwargs=kwargs,
                )
                key = key_fn(fn_info)

            if disable or _checkpoint_file is None:
                return fn(*args, **kwargs)

            ret = _get_checkpoint(key)
            if ret is not EMPTY:
                return ret

            ret = fn(*args, **kwargs)

            if isinstance(ret, IFuture):
                result_fn = ret.result
                def _wrap_fn(self, timeout=None):
                    _ret = result_fn(timeout)
                    _set_checkpoint(key, ret)
                    return _ret
                ret.result = types.MethodType(_wrap_fn, ret)
            else:
                _set_checkpoint(key, ret)

            return ret

        return wrapper # type: ignore

    return _checkpoint


def _load_checkpoint():
    global _checkpoint_data
    if _checkpoint_data is not None:
        return
    assert _checkpoint_file is not None, '_checkpoint_path should not be None!'
    if os.path.exists(_checkpoint_file):
        with open(_checkpoint_file, 'rb') as f:
            _checkpoint_data = cloudpickle.load(f)
    else:
        _checkpoint_data = dict()


def _dump_checkpoint():
    assert _checkpoint_data is not None, '_checkpoint_data should not be None!'
    with open(_checkpoint_file, 'wb') as f:  # type: ignore
        cloudpickle.dump(_checkpoint_data, f)


def _get_checkpoint(key: str):
    try:
        with _lock:
            _load_checkpoint()
            return _checkpoint_data.get(key, EMPTY)  # type: ignore
    except Exception as e:
        print("Fail to get checkpoint", e)
        return EMPTY


def _set_checkpoint(key: str, value):
    try:
        with _lock:
            _checkpoint_data[key] = value  # type: ignore
            _dump_checkpoint()
    except Exception as e:
        print('Fail to set checkpoint', e)
