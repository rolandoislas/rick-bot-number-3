from datetime import datetime


class Timeval:
    second = 1
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    month = 30.5 * day
    year = 365.25 * day

    def __init__(self):
        pass


class TimeUtil:
    hours = None
    seconds = None
    days = None
    minutes = None
    months = None
    years = None

    def __init__(self):
        epoch = datetime(1970, 1, 1)
        # Season 2
        season_two_production_date = datetime(2014, 1, 1)  # Some time in January
        season_two_premier_date = datetime(2015, 7, 26)
        season_two_production_time = season_two_premier_date - season_two_production_date
        # Season 3
        season_three_production_date = datetime(2015, 8, 1)  # Some time is August
        season_three_premier_date = datetime(2017, 1, 1)  # I hope this will not need to edited (April Fools Release?)
        season_three_production_time = season_three_premier_date - season_three_production_date
        # diff
        diff = season_two_production_time - season_three_production_time
        # diff = datetime(2001, 2, 7, 0) - datetime(2000, 1, 1, 0)  # y m d h m s
        total_seconds = abs(diff.total_seconds())
        TimeUtil.years = int(total_seconds // Timeval.year)
        total_seconds %= Timeval.year
        TimeUtil.months = int(total_seconds // Timeval.month)
        total_seconds %= Timeval.month
        TimeUtil.days = int(total_seconds // Timeval.day)
        total_seconds %= Timeval.day
        TimeUtil.hours = int(total_seconds // Timeval.hour)
        total_seconds %= Timeval.hour
        TimeUtil.minutes = int(total_seconds // Timeval.minute)
        total_seconds %= Timeval.minute
        TimeUtil.seconds = int(total_seconds)

    @classmethod
    def get_reply(cls):
        """
        Returns a markdown message containing the difference between season 2 and 3's prediction times
        :return: string
        """
        years = " %d year%s," % (cls.years, cls.get_plural(cls.years)) if cls.years > 0 else ""
        months = " %d month%s," % (cls.months, cls.get_plural(cls.months)) if cls.months > 0 else ""
        days = " %d day%s," % (cls.days, cls.get_plural(cls.days)) if cls.days > 0 else ""
        hours = " %d hour%s," % (cls.hours, cls.get_plural(cls.hours)) if cls.hours > 0 else ""
        minutes = " %d minute%s," % (cls.minutes, cls.get_plural(cls.minutes)) if cls.minutes > 0 else ""
        seconds = " %d second%s" % (cls.seconds, cls.get_plural(cls.seconds))
        return "Season three production was about%s%s%s%s%s%s behind season 2." \
               % (years, months, days, hours, minutes, seconds)

    @classmethod
    def get_plural(cls, number):
        """
        Returns an "s" if the noun the number would describe should be plural
        :param number: int
        :return: string
        """
        if number == 0 or number < -1 or number > 1:
            return "s"
        else:
            return ""


TimeUtil()

# Dev
if __name__ == '__main__':
    import time

    while True:
        TimeUtil()
        print TimeUtil.get_reply()
        time.sleep(1)
