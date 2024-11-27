import anvil.server
from anvil.tables import app_tables


def run_callable():
    """
    Make sure a special secret is defined when calling any callable from the Anvil Squared dependency.

    This avoids any unintended server calls of callables in this app
    when using this app as a dependency.
    """
    if anvil.server.context.client.type:
        try:
            _ = anvil.secrets.get_secret('SQUARED')
        except anvil.secrets.SecretError as e:
            print_timestamp(str(e.args[0]))


def print_timestamp(input_str, verbose=True):
    # TODO: make this flexible to print any object
    if verbose:
        import datetime as dt
        import pytz
        eastern_tz = pytz.timezone('US/Eastern')
        current_time = dt.datetime.now(eastern_tz)
        formatted_time = current_time.strftime('%H:%M:%S.%f')
        print(f"{input_str} : {formatted_time}")





def list_to_csv(data):
    """Output a list of dicts to csv."""
    import io
    import csv
    import anvil.media
    
    output = io.StringIO()
    
    # Create a CSV writer object
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    # Write the header
    writer.writeheader()
    # Write the data
    for row in data:
        writer.writerow(row)
    # Get the CSV content
    csv_content = output.getvalue()
    # Close the string buffer
    output.close()
    
    # Create a media object from the CSV content
    csv_file = anvil.BlobMedia('text/csv', csv_content.encode('utf-8'), 'data.csv')
    return csv_file