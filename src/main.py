import os

import sys

import time

from bot import Bot
from logger import Logger
import constants


def main():
    # Verbose logging
    if "-v" in sys.argv:
        Logger.set_level(Logger.VERBOSE)
    else:
        Logger.set_level(Logger.FINER)
    # Reply print test
    if len(sys.argv) >= 3 and sys.argv[1] == "test" and sys.argv[2] == "reply":
        Logger.set_level(Logger.VERBOSE)
        try:
            Bot("", "", "", "", "", "", "", "", True, "", "").reply(None)
        except Exception, e:
            Logger.debug(e)
        return
    # Check environment variables
    Logger.info("%s version %s", constants.NAME, constants.VERSION)
    reddit_username = os.environ.get("REDDIT_USERNAME")
    reddit_password = os.environ.get("REDDIT_PASSWORD")
    reddit_client_id = os.environ.get("REDDIT_CLIENT_ID")
    reddit_secret = os.environ.get("REDDIT_SECRET")
    run_live = os.environ.get("RUN_LIVE")
    interval = os.environ.get("INTERVAL")
    comments_root_only = os.environ.get("COMMENTS_ROOT_ONLY") or "false"
    comments_enabled = os.environ.get("COMMENTS_ENABLED") or "true"
    comment_prefix = os.environ.get("COMMENT_PREFIX") or "true"
    post_reply_enabled = os.environ.get("POST_REPLY_ENABLED") or "true"
    post_reply_question = os.environ.get("POST_REPLY_QUESTION") or "true"
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
    if not run_live:
        Logger.warn("Missing RUN_LIVE environment variable. Defaulting to false.")
    if not constants.SEASON_3_URL:
        Logger.info("No SEASON_THREE_URL found. Using countdown as message.")
    # Parse environment variables
    interval_error = "INTERVAL must be a positive integer."
    try:
        interval = int(interval)
    except ValueError:
        Logger.throw(interval_error)
    if interval <= 0:
        Logger.throw(interval_error)
    run_live = run_live.upper() == "TRUE"
    comments_enabled = comments_enabled.upper() == "TRUE"
    comments_root_only = comments_root_only.upper() == "TRUE"
    comment_prefix = comment_prefix.upper() == "TRUE"
    post_reply_enabled = post_reply_enabled.upper() == "TRUE"
    post_reply_question = post_reply_question.upper() == "TRUE"
    # Info booleans
    if not comments_enabled:
        Logger.info("Comments disabled.")
    if comments_root_only and comments_enabled:
        Logger.info("Only root comments will get replies.")
    if comment_prefix and comments_enabled:
        Logger.info("Using comment prefix: %s", constants.COMMENT_PREFIX)
    if not post_reply_enabled:
        Logger.info("Post replied disabled.")
    if post_reply_question and post_reply_enabled:
        Logger.info("Only replying to question posts.")
    # Run
    try:
        tries = 0
        max_tries = 3
        while not Bot(reddit_password, reddit_username, reddit_client_id, reddit_secret, run_live, interval,
                      comments_enabled, comments_root_only, comment_prefix, post_reply_enabled, post_reply_question)\
                .run() \
                and tries < max_tries:
            tries += 1
            delay = 60 * tries
            Logger.warn("Failed to run bot. Trying again after a %d second delay.", delay)
            time.sleep(delay)  # sleep on failure
        if tries >= max_tries:
            Logger.throw("Giving up after failing %d times." % max_tries)
    except KeyboardInterrupt:
        pass
    Logger.info("Exiting")


if __name__ == '__main__':
    main()
