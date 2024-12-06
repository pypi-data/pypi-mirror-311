
MINUTES_FACTOR = 60
HOURS_FACTOR = MINUTES_FACTOR * 60
DAYS_FACTOR = HOURS_FACTOR * 24
WEEKS_FACTOR = DAYS_FACTOR * 7
MONTHS_FACTOR = DAYS_FACTOR * 30
YEARS_FACTOR = MONTHS_FACTOR * 12
DECADES_FACTOR = YEARS_FACTOR * 10
CENTURIES_FACTOR = DECADES_FACTOR * 10

def total_seconds(centuries=0, decades=0, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0):
    total_secs = 0
    total_secs += milliseconds / 1000
    total_secs += seconds
    total_secs += minutes * MINUTES_FACTOR
    total_secs += hours * HOURS_FACTOR
    total_secs += days * DAYS_FACTOR
    total_secs += weeks * WEEKS_FACTOR
    total_secs += months * MONTHS_FACTOR
    total_secs += years * YEARS_FACTOR
    total_secs += decades * DECADES_FACTOR
    total_secs += centuries * CENTURIES_FACTOR

    return total_secs

