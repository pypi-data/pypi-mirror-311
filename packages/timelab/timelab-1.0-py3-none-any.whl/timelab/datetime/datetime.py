from timelab.core.base import Base
import time

time_span_cache = None

def get_timespan():
    global time_span_cache

    if time_span_cache is None:
        from timelab.timespan.timespan import TimeSpan
        time_span_cache = TimeSpan

    return time_span_cache

class DateTime(Base):
    @classmethod
    def now(cls):
        current_time = time.localtime()

        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec

        return DateTime(years=year, months=month, days=day, hours=hour, minutes=minute, seconds=second)

    def __add__(self, other):
        assert isinstance(other, get_timespan()), AssertionError(f"Invalid operation on a DateTime(), Possible operations: datetime + timespan, datetime - timespan, datetime - datetime = timespan")

        return DateTime(
            self.centuries + other.centuries,
            self.decades + other.decades,
            self.years + other.years,
            self.months + other.months,
            self.weeks + other.weeks,
            self.days + other.days,
            self.hours + other.hours,
            self.minutes + other.minutes,
            self.seconds + other.seconds,
            self.milliseconds + other.milliseconds
        )

    def __sub__(self, other):
        assert isinstance(other, (get_timespan(), DateTime)), AssertionError(f"Invalid operation on a DateTime(), Possible operations: datetime + timespan, datetime - timespan, datetime - datetime = timespan")

        if isinstance(other, get_timespan()):
            return DateTime(
                self.centuries - other.centuries,
                self.decades - other.decades,
                self.years - other.years,
                self.months - other.months,
                self.weeks - other.weeks,
                self.days - other.days,
                self.hours - other.hours,
                self.minutes - other.minutes,
                self.seconds - other.seconds,
                self.milliseconds - other.milliseconds
            )
        elif isinstance(other, DateTime):
            return get_timespan()(
                self.centuries - other.centuries,
                self.decades - other.decades,
                self.years - other.years,
                self.months - other.months,
                self.weeks - other.weeks,
                self.days - other.days,
                self.hours - other.hours,
                self.minutes - other.minutes,
                self.seconds - other.seconds,
                self.milliseconds - other.milliseconds
            )

    def __iadd__(self, other):
        assert isinstance(other, get_timespan()), AssertionError(f"Other value must be 'TimeSpan', Got '{type(other)}' instead")

        self.centuries += other.centuries
        self.decades += other.decades
        self.years += other.years
        self.months += other.months
        self.weeks += other.weeks
        self.days += other.days
        self.hours += other.hours
        self.minutes += other.minutes
        self.seconds += other.seconds
        self.milliseconds += other.milliseconds

        return self

    def __isub__(self, other):
        assert isinstance(other, get_timespan()), AssertionError(f"Other value must be 'TimeSpan', Got '{type(other)}' instead")

        self.centuries -= other.centuries
        self.decades -= other.decades
        self.years -= other.years
        self.months -= other.months
        self.weeks -= other.weeks
        self.days -= other.days
        self.hours -= other.hours
        self.minutes -= other.minutes
        self.seconds -= other.seconds
        self.milliseconds -= other.milliseconds

        return self

    def timestamp(self, time_format: str = '%Y %M %D'):
        """ Returns the timestamp in the specified format. """
        return multi_replace(time_format, self.as_dictionary(single_letter_unit_names=True))

    def as_timespan(self):
        return get_timespan()(**self.as_dictionary())


def multi_replace(string: str, replacements: dict[str, float]):
    for k, v in replacements.copy().items():
        replacements[k.upper()] = v  # Add uppercase replacements

    for replace_this, with_this in replacements.items():
        string = string.replace('%' + replace_this, str(with_this))

    return string

