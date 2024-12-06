from datetime import timedelta


def display(d: timedelta, use_double_digits: bool = False) -> str:
    years = int(d.days / 365)
    remaining = d.days % 365
    weeks = int(remaining / 7)
    days = remaining % 7

    hours = int(d.seconds / 3600)
    remaining = d.seconds % 3600
    minutes = int(remaining / 60)
    seconds = remaining % 60

    if use_double_digits:
        if years:
            return f"{years:02}y{weeks:02}w"
        if weeks:
            return f"{weeks:02}w{days:02}d"
        if days:
            return f"{days:02}d{hours:02}h"
        if hours:
            return f"{hours:02}h{minutes:02}m"
        if minutes:
            return f"{minutes:02}m{seconds:02}s"
        return f"{seconds}s"
    else:
        if years:
            return f"{years}y{weeks}w"
        if weeks:
            return f"{weeks}w{days}d"
        if days:
            return f"{days}d{hours}h"
        if hours:
            return f"{hours}h{minutes}m"
        if minutes:
            return f"{minutes}m{seconds}s"
        return f"{seconds}s"
