from datetime import datetime, timedelta
# Get the date of a certain timeframe
def get_date_range(timeframe, starting_date = datetime.today() + timedelta(days=1)):
    if timeframe == 'days':
        return str((starting_date - timedelta(days=1)).strftime("%Y-%m-%d"))
    elif timeframe == 'weeks':
        return str((starting_date - timedelta(days=7)).strftime("%Y-%m-%d"))
    elif timeframe == 'months':
        return str((starting_date - timedelta(weeks=4)).strftime("%Y-%m-%d"))
    elif timeframe == 'years':
        return str((starting_date - timedelta(days=365)).strftime("%Y-%m-%d"))
    else:
        return None

# Get date of the after now
def get_date_tomorrow():
    return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

# Get the date of now
def get_date_now(hours = False):
    if hours:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.now().strftime('%Y-%m-%d')