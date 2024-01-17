import datetime
import json
from datetime import datetime, timedelta, timezone

file = "settings.json"

def next_friday_six_pm():
    today = datetime.now(timezone(timedelta(hours=8)))  
    days_until_friday = (4 - today.weekday() + 7) % 7

    next_friday_date = today + timedelta(days=days_until_friday)

    next_friday_six_pm = datetime(next_friday_date.year, next_friday_date.month, next_friday_date.day, 18, 0, 0, 0, tzinfo=timezone(timedelta(hours=8)))

    return next_friday_six_pm

def check_next_announcement_time():
    now = datetime.now(timezone(timedelta(hours=8)))
    next_announcement_time = read_next_announcement_time() 
    if next_announcement_time is None:
        return True
    else:
        return now >= next_announcement_time

def write_next_announcement_time(next_announcement_time):
    if isinstance(next_announcement_time, datetime):
        next_announcement_time_str = next_announcement_time.isoformat()
    else:
        raise TypeError("next_announcement_time must be a datetime object")
    with open(file, "w", encoding="utf-8") as f:
        json.dump({"next_announcement_time": next_announcement_time_str}, f)

def read_next_announcement_time():
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            next_announcement_time = datetime.fromisoformat(data["next_announcement_time"])
            return next_announcement_time
    except FileNotFoundError:
        return None
    except KeyError:
        return None