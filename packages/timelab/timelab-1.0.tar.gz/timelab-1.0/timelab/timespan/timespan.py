from timelab.core.base import Base


class TimeSpan(Base):
    def __add__(self, other):
        assert isinstance(other, TimeSpan), AssertionError(f"Only 'TimeSpan' can be added to 'TimeSpan', Got '{type(other)}' instead")

        return TimeSpan(
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
        assert isinstance(other, TimeSpan), AssertionError(f"Only 'TimeSpan' can be subtracted to 'TimeSpan', Got '{type(other)}' instead")

        return TimeSpan(
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
        assert isinstance(other, TimeSpan), AssertionError(f"Only 'TimeSpan' can be added to 'TimeSpan', Got '{type(other)}' instead")

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

    def __isub__(self, other):
        assert isinstance(other, TimeSpan), AssertionError(f"Only 'TimeSpan' can be added to 'TimeSpan', Got '{type(other)}' instead")

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

    def as_datetime(self):
        from timelab.datetime.datetime import DateTime
        return DateTime(**self.as_dictionary())
