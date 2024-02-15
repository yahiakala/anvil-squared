import anvil.server
from anvil.tables import app_tables


@anvil.server.callable
def ping():
    print_timestamp("ping")
    return "pong"


def print_timestamp(input_str, verbose=True):
    if verbose:
        import datetime as dt
        import pytz
        eastern_tz = pytz.timezone('US/Eastern')
        current_time = dt.datetime.now(eastern_tz)
        formatted_time = current_time.strftime('%H:%M:%S.%f')
        print(f"{input_str} : {formatted_time}")