def get_from_ledger(account_str, time_freq, start_date, end_date):
  # time_freq is time_frequency object
  # start_date, end_date are date objects
  from subprocess import Popen
  from subprocess import PIPE

  years = time_freq.get_years();
  months = time_freq.get_months();
  weeks = time_freq.get_weeks();
  days = time_freq.get_days();

  if sum([years > 0, months > 0, weeks > 0, days > 0]) > 1:
    raise Exception("Frequency not supported.")

  cmd_string = ["ledger", "-E", "-R", "-V", "-n", "-j",\
      "--period",  "every " +\
      build_ledger_period(years, months, weeks, days) +\
      " from " +\
      build_ledger_date(start_date) +\
      " to " +\
      build_ledger_date(end_date),\
      "reg",\
      " " + account_str]

  ledger_cmd = Popen(cmd_string, stdout=PIPE)
  ledger_out = ledger_cmd.communicate()[0].decode("ascii")

  (dates, values) = parse_ledger_output(ledger_out)
  return (dates, values)

def build_ledger_period(years, months, weeks, days):
  if years > 0:
    return str(year) + " years"
  elif months > 0:
    return str(months) + " months"
  elif weeks > 0:
    return str(weeks) + " weeks"
  elif days > 0:
    return str(days) + " days"
    
def build_ledger_date(date_obj):
  return date_obj.strftime("%Y/%m/%d")

def parse_ledger_output(in_str):
  import datetime  # do i really need this here?

  out_date = []
  out_val = []

  str_idx = 0
  while str_idx < len(in_str):
    space_idx = in_str.find(" ", str_idx)
    newline_idx = in_str.find("\n", str_idx)
    in_date = in_str[str_idx:space_idx]
    in_val = in_str[space_idx+1:newline_idx]
    str_idx = newline_idx + 1

    out_date.append(datetime.datetime.strptime(in_date, "%Y-%m-%d").date())
    out_val.append(float(in_val))

  return (out_date, out_val)
