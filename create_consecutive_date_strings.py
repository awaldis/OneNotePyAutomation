import datetime

def get_consecutive_days(start_date_str="", num_days=7):
    """
    Generates an array of strings representing consecutive days.

    Args:
        start_date_str (str): The starting date in the format "YYYY-MMM-DD".
        num_days (int): The number of consecutive days to generate.

    Returns:
        list: An array of strings in the format "YYYY-MMM-DD - Weekday", or an empty list if an error occurs.
    """

    try:
        # Ensure num_days is an integer and nonnegative
        num_days = int(num_days)
        if num_days < 0:
            raise ValueError("Number of days must be nonnegative.")

        # Use the current date if start_date_str is empty
        if start_date_str == "":
            start_date = datetime.datetime.today()
        else:
            # Parse the starting date
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%b-%d")
    except ValueError as ve:
        print(f"Error: {ve}")
        return []
    except TypeError:
        print("Invalid type for num_days. Please provide an integer.")
        return []
    except OverflowError:
        print("Date range overflow. Please use a smaller number of days.")
        return []

    # Create the array to store the dates
    days = []

    # Generate the consecutive dates
    for i in range(num_days):
        day = start_date + datetime.timedelta(days=i)
        days.append(day.strftime("%Y-%b-%d - %A"))

    return days
