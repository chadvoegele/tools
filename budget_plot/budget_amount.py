class budget_amount:
  """budget_amount object"""
  # input is lists of amounts, time frequencies, start dates, and end dates 
  # for perpetuity amount use "*" for the start date and end date
  # budget_amount(budget_id, amt, time_f, start_date, end_date)
  # budget_amount(budget_id)
  def __init__(self, *args):
    from time_frequency import time_frequency

    if len(args) == 0:
      raise Exception("Must define a budget id")
    self.budget_id = args[0]
  
    # set this up as the default
    self.budgets_amt = [0]
    self.budgets_time_f = [time_frequency('1M')]
    self.budgets_start_date = ['*']
    self.budgets_end_date = ['*']

    if len(args) >= 2 and len(args) <= 4:
      raise Exception("Must specify all budget components.")

    if len(args) == 5:
      self.add_budgets(args[1], args[2], args[3], args[4])

  def add_budgets(self, amt, time_f, start_date, end_date):
    # input must be in lists
    if not isinstance(amt, list):
      amt = [amt]
    if not isinstance(time_f, list):
      time_f = [time_f]
    if not isinstance(start_date, list):
      start_date = [start_date]
    if not isinstance(end_date, list):
      end_date = [end_date]

    if not len(amt) == len(time_f) or not len(amt) == len(start_date) or\
        not len(amt) == len(end_date):
      raise Exception("Invalid budget amounts.")

    try:
      perpetual_idx = start_date.index('*')
      if not end_date[perpetual_idx] == '*':
        raise Exception("perpetual not aligned")

      # swaps the element in the list
      # x[3], x[0] = x[0], x[3] swaps elements in list
      self.budgets_amt[0] = amt[perpetual_idx]
      self.budgets_time_f[0] = time_f[perpetual_idx]
      self.budgets_start_date[0] = start_date[perpetual_idx]
      self.budgets_end_date[0] = end_date[perpetual_idx]

      del amt[perpetual_idx]; del time_f[perpetual_idx]
      del start_date[perpetual_idx]; del end_date[perpetual_idx] 

    except ValueError:
      pass

    # no structures unless I make another class...
    self.budgets_amt.extend(amt)
    self.budgets_time_f.extend(time_f)
    self.budgets_start_date.extend(start_date)
    self.budgets_end_date.extend(end_date)
  
  def get_budget_amt(self, time_freq, start_date, end_date):
    # date intervals are [a,b). in ledger too.
    # idea here is store list of lists in the form of
    #   [date, original_date_flag, amt_idx]

    date_interval = [[start_date, True, 0]]
    counter = 0
    while date_interval[-1][0] < end_date:
      new_date = time_freq + date_interval[-1][0]
      if new_date > end_date:
        new_date = end_date
      date_interval.append([new_date, True, 0])
    
    out_date_interval = [y[0] for y in date_interval]

    # overrides start at index 1
    for i_override in range(1, len(self.budgets_start_date)):
      over_sd = self.budgets_start_date[i_override]
      over_ed = self.budgets_end_date[i_override]
      # check if we need to do anything
      if (over_sd >= start_date and over_sd < end_date) or\
          (over_ed > start_date and over_ed <= end_date):

        # override should not extend outside the original interval
        if over_sd < start_date: insert_sd = start_date
        else: insert_sd = over_sd
        
        if over_ed > end_date: insert_ed = end_date
        else: insert_ed = over_ed

        # replace existing date if override is same date
        try:
          sd_idx = [y[0] for y in date_interval].index(insert_sd)
          if date_interval[sd_idx][1]:
            orig_sd_flag = True
          else:
            orig_sd_flag = False
          overwritten_budget_idx = date_interval[sd_idx][2]
          del date_interval[sd_idx]
        except ValueError:
          orig_sd_flag = False

        date_interval.append([insert_sd, orig_sd_flag, i_override])
        date_interval = sorted(date_interval, key=lambda x: x[0])

        # TODO: does anything change in the first block of this try?
        try:
          ed_idx = [y[0] for y in date_interval].index(insert_ed)
          if date_interval[ed_idx][1]:
            orig_ed_flag = True 
          else:
            orig_ed_flag = False
          budget_idx = date_interval[ed_idx][2]
          del date_interval[ed_idx]
        except ValueError:
          closest_idx = find_closest_index(\
              [y[0] for y in date_interval], insert_ed)
          budget_idx = date_interval[closest_idx][2]
          # TODO: bad hack. problem is original budget_idx is overwritten.
          # fix by storing old idx and if overwritten take old...
          if budget_idx == i_override:
            budget_idx = overwritten_budget_idx
          orig_ed_flag = False

        date_interval.append([insert_ed, orig_ed_flag, budget_idx])

        date_interval = sorted(date_interval, key=lambda x: x[0])

        # 1+ because want to reset first one after start
        start_idx = 1+[y[2] for y in date_interval].index(i_override)
        while date_interval[start_idx][0] < insert_ed:
          date_interval[start_idx][2] = i_override
          start_idx = start_idx + 1

    # original date indices
    out_idx = [i for (i,x) in enumerate([y[1] for y in date_interval]) if x]

    # if overrides, break up date ranges here
    budget_amt = []
    for i_date in range(0, len(date_interval)-1):
      budget_amt.append(get_one_budget_amt(\
          self.budgets_amt[date_interval[i_date][2]],\
          self.budgets_time_f[date_interval[i_date][2]],\
          date_interval[i_date][0], date_interval[i_date+1][0]))

    out_budget_amt = []
    for i_date in range(0, len(out_idx)-1):
      out_budget_amt.append(sum(budget_amt[out_idx[i_date]:out_idx[i_date+1]]))

    return (out_date_interval[0:-1], out_budget_amt)

