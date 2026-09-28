import re
from functools import wraps

class InvalidDateError(Exception):
    pass

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[SYSTEM LOG] Executing action: {func.__name__.replace('_', ' ')}...")
        return func(*args, **kwargs)
    return wrapper

def validate_date(date_str):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        raise InvalidDateError("Date must be in the exact format YYYY-MM-DD (e.g., 2026-05-01).")
    return True