import datetime

def get_time(format: str):
    return datetime.datetime.now().strftime(format)