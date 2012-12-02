class time_frequency:
  """time_frequency object"""
  def __init__(self, *args):
  # def __init__(self, years, months, weeks, days):
    if len(args) == 4 and isnum(args[0]) and isnum(args[1]) \
        and isnum(args[2]) and isnum(args[3]):
      self._years = args[0]
      self._months = args[1] 
      self._weeks = args[2]
      self._days = args[3]

    if len(args) == 1 and ischar(args[0]):
      self.__parse_string_frequency(args[0])

  def get_years(self):
    return self._years

  def get_months(self):
    return self._months

  def get_weeks(self):
    return self._weeks

  def get_days(self):
    return self._days

  def to_days(self):
    return self.get_years()*365.25 + self.get_months()*365.25/12\
        + self.get_weeks()*7 + self.get_days()

  def __add__(self, in_arg):
    import datetime
    if isinstance(in_arg, datetime.datetime) or\
        isinstance(in_arg, datetime.date):
      new_year = in_arg.year + self.get_years()
      new_month = in_arg.month + self.get_months()
      add_year = (new_month-1)//12
      new_month = (new_month-1)%12+1  # 12 should be 12, 13 should be 1
      new_year = new_year + add_year
      week_timedelta = datetime.timedelta(7*self.get_weeks())
      days_timedelta = datetime.timedelta(self.get_days())

      out_date = datetime.date(new_year, new_month, in_arg.day)
      return out_date + week_timedelta + days_timedelta

    else:
      raise Exception("Don't know how to add here")
  
  def __radd__(self, in_arg):
    return self.__add__(in_arg)

  def __parse_string_frequency(self, in_str):
    import re
    # ex: '1D', '3M'
    m1 = re.match("(\d+)([a-zA-Z])", in_str)
    # ex: 'Monthly'
    m2 = re.match("[a-zA-Z]+", in_str) 

    # if no matches the error
    if m1 == None and m2 == None:
      raise Exception("Invalid time frequency string.")

    # if we matched 1, parse this first and return
    if not m1 == None:
      amt=m1.group(1)
      str_freq=m1.group(2)

      self._years = 0
      self._months = 0
      self._weeks = 0
      self._days = 0
      if str_freq.lower() == "y":
        self._years = int(amt)
      if str_freq.lower() == "m":
        self._months = int(amt)
      if str_freq.lower() == "w":
        self._weeks = int(amt)
      if str_freq.lower() == "d":
        self._days = int(amt)
      return

    # if we matched 2, parse this and return
    if not m2 == None:
      match_string = m2.string
      self._years = 0
      self._months = 0
      self._weeks = 0
      self._days = 0
      if match_string.lower() == 'daily':
        self._days = 1
      if match_string.lower() == 'monthly':
        self._months = 1
      if match_string.lower() == 'quarterly':
        self._months = 3
      if match_string.lower() == 'yearly':
        self._years = 1
      return

def isnum(in_arg):
  return isinstance(in_arg, float) or isinstance(in_arg, int)

def ischar(in_arg):
  return isinstance(in_arg, str)
