import os
import platform
import re
from enum import Enum
from datetime import datetime, timedelta
try:
    from typing import Dict, Literal
except ImportError:
    from typing import Dict
    from typing_extensions import Literal

VIDEO_ID_REGEX = re.compile(
    r"(.+?)(\/)(watch\x3Fv=)?(embed\/watch\x3Ffeature\=player_embedded\x26v=)?([a-zA-Z0-9_-]{11})+"
)
ALL_CATEGORIES = [
    "sponsor",
    "selfpromo",
    "interaction",
    "intro",
    "outro",
    "preview",
    "music_offtopic",
    "poi_highlight",
    "filler",
]
Category = Literal[
    "sponsor",
    "selfpromo",
    "interaction",
    "intro",
    "outro",
    "preview",
    "music_offtopic",
    "poi_highlight",
    "filler",
]
__version__ = "0.2.1"

class SortType(Enum):
    """0 for by minutes saved, 1 for by view count, 2 for by total submissions

    See Also
    --------
    sponsorblock.client.Client.get_top_users : Should be used with the SortType
    """

    MINUTES_SAVED = 0
    VIEW_COUNT = 1
    TOTAL_SUBMISSIONS = 2


def set_env_var(key: str, value: str):
    """Sets an environment variable to the given value.

    Parameters
    ----------
    key : str
        The key of the environment variable to set.
    value : str
        The value of the environment variable to set.

    Warning
    -------
    Most of the time this shouldn't be used manually, but it's here in case you need to set the SPONSORBLOCK_USER_ID environment variable.
    """
    print("Setting SPONSORBLOCK_USER_ID environment variable")
    operating_system = platform.system()
    if operating_system == "Windows":
        os.system(f'setx {key} "{value}" ')
    elif operating_system in ("Darwin", "Linux"):
        os.system(f'export {key}="{value}" ')


def cache(**kwargs):
    """
    Custom cache implementation taken from https://stackoverflow.com/a/67555155/13123877.

    Parameters
    ----------
    ttl : timedelta, optional
        The time to live for the cache. Defaults to max time supported by the platform.
    max_entries : int
        The maximum number of entries to store in the cache..
    """

    def decorator(function):
        # static function variable for cache, lazy initialization
        try:
            function.cache
        except AttributeError:
            function.cache = {}

        def wrapper(*args):
            # if nothing valid in cache, insert something
            if (
                not args in function.cache
                or datetime.now() > function.cache[args]["expiry"]
            ):
                if "max_entries" in kwargs:
                    max_entries = kwargs["max_entries"]
                    if max_entries is not None and len(function.cache) >= max_entries:
                        now = datetime.now()
                        function.cache = {
                            key: function.cache[key]
                            for key in function.cache.keys()
                            if function.cache[key]["expiry"] > now
                        }
                        # if nothing is expired that is deletable, delete the first
                        if len(function.cache) >= max_entries:
                            del function.cache[next(iter(function.cache))]
                function.cache[args] = {
                    "result": function(*args),
                    "expiry": datetime.max
                    if "ttl" not in kwargs
                    else datetime.now() + timedelta(seconds=kwargs["ttl"]),
                }

            # answer from cache
            return function.cache[args]["result"]

        return wrapper

    return decorator


class Singleton(type):
    _instances: Dict['Singleton', 'Singleton'] = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
