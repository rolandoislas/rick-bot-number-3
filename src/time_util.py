from datetime import datetime
from pytz import timezone


class Timeval:
    second = 1
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    month = 31 * day
    year = 365 * day

    def __init__(self):
        pass

    def dst(self, dt):
        return datetime.timedelta(0)


class TimeUtil:
    diff_season_two_to_three = None
    diff_now_to_season_three = None

    def __init__(self):
        central = timezone("US/Central")
        # Season 2
        season_two_production_date = datetime(2014, 1, 1, tzinfo=central)  # Some time in January
        season_two_premier_date = datetime(2015, 7, 26, 21, 30, tzinfo=central)  # Exact *date* assuming 9:30pm
        season_two_production_time = season_two_premier_date - season_two_production_date
        # Season 3
        season_three_production_date = datetime(2015, 8, 1, tzinfo=central)  # Some time is August
        season_three_premier_date_fool = datetime(2017, 4, 1, 17, 1, tzinfo=central)  # Exact *date* 5:01pm (tweet)
        # TODO update if actual date is released
        season_three_premier_date = datetime(2017, 8, 1, 21, 30, tzinfo=central)  # Summer 2017 assuming 9:30pm
        season_three_production_time = season_three_premier_date_fool - season_three_production_date
        # diff
        TimeUtil.diff_season_two_to_three = self.get_diff(season_two_production_time, season_three_production_time)
        TimeUtil.diff_now_to_season_three = self.get_diff(datetime.now(central), season_three_premier_date)

    @classmethod
    def get_season_3_production_time_reply(cls):
        """
        Returns a markdown message containing the difference between season 2 and 3's prediction times
        :return: string
        """
        return "Season three production was about%s behind season 2." \
               % cls.get_time_string(cls.diff_season_two_to_three)

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

    @staticmethod
    def get_diff(time_delta_1, time_delta_2):
        """
        Finds the time between two time deltas.
        :param time_delta_1: time delta
        :param time_delta_2: time delta
        :return: TimeVal with populated years, months, days, hours, minutes, seconds
        """
        time_val = Timeval()
        diff = time_delta_1 - time_delta_2
        total_seconds = abs(diff.total_seconds())
        time_val.years = int(total_seconds // Timeval.year)
        total_seconds %= Timeval.year
        time_val.months = int(total_seconds // Timeval.month)
        total_seconds %= Timeval.month
        time_val.days = int(total_seconds // Timeval.day)
        total_seconds %= Timeval.day
        time_val.hours = int(total_seconds // Timeval.hour)
        total_seconds %= Timeval.hour
        time_val.minutes = int(total_seconds // Timeval.minute)
        total_seconds %= Timeval.minute
        time_val.seconds = int(total_seconds)
        return time_val

    @classmethod
    def get_time_string(cls, diff):
        """
        Reruns a string in format ( %d years, %d months, %d days, %d hours, %d minutes, %d seconds). 
        Note the preceding space.
        :param diff: TimeVal with years, months, etc set. See get_diff().
        :return: string
        """
        years = " %d year%s," % (diff.years, cls.get_plural(diff.years)) if diff.years > 0 else ""
        months = " %d month%s," % (diff.months, cls.get_plural(diff.months)) if diff.months > 0 else ""
        days = " %d day%s," % (diff.days, cls.get_plural(diff.days)) if diff.days > 0 else ""
        hours = " %d hour%s," % (diff.hours, cls.get_plural(diff.hours)) if diff.hours > 0 else ""
        minutes = " %d minute%s," % (diff.minutes, cls.get_plural(diff.minutes)) if diff.minutes > 0 else ""
        seconds = " %d second%s" % (diff.seconds, cls.get_plural(diff.seconds))
        return "%s%s%s%s%s%s" % (years, months, days, hours, minutes, seconds)

    @classmethod
    def get_season_3_expected_date_reply(cls):
        """
        Returns a markdown message with the time until now and the expected release of season 3.
        :return: string
        """
        return "Season three is about%s away. `Summer (assuming August) 2017`" \
               % cls.get_time_string(cls.diff_now_to_season_three)


TimeUtil()

# Dev
if __name__ == '__main__':
    import time

    while True:
        TimeUtil()
        print TimeUtil.get_season_3_expected_date_reply()
        print TimeUtil.get_season_3_production_time_reply()
        time.sleep(1)
