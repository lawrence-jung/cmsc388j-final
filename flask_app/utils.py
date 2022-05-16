from datetime import datetime


def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")

def current_day():
    return datetime.now().date