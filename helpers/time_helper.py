from .. import datetime

# convert string date to timestamp
def date_to_string(date: datetime.datetime) -> str:
    print(date.strftime("%Y-%m-%d"))
