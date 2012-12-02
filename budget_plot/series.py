class series:
  """data series object"""
  def __init__(self, x, y, des = ""):
    self._x = x
    self._y = y
    self._des = des

  def get_x(self):
    return self._x

  def get_y(self):
    return self._y

  def get_des(self):
    return self._des

  def to_array(self, want_des = True):
    from numpy import array as array
    import datetime
    cur_des = self.get_des()
    cur_x = self.get_x()
    cur_y = self.get_y()

    if all(list(map(lambda x:isinstance(x,(datetime.datetime, datetime.date)),\
        cur_x))):
      cur_x = list(map(str, cur_x))

    if want_des:
      out_x = [cur_des]
      out_x.extend(cur_x)

      out_y = ['']
      out_y.extend(cur_y)
    else:
      out_x = cur_x
      out_y = cur_y

    return array([out_x, out_y])

