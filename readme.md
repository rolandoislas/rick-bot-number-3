# rick-bot-number-3

Where is Rick and Morty season 3?

[/u/rick_bot_number_3] does not know but it does like pointing out the production
 time differences between season 2 and 3 on [/r/RickAndMorty].

For info how the bot determines the time difference see the post [Season Three is not Late].

Like the bot? Toss me a Schmeckle (or part of one): `1C55DzMDvTMHQ2o3HUQtHex5EoPKi1Et17`.

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

- REDDIT_USERNAME
- REDDIT_PASSWORD
- REDDIT_CLIENT_ID
- REDDIT_SECRET

Self explanatory.

### RUN_LIVE

boolean (lowercase) - Determines if the bot should run in live mode. If it is 
 not live it will error (catch and log) on post. It is useful for testing.

### INTERVAL

The bot does not run in a loop, it uses a time interval to check for posts and
 comments. This should be set to the amount of time between runs of the script.
 It can be set to longer with no ill effect, but it will miss item if it is lower
 than the actual interval.

### SEASON_THREE_URL

optional URL for season 3 release 

This is the URL that will be used for the random season 3 messages.
 It is a string instead of the a boolean because the URL may vary.
 If it is not present or empty, the season three URL message will not display.
 If it is present, the countdown will not display.



[/u/rick_bot_number_3]: https://www.reddit.com/user/rick_bot_number_3/
[/r/RickAndMorty]: https://www.reddit.com/r/rickandmorty/
[Season Three is not Late]: https://www.reddit.com/r/rickandmorty/comments/62clpj/season_three_is_not_late/
[issue tracker]: https://github.com/rolandoislas/rick-bot-number-3