def get_one_budget_amt(amt, time_frequency, start_date, end_date):
  import datetime
  # no +1 because open interval!
  date_range = end_date - start_date
  ratio = date_range.days/time_frequency.to_days()
  ratio = approx_round(ratio)
  return amt*ratio

# bit of art here.
# round to nearest tenth so we don't get weird numbers
def approx_round(in_val):
  return round(in_val*10)/10

# def find_closest_index(find_in_list, find_val):
# find_in_list should already be sorted!!!
# return the index for the list element just before find_val
def find_closest_index(find_in_list, find_val):
  num_list = len(find_in_list)
  idx = num_list//2

  if find_in_list[idx] < find_val:
    while find_in_list[idx] < find_val:
      idx = idx + 1
    return idx - 1
  else:
    while find_in_list[idx] > find_val:
      idx = idx - 1
    return idx

def parse_money_str(money_str):
  import re
  amt = re.match('\$*(\d+[.\d*]\d*)', money_str.replace(',',''))
  return float(amt.group(1))

def get_budget_by_id(in_budgets, in_id):
  if not isinstance(in_budgets, list):
    in_budgets = [in_budgets]

  idx = [i for (i,x) in enumerate(in_budgets)\
      if not x.budget_id.lower().find(in_id.lower()) == -1]
  return idx

def parse_ledger_budget(in_filename):
  import re, shlex
  from time_frequency import time_frequency
  from datetime import datetime

  budgets = []

  budget_defined = False
  with open(in_filename, 'r') as fid:
    for line in fid:
      line_split = shlex.split(line, comments=True)
      if len(line_split) == 0:
        continue

      if line_split[0]=='~':
        if len(line_split) <= 1:
          raise Exception("Budget missing time period after ~")
        time_f = time_frequency(line_split[1])
        start_date = '*'
        end_date = '*'
        budget_defined = True

        if len(line_split) >= 3:
          if len(line_split) <= 5:
            raise Exception("Incomplete start and end date expression.")

          for i in range(2, 6, 2):
            try: 
              in_date = datetime.strptime(line_split[i+1], '%Y/%m/%d').date()
            except ValueError:
              in_date = datetime.strptime(line_split[i+1], '%m/%d/%Y').date()
            except ValueError:
              raise Exception("Date cannot be parsed.")

            if line_split[i].lower() == 'from':
              start_date = in_date

            elif line_split[i].lower() == 'to':
              end_date = in_date

            else:
              raise Exception("Unknown format in date expression.")
        continue

      # must be an account right?
      if len(line_split) <= 2:
        if len(line_split) == 1 and line_split[0] == 'assets':
          continue

        if len(line_split) == 1:
          raise Exception("no value for account")

        account_str = line_split[0]
        amt = parse_money_str(line_split[1])

        if not budget_defined:
          raise Exception("budget account defined before time period.")

        find_budget_idx = get_budget_by_id(budgets, account_str)
        if len(find_budget_idx) > 0:
          # maybe should if more than one idx returned
          budgets[find_budget_idx[0]].add_budgets(\
              amt, time_f, start_date, end_date)
        else:
          budgets.append(\
              budget_amount(account_str, amt, time_f, start_date, end_date))
  
  return budgets
