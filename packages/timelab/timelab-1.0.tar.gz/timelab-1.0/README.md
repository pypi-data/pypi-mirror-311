# TimeLab
This library handles everything related to time, Heres an example of how to use this library:

```python
from timelab import TimeSpan

timespan = TimeSpan(minutes=100)
print(timespan.seconds)  # Output: 0
print(timespan.minutes)  # Output: 100
print(timespan.hours)    # Output: 0

# Find total
print(timespan.total_seconds())  # Output: 6000
print(timespan.total_minutes())  # Output: 100
print(timespan.total_hours())    # Output: 1.6~

# Add time
print(TimeSpan(minutes=100) + TimeSpan(minutes=30))  # Output: TimeSpan(130 minutes)

# Subtract time
print(TimeSpan(minutes=100) - TimeSpan(minutes=30))  # Output: TimeSpan(70 minutes)

# Normalize time
# Normalize() will normalize the time format to make it more readable
print(TimeSpan(seconds=125).normalize())  # Output: TimeSpan(2 minutes, 5 seconds)
print(TimeSpan(hours=2.5).normalize())  # Output: TimeSpan(2 hours, 30 minutes)

# Get time as dictionary
print(TimeSpan(hours=2.5).as_dictionary())  # Output: {'hours': 2.5, 'centuries': 0.0, 'years': 0.0, ...}
print(TimeSpan(hours=2.5).as_dictionary())  # Output: {'hours': 2.5, 'centuries': 0.0, 'years': 0.0, ...}

# As datetime
print(TimeSpan(hours=2.5).as_datetime())  # Output: DateTime(2.5 hours)
```

And usage for datetime:

```python
from timelab import DateTime, TimeSpan

# Timestamp
print(DateTime.now().timestamp())  # Output format: Year-Month-Day

# Timestamp with custom format
print(DateTime.now().timestamp(time_format='Year: %Y, Month: %M, Day: %D'))  # Output format: Year: Year, Month: Month, Day: Day

# As timespan
print(DateTime.now().as_timespan())

# Add and subtract timespan to datetime
print(DateTime.now() + TimeSpan(minutes=30))
print(DateTime.now() - TimeSpan(minutes=30))

# Get difference between 2 datetimes
print(DateTime.now() - DateTime.now())  # Returns the difference as a timespan
```