from timelab.core.total_time import *


class Base:
    """ Base class for TimeSpan and DateTime. """
    def __init__(self, centuries=0.0, decades=0.0, years=0.0, months=0.0, weeks=0.0, days=0.0, hours=0.0, minutes=0.0, seconds=0.0, milliseconds=0.0):
        self.centuries = centuries
        self.decades = decades
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def __eq__(self, other): return self.as_dictionary() == other.as_dictionary()
    def __gt__(self, other): return self.total_seconds() > other.total_seconds()
    def __lt__(self, other): return self.total_seconds() < other.total_seconds()
    def __ge__(self, other): return self.total_seconds() >= other.total_seconds()
    def __le__(self, other): return self.total_seconds() <= other.total_seconds()

    def total_seconds(self):   return total_seconds(self.centuries, self.decades, self.years, self.months, self.weeks, self.days, self.hours, self.minutes, self.seconds, self.milliseconds)
    def total_minutes(self):   return self.total_seconds() / MINUTES_FACTOR
    def total_hours(self):     return self.total_seconds() / HOURS_FACTOR
    def total_days(self):      return self.total_seconds() / DAYS_FACTOR
    def total_weeks(self):     return self.total_seconds() / WEEKS_FACTOR
    def total_months(self):    return self.total_seconds() / MONTHS_FACTOR
    def total_years(self):     return self.total_seconds() / YEARS_FACTOR
    def total_decades(self):   return self.total_seconds() / DECADES_FACTOR
    def total_centuries(self): return self.total_seconds() / CENTURIES_FACTOR

    def as_dictionary(self, single_letter_unit_names=False) -> dict[str, float]:
        as_dictionary = {
            'centuries': self.centuries,
            'decades': self.decades,
            'years': self.years,
            'months': self.months,
            'weeks': self.weeks,
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds,
            'milliseconds': self.milliseconds
        }

        if single_letter_unit_names:
            for unit, value in as_dictionary.copy().items():
                as_dictionary.pop(unit)

                if unit == 'milliseconds':
                    shortened = 'ms'
                elif unit == 'minutes':
                    shortened = 'min'
                # elif unit == 'months':
                #     shortened = 'mon'
                else:
                    shortened = unit[0]

                as_dictionary[shortened] = value

        return as_dictionary

    def __str__(self):
        args = ''

        for unit, value in self.as_dictionary().items():
            if value == 0:
                continue

            if value == 1:
                unit = unit.removesuffix('s')  # Remove s for singular values

            value = str(value).removesuffix('.0')  # Remove trailing '.0'
            args += f'{value} {unit}, '

        return f'{self.__class__.__name__}({args.removesuffix(', ')})'

    def __repr__(self):
        return self.__str__()

    def normalize(self):
        """
        Normalizes the time format to make it readable.
        For example, If its 'seconds=125', it will be normalized to 'minutes=2, seconds=5'.
        Another example, if its 'hours=2.5', it will be normalized to 'hours=2, minutes=30'.
        """

        normalized = self.__class__()
        remaining_seconds = self.total_seconds()

        if remaining_seconds < 0:
            raise ValueError(f'Cannot normalize negative {self.__class__.__name__.lower()}')

        normalized.centuries, remaining_seconds = divmod(remaining_seconds, CENTURIES_FACTOR)
        normalized.decades, remaining_seconds = divmod(remaining_seconds, DECADES_FACTOR)
        normalized.years, remaining_seconds = divmod(remaining_seconds, YEARS_FACTOR)
        normalized.months, remaining_seconds = divmod(remaining_seconds, MONTHS_FACTOR)
        normalized.weeks, remaining_seconds = divmod(remaining_seconds, WEEKS_FACTOR)
        normalized.days, remaining_seconds = divmod(remaining_seconds, DAYS_FACTOR)
        normalized.hours, remaining_seconds = divmod(remaining_seconds, HOURS_FACTOR)
        normalized.minutes, remaining_seconds = divmod(remaining_seconds, MINUTES_FACTOR)
        normalized.seconds = remaining_seconds

        return normalized
