from datetime import timedelta


def timedelta_to_string(td: timedelta) -> str:
    result_parts: list[str] = []
    days = td.days
    hours, rem = divmod(td.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    if days:
        result_parts.append(f'{days} days' if days != 1 else '1 day')
    if hours:
        result_parts.append(f'{hours} hours' if hours != 1 else '1 hour')
    if minutes:
        result_parts.append(f'{minutes} minutes' if minutes != 1 else '1 minute')
    if seconds:
        result_parts.append(f'{seconds} seconds' if seconds != 1 else '1 second')
    return ', '.join(result_parts)
