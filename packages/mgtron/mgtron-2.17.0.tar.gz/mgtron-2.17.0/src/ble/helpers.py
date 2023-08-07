"""Make remote API calls to find Bluetooth device names."""

import json

import requests
from threading import Thread

from decouple import config
import logging
from colorama import Fore as F


loggei = logging.getLogger(name=__name__)

R = F.RESET


def get_device_name(mac: str) -> dict:
    """Make the remote API call to get the device name."""
    API_KEY: str = config("API_KEY")

    url = "https://mac-address-lookup1.p.rapidapi.com/static_rapid/mac_lookup/"

    print(f"mac: {mac}")
    querystring = {"query": mac}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "mac-address-lookup1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(json.dumps(response.json(), indent=4))

    return response.json()


class ThreadWithReturnValue(Thread):
    """Create a thread that returns a value."""

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        """Initialize the thread."""
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        """Run the thread."""
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def get_id(self):
        """Return the id of the thread."""
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in Thread._active.items():
            if thread is self:
                return id

    def join(self, *args):
        """Join the thread."""
        Thread.join(self, *args)
        return self._return
