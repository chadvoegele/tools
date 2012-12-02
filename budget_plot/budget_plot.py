#!/usr/bin/env python
import argparse

# start_date, end_date, budget_plot_config, ledger_budget_file, verbose
def my_parse_args():
  from datetime import date as date
  from dateutil.parser import parse

  parser = argparse.ArgumentParser(description='Budget plotting.')
  parser.add_argument('-v', dest="verbose", action="store_true", default=False,
      help='verbose')
  parser.add_argument('-s', '--start-date', dest="start_date", action="store",
      help='start date')
  parser.add_argument('-e', '--end-date', dest="end_date", action="store",
      help='end date')
  parser.add_argument('-b', '--budget-file', dest="budget_file", action="store",
      help='location of ledger budget file')
  parser.add_argument('-c', '--config-file', dest="config_file", action="store",
      help='location of budget_plot.py config file')
  args = parser.parse_args()

  if args.start_date == None or args.end_date == None\
      or args.budget_file == None or args.config_file == None:
    raise Exception('start date, end date, budget_file, and config_file'\
        +' are required')
  
  args.start_date = parse(args.start_date).date()
  args.end_date = parse(args.end_date).date()

  if args.verbose:
    print("Current parameters:")
    print("  Verbose: " + str(args.verbose))
    print("  Start Date: " + str(args.start_date))
    print("  End Date: " + str(args.end_date))
    print("  Budget File: " + args.budget_file)
    print("  budget_plot Config File: " + args.config_file)

  return args

def gen_output_series_list(start_date, end_date, accounts_config, all_budgets):
  from budget_amount import get_budget_by_id
  from get_from_ledger import get_from_ledger
  from series import series
  output_series = []
  for i_acct in range(0, len(accounts_config)):
    account_str = accounts_config[i_acct][0]
    account_timef = accounts_config[i_acct][1]
    (dates, values) = get_from_ledger(account_str, account_timef,\
        start_date, end_date)
    budget_id = get_budget_by_id(all_budgets, account_str)
    budget_values = []
    for i_budget in range(0, len(budget_id)):
      (budget_dates, tmp_budget_values)\
          = all_budgets[budget_id[i_budget]].get_budget_amt(\
            account_timef, start_date, end_date)
      budget_values.append(tmp_budget_values)

    # sum of transposed list
    budget_values = [sum(x) for x in list(zip(*budget_values))]

    if len(budget_id) >= 1:
      output_series.append([series(dates, values, account_str),\
          series(budget_dates, budget_values, account_str+' budget')])
    else:
      output_series.append(series(dates, values, account_str))

  return output_series

def write_series_list(output_format, output_filename, output_series):
  if output_format == 'csv':
    # return output matrix instead which can then write here??
    from series_list2csv import series_list2csv
    series_list2csv(output_filename, output_series)
  elif output_format == 'pdf':
    from series_list2pdf import series_list2pdf
    series_list2pdf(output_filename, output_series)

def main():
  from budget_amount import parse_ledger_budget
  from budget_config import budget_config
  args = my_parse_args()

  config = budget_config(args.config_file)
  accounts_config = config.accounts

  budget_filename = args.budget_file
  all_budgets = parse_ledger_budget(budget_filename)

  output_series = gen_output_series_list(\
      args.start_date, args.end_date, accounts_config, all_budgets)

  write_series_list(config.output_format, config.output_filename, output_series)

if __name__ == "__main__":
  main()
