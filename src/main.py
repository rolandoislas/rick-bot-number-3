import os

import sys

import time

from bot import Bot
from logger import Logger
import constants


def main():
    if "-v" in sys.argv:
        Logger.set_level(Logger.VERBOSE)
    else:
        Logger.set_level(Logger.FINER)
    Logger.info("%s version %s", constants.NAME, constants.VERSION)
    reddit_username = os.environ.get("REDDIT_USERNAME")
    reddit_password = os.environ.get("REDDIT_PASSWORD")
    reddit_client_id = os.environ.get("REDDIT_CLIENT_ID")
    reddit_secret = os.environ.get("REDDIT_SECRET")
    run_live = os.environ.get("RUN_LIVE")
    interval = os.environ.get("INTERVAL")
    if not reddit_username:
        Logger.throw("Missing REDDIT_USERNAME environment variable.")
    if not reddit_password:
        Logger.throw("Missing REDDIT_PASSWED environment variable.")
    if not reddit_client_id:
        Logger.throw("Missing REDDIT_CLIENT_ID environment variable.")
    if not reddit_secret:
        Logger.throw("Missing REDDIT_SECRET environment variable.")
    if not interval:
        Logger.throw("Missing INTERVAL environment variable.")
    interval_error = "INTERVAL must be a positive integer."
    try:
        interval = int(interval)
    except ValueError:
        Logger.throw(interval_error)
    if interval <= 0:
        Logger.throw(interval_error)
    if not run_live:
        Logger.warn("Missing RUN_LIVE environment variable. Defaulting to false.")
    run_live = run_live == "true"
    try:
        tries = 0
        max_tries = 3
        while not Bot(reddit_password, reddit_username, reddit_client_id, reddit_secret, run_live, interval).run() \
                and tries < max_tries:
            Logger.warn("Failed to run bot. Trying again after a delay.")
            tries += 1
            time.sleep(60 * (tries + 1))  # sleep on failure
        if tries >= max_tries:
            Logger.throw("Giving up after failing %d times." % max_tries)
    except KeyboardInterrupt:
        pass
    Logger.info("Exiting")


if __name__ == '__main__':
    main()
