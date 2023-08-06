import os


def config(key, cast=None, default=None) -> str:
    value = os.environ.get(key, default)
    return cast(value) if cast else value
