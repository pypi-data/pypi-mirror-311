from loguru import logger as LOGGER
from typing import Dict
import requests
from threading import Lock

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


def call_api(url: str, is_post: bool = False) -> Dict:
    LOGGER.debug(f'Gateway call: {url}')
    if is_post:
        resp = requests.post(url)
    else:
        resp = requests.get(url)
    
    if resp.status_code < 400:
        try:
            resp_json = resp.json()
        except requests.exceptions.JSONDecodeError():
            resp_json = {}
    else:
        resp_json = {}

    if resp.status_code >= 400 and resp_json.get('success',None) is None:
        resp_json['success'] = False
        resp_json['command'] = url
        resp_json['msg'] = resp.reason
    
    log_lvl = "DEBUG" if resp_json['success'] else "WARNING"
    LOGGER.log(log_lvl, f'_call_api("{url}",is_post={is_post})')
    LOGGER.log(log_lvl, f' {resp_json["command"]} | {resp_json["msg"]}')

    resp.raise_for_status()
    
    return resp_json

def is_gateway_available(base_url: str) -> bool:
    try:
        url = f'{base_url}/ping'
        call_api(url)
    except Exception as ex:
        msg = f'Unable to connect [{url}].\n{ex}.\nIs the site down?'
        LOGGER.error(msg)
        return False
    
    return True