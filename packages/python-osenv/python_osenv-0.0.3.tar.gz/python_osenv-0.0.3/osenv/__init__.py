import os
import dotenv as __dotenv
from typing import TypeVar, Callable, Type, Union

T = TypeVar("T")


def __find_env(root: str = "", env_name: str = ".env"):
    if not root:
        root = __file__
    if not os.path.isdir(root):
        root = os.path.dirname(root)
    result = None
    while len(root) > 1:
        result = os.path.join(root, env_name)
        if os.path.exists(result):
            break
        root = os.path.dirname(root)
    if result is None:
        raise FileExistsError("Unable to locate env path")
    return os.path.abspath(result)


def osenv(root: str = "", schema: Union[Callable[[dict], T], Type] = dict):
    env_path = __find_env(root=root)
    result = __dotenv.dotenv_values(env_path)
    is_complete = False
    if isinstance(schema, Type) and hasattr(schema, "parse_obj"):
        try:
            result = schema.parse_obj(result)
            is_complete = True
        except BaseException:
            pass
    if not is_complete:
        result = schema(result)
    return result
