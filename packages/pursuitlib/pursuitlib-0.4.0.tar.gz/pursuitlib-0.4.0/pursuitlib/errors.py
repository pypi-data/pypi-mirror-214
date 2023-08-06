from typing import Callable


def not_implemented(obj: object, method: Callable) -> NotImplementedError:
    return NotImplementedError(f"Method '{method.__name__}' is not implemented for '{type(obj).__name__}'")
