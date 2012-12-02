class budget_config:
  def __init__(self, input_filename):
    self.__parse_budget_config(input_filename)

  def __parse_budget_config(self, input_filename):
    import re, shlex
    from time_frequency import time_frequency

    self.output_format = "csv"
    self.accounts = []
    self.output_filename = []

    bAcct = False
    with open(input_filename, 'r') as fid:
      for line in fid:
        line = re.sub("=", " = ", line)
        line_split = shlex.split(line, comments=True)
        if len(line_split) == 0:
          continue

        if line_split[0] == "~Accounts":
          bAcct = True
          continue

        find_eq_bool = list(map(lambda x: x == '=', line_split))
        if (not any(find_eq_bool) or not find_eq_bool[1]):
            raise Exception("Invalid config.")

        config_item_name = line_split[0]
        config_item_val = line_split[2]

        # maybe easier to do this with an eval
        if config_item_name == "output_filename":
          self.output_filename = config_item_val

        if config_item_name == "output_format":
          self.output_format = config_item_val

        if bAcct:
          self.accounts.append(\
            [config_item_name, time_frequency(config_item_val)])

    if len(self.output_filename) == 0 and self.output_format == "csv":
      raise Exception("Must specify a filename if using csv output")

    if len(self.accounts) == 0:
      raise Exception("No accounts specified")
