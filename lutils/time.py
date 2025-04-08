def sec_to_hms(seconds, string=True, short=False):
    """Convert seconds to hours, minutes, and seconds."""
    if isinstance(seconds, str) and ":" in seconds:
        return sec_to_hms(hms_to_sec(seconds), string=string, short=short)
    if isinstance(seconds, str) and seconds.isdigit() or isinstance(seconds, float):
        seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if string:
        if h == 0 and short:
            return f"{m:02d}:{s:02d}"
        return f"{h:02d}:{m:02d}:{s:02d}"
    return h, m, s


def hms_to_sec(time_str, enable_single_part=False):
    """Convert hours, minutes, and seconds to total seconds."""
    if isinstance(time_str, (int, float)):
        return time_str
    if isinstance(time_str, str) and time_str.isdigit():
        return int(time_str)

    parts = time_str.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = parts
        seconds = float(seconds) if "." in seconds else int(seconds)
        minutes = int(minutes)
        if minutes >= 60 or seconds >= 60:
            return False
        total_seconds = int(hours) * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes, seconds = parts
        seconds = float(seconds) if "." in seconds else int(seconds)
        minutes = int(minutes)
        if seconds >= 60:
            return False
        total_seconds = int(minutes) * 60 + seconds
    elif len(parts) == 1 and enable_single_part:
        seconds = float(parts[0]) if "." in parts[0] else int(parts[0])
        total_seconds = seconds
    else:
        raise ValueError("Invalid time format")
    return total_seconds
