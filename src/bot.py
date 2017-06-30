import os
import random
import time

import datetime
from praw import Reddit
from praw.exceptions import APIException, ClientException
from prawcore import ServerError

import constants
from logger import Logger
from time_util import TimeUtil


class Bot:
    def __init__(self, reddit_password, reddit_username, reddit_client_id, reddit_secret, run_live, interval, comments,
                 comments_root_only, comment_prefix, post_reply_enabled, post_reply_question):
        """
        Initialize the bot
        :param reddit_password: bot password
        :param reddit_username: bot username
        :param reddit_client_id: Reddit APT app client id
        :param reddit_secret: Reddit API app secret
        :param run_live: boolean - should run in live mode (send replies)
        :param interval: Interval the script is expected to be ran at. This determines what posts and comments are "new"
        :param comments: boolean - reply to comments
        :param comments_root_only: boolean - reply only to root comments
        :param post_reply_enabled: boolean - enable replies to posts
        :param post_reply_question: boolean - reply only to posts that ask a question
        to the bot.
        """
        self.reddit_password = reddit_password
        self.reddit_username = reddit_username
        self.reddit_client_id = reddit_client_id
        self.reddit_secret = reddit_secret
        self.run_live = run_live
        self.interval = interval
        self.comments_enabled = comments
        self.comments_root_only = comments_root_only
        self.comment_prefix = comment_prefix
        self.post_reply_enabled = post_reply_enabled
        self.post_reply_question = post_reply_question
        # Init
        self.reddit = None
        self.trigger_phrases = []
        pwd = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(pwd, "../resources/trigger_phrases.txt")) as txt:
            self.trigger_phrases = txt.read().splitlines()
        self.footer_phrases = []
        with open(os.path.join(pwd, "../resources/footer_phrases.txt")) as txt:
            self.footer_phrases = txt.read().splitlines()
        self.countdown_end_phrases = []
        with open(os.path.join(pwd, "../resources/countdown_end_phrases.txt")) as txt:
            self.countdown_end_phrases = txt.read().splitlines()
        self.question_phrases = []
        with open(os.path.join(pwd, "../resources/question_phrases.txt")) as txt:
            self.question_phrases = txt.read().splitlines()

    def run(self):
        """
        Entry point for the bot
        :return: boolean - success status
        """
        Logger.info("Staring bot")
        try:
            self.login()
            self.check_rate_limit(3)
            subreddit = self.reddit.subreddit("rickandmorty")
            if self.post_reply_enabled:
                self.reply_to_new_posts(subreddit)
            if self.comments_enabled:
                self.reply_to_new_comments(subreddit)
        except (APIException, ClientException, ServerError), e:
            Logger.exception(e)
            return False
        return True

    def login(self):
        """
        Login with bot credentials
        :return: None
        """
        self.reddit = Reddit(client_id=self.reddit_client_id,
                             client_secret=self.reddit_secret,
                             user_agent=constants.USERAGENT,
                             username=self.reddit_username,
                             password=self.reddit_password)
        self.reddit.read_only = not self.run_live
        if self.reddit.read_only:
            Logger.info("Bot running in read only mode.")
        else:
            Logger.info("Bot is running in live post mode.")

    def reply(self, post):
        """
        Replies to a post (or comment). Does not check for any prerequisites.
        :param post: PRAW submission or comment
        :return: None
        """
        season_three = self.countdown_end_phrases[random.randint(0, len(self.countdown_end_phrases) - 1)]
        season_three %= constants.SEASON_3_URL
        info_message = "I am a bot. I reply to posts and comments related to season 3."
        if self.comment_prefix:
            info_message += " Use **%sseason 3** to summon me in the comments." % constants.COMMENT_PREFIX
        footer = "%s v%s | [%s](%s)" % (constants.NAME,
                                        constants.VERSION,
                                        self.footer_phrases[random.randint(0, len(self.footer_phrases) - 1)],
                                        constants.REPO)
        # TODO Don't handle the season three release message with environment variable logic.
        # Have the message update based on the time.
        message = "%s\n\n%s\n\n---\n\n%s\n\n%s" % (season_three if constants.SEASON_3_URL else "",
                                                   TimeUtil.get_season_3_expected_date_reply()
                                                   if not constants.SEASON_3_URL else "",
                                                   info_message,
                                                   footer)
        Logger.verbose("Message:\n%s", message)
        self.check_rate_limit()
        try:
            post.reply(message)
        except APIException:
            self.check_rate_limit()
            post.reply(message)  # Don't recurse. One retry

    def reply_to_new_comments(self, subreddit):
        """
        Replies to new comments in the subreddit if they contain a matching phrase.
        :param subreddit: PRAW subreddit
        :return: None
        """
        comments = self.get_new_comments(subreddit)
        comment_number = 0
        comments_with_reply = []  # IDs
        for comment in comments:
            self.check_rate_limit()
            if comment.author == self.reddit_username and not comment.is_root:
                parent = comment.parent()
                parent.refresh()
                comments_with_reply.append(parent.id)
        for comment in comments:
            if comment.author == self.reddit_username:
                continue
            Logger.debug("===== Checking comment %d =====", comment_number)
            Logger.extra("Comment truncated text: %s", comment.body[:100].replace("\n", ""))
            comment_number += 1
            is_season_three_comment = self.contains_valid_phrase(comment.body, True)
            Logger.debug("Season 3 comment: %s", is_season_three_comment)
            Logger.debug("Is root: %s", comment.is_root)
            if not is_season_three_comment:
                continue
            if comment.id in comments_with_reply:
                Logger.debug("Already replied to this comment")
                continue
            if self.comments_root_only and not comment.is_root:
                Logger.debug("Comment is not root and only root comment replies are enabled.")
                continue
            Logger.verbose("Comment full text: %s", comment.body)
            Logger.info("Replying to comment")
            try:
                self.reply(comment)
            except APIException, e:
                Logger.exception(e)

    def get_posts(self, subreddit, interval=None):
        """
        Get posts from time (NOW - INTERVAL) to (NOW).
        :param subreddit: PRAW subreddit
        :param interval: int - interval override in minutes
        :return: PRAW submissions
        """
        interval = interval if interval else self.interval
        end = int(time.time())  # now
        start = end - interval * 60  # past time - specified by interval
        return subreddit.submissions(start, end)

    def check_rate_limit(self, remaining=1):
        """
        Checks if the rate limit allows for an amount of requests. If not, sleep until reset.
        :param remaining: int - amount of request that should be available
        :return: None
        """
        limits = self.reddit.auth.limits
        if limits["remaining"] < remaining:
            self.sleep_until(limits["reset_timestamp"])

    @staticmethod
    def sleep_until(timestamp):
        """
        Sleeps until a given timestamp
        May be late by up to one seconds
        :param timestamp: UNIX/time.time()
        :return: None
        """
        while time.time() < timestamp:
            time.sleep(1)

    def contains_valid_phrase(self, text, is_comment=False):
        """
        Checks if the text has a valid phrase
        :param is_comment: boolean checks and adds prefix to comments if enabled
        :param text: string
        :return: boolean
        """
        text_up = text.upper()
        phrases = list(self.trigger_phrases)
        if is_comment and self.comment_prefix:
            for phrase_num in range(0, len(phrases)):
                phrases[phrase_num] = constants.COMMENT_PREFIX + phrases[phrase_num]
        if any(phrase in text_up for phrase in phrases):
            return True
        return False

    def get_comments_on_post(self, post):
        """
        Gets all the comments for on a post
        :param post: PRAW submission
        :return: List of PRAW comments
        """
        self.check_rate_limit()  # PRAW comment retrial seems to implement rate limit handling itself
        post.comment_sort = "new"
        post.comments.replace_more(limit=0)
        return post.comments.list()

    def has_replied_to_post(self, comments):
        """
        Checks top-level comments for a comment by the bot
        :param comments: PRAW list of comments
        :return: boolean
        """
        Logger.debug("Checking top level comments for a previous reply")
        has_commented = False
        for comment in comments:
            Logger.extra("Comment is root: %s", comment.is_root)
            if comment.is_root and ((not comment.author) or comment.author.name == self.reddit_username):
                has_commented = True
                break
        return has_commented

    def reply_to_new_posts(self, subreddit):
        """
        Checks new posts and replies to them if they have a matching phrase and have not been previously replied to
        by the bot.
        :param subreddit: PRAW subreddit
        :return: None
        """
        posts = self.get_posts(subreddit)
        post_num = 0
        Logger.info("Getting posts")
        for post in posts:
            Logger.debug("===== Checking post %d =====", post_num)
            post_num += 1
            Logger.extra("Post Title: %s", post.title)
            Logger.debug("Link: %s", post.shortlink)
            Logger.debug("Created: %s", datetime.datetime.fromtimestamp(post.created))
            # Check valid title
            self_text_is_season_3 = self.contains_valid_phrase(post.selftext, True)  # Parse self-text as a comment
            is_season_three_post = self.contains_valid_phrase(post.title) or self_text_is_season_3
            Logger.debug("Season 3 post: %s", is_season_three_post)
            if self.post_reply_question:
                # Checking the selftext might be to broad
                is_question = self.is_question(post.title)
                Logger.debug("Contains question: %s", is_question)
                if not (is_question or self_text_is_season_3):
                    continue
            # Ignore if not season 3 post
            if not is_season_three_post:
                continue
            # Check comments
            Logger.debug("Getting comments for post")
            comments = self.get_comments_on_post(post)
            if self.has_replied_to_post(comments):
                Logger.debug("Already replied to this post")
                continue
            Logger.info("Commenting on post")
            try:
                self.reply(post)
            except APIException, e:
                Logger.exception(e)

    def get_new_comments(self, subreddit):
        """
        Gets comments from the subreddit from time (NOW - INTERVAL) to (NOW)
        :param subreddit: PRAW subreddit
        :return: array of PRAW comments
        """
        start_time = int(time.time()) - self.interval * 60
        subreddit.comment_sort = "new"
        comments = []
        Logger.info("Getting comments")
        for comment in subreddit.comments(limit=1000000):
            if comment.created_utc < start_time:
                Logger.debug("Found %d comments", len(comments))
                break
            comments.append(comment)
            self.check_rate_limit()
        return comments

    def is_question(self, text):
        """
        Checks if a string contains phrases that might make it a season time question.
        :param text: 
        :return: boolean
        """
        text_up = text.upper()
        if any(text_up.startswith(phrase) for phrase in self.question_phrases):
            return True
        return False


if __name__ == '__main__':
    bot = Bot("", "", "", "", "", "", "", "", "", "", True)
    print bot.is_question("Blah blah season 3?")
