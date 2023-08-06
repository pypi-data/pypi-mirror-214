import os
import dotenv as __dotenv
from typing import TypeVar, Callable

T = TypeVar("T")


def find_env_path(root: str = ""):
    if not root:
        root = __file__
    if not os.path.isdir(root):
        root = os.path.dirname(root)
    result = None
    while len(root) > 1:
        result = os.path.join(root, ".env")
        if os.path.exists(result):
            break
        root = os.path.dirname(root)
    if result is None:
        raise FileExistsError("Unable to locate env path")
    return os.path.abspath(result)


def osenv(root: str = "",schema:Callable[[dict],T]=dict):
    env_path = find_env_path(root=root)
    result = __dotenv.dotenv_values(env_path)
    return schema(result)
