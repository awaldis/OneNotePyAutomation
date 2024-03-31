import datetime

def get_consecutive_days(start_date_str="2024-Mar-21", num_days=7):
  """
  Generates an array of strings representing consecutive days.

  Args:
      start_date_str (str): The starting date in the format "YYYY-MMM-DD".
      num_days (int): The number of consecutive days to generate.

  Returns:
      list: An array of strings in the format "YYYY-MMM-DD - Weekday".
  """

  # Parse the starting date
  start_date = datetime.datetime.strptime(start_date_str, "%Y-%b-%d")

  # Create the array to store the dates
  days = []

  # Generate the consecutive dates
  for i in range(num_days):
      day = start_date + datetime.timedelta(days=i)
      days.append(day.strftime("%Y-%b-%d - %A"))

  return days
