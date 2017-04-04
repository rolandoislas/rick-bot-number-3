# rick-bot-number-3

Where is Rick and Morty season 3?

[/u/rick_bot_number_3] does not know but it does like counting down the time until season 3 on [/r/RickAndMorty].
 The date will be updated if an official one is given before the release.

The initial intention of the bot was to point out the time difference between the off-season 1-2 and 2-3.

Like the bot? Toss me a Schmeckle: `1C55DzMDvTMHQ2o3HUQtHex5EoPKi1Et17`.

# Suggestions

Have a suggestion?

> Your opinion means very little to me.
>
> \- Rick Sanchez

Fortunately, I am not Rick. Submit ideas and bug reports to the [issue tracker].

# Contributing

- The Python dependencies are lazily put into `requirements.txt`.
- The entry point is `src/main.py`.
- Follow PEP-8 with 120 characters per line instead of 80.
- Do not be a Tammy.

## Environment Variables

### REDDIT_*

strings

- REDDIT_USERNAME
- REDDIT_PASSWORD
- REDDIT_CLIENT_ID
- REDDIT_SECRET

Self explanatory.

### RUN_LIVE

boolean

Determines if the bot should run in live mode. If it is 
 not live it will error (catch and log) on post. It is useful for testing.

### INTERVAL

integer

The bot does not run in a loop, it uses a time interval to check for posts and
 comments. This should be set to the amount of time between runs of the script.
 It can be set to longer with no ill effect, but it will miss item if it is lower
 than the actual interval.

### SEASON_THREE_URL

string

optional URL for season 3 release 

This is the URL that will be used for the random season 3 messages.
 It is a string instead of the a boolean because the URL may vary.
 If it is not present or empty, the season three URL message will not display.
 If it is present, the countdown will not display.
 
### COMMENTS_ROOT_ONLY

boolean - default false

This sets the bot to only reply root comments.

### COMMENTS_ENABLED

boolean - default true

This determines if the bot should reply to comments.

### COMMENT_PREFIX

boolean - default true

Enables only replying to comments with a prefix followed by a matching phrase (e.g. !season 3).

### POST_REPLY_ENABLED

boolean - default true

This determines if posts should get replies.

### POST_REPLY_QUESTION

boolean - default true

Requires posts to contain additional phrases that make it a question. It is not entirely accurate, but it should reduce
 the overall posting on general season 3 posts.


[/u/rick_bot_number_3]: https://www.reddit.com/user/rick_bot_number_3/
[/r/RickAndMorty]: https://www.reddit.com/r/rickandmorty/
[issue tracker]: https://github.com/rolandoislas/rick-bot-number-3
