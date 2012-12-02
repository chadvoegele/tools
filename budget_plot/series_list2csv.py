def series_list2csv(output_filename, csv_input):
  from numpy import array as array
  import csv

  input_dim = get_list_dim(csv_input)

  import datetime
  output_mat = [];
  for i_series in range(0,len(csv_input)):
    if isinstance(csv_input[i_series], list):
      tmp_mat = []
      for y_series in range(0, len(csv_input[i_series])):
        tmp_mat.append(csv_input[i_series][y_series].to_array())
      append_mat = pad_array(tmp_mat, 2, '');
      append_mat = join_array(append_mat, 1, '', 0);
      output_mat.append(append_mat)
    else:
      output_mat.append(csv_input[i_series].to_array())

  output_mat = pad_array(output_mat, 2, '')
  output_mat = join_array(output_mat, 1, '', 1)
  output_list = output_mat.transpose().tolist()

  with open(output_filename, 'w') as fid:
    csv_writer = csv.writer(fid)
    csv_writer.writerows(output_list)

  return output_filename

def get_list_dim(in_list, last_dim=1):
  if type(in_list[0]) == list:
    return get_list_dim(in_list[0], last_dim+1)
  return last_dim

def pad_array(in_array_list, dim, pad_char):
  # only works for two dimensions, dim = 1 or dim = 2
  from numpy import array as array, concatenate

  if dim == 1:
    add_dim = 0; other_dim = 1;
  elif dim == 2:
    add_dim = 1; other_dim = 0;
  else:
    raise Exception("dim not supported")

  max_size = 0
  for i_array in range(0, len(in_array_list)):
    max_size = max(max_size, in_array_list[i_array].shape[add_dim])

  output = [];
  for i_array in range(0, len(in_array_list)):
    cur_add_dim = in_array_list[i_array].shape[add_dim]
    cur_other_dim = in_array_list[i_array].shape[other_dim]
    if add_dim == 1:
      add_array = array([[pad_char]*(max_size-cur_add_dim)]*cur_other_dim)
    elif add_dim == 0:
      add_array = array([[pad_char]*cur_other_dim]*(max_size-cur_add_dim))

    if add_array.shape[0] == 0\
        or (len(add_array.shape) > 1 and add_array.shape[1] == 0):
      output.append(in_array_list[i_array])
    else:
      output.append(concatenate((in_array_list[i_array],\
        add_array),\
        axis = add_dim))

  return output

def join_array(in_array_list, dim, pad_char, num_sep_cols):
  from numpy import array as array

  if dim == 1:
    add_dim = 0; other_dim = 1;
  elif dim == 2:
    add_dim = 1; other_dim = 0;
  else:
    raise Exception("dim not supported")

  # assume that all arrays are like sized along other_dim
  other_dim_size = in_array_list[0].shape[other_dim]

  add_dim_size = 0;
  for i_array in range(0, len(in_array_list)):
    add_dim_size = add_dim_size + in_array_list[i_array].shape[add_dim]

  add_dim_size = add_dim_size + (len(in_array_list)-1)*num_sep_cols

  # use 50 character data type
  data_type = '<U50'
  if add_dim == 0:
    output = array([[pad_char]*other_dim_size]*add_dim_size, data_type)
  elif add_dim == 1:
    output = array([[pad_char]*add_dim_size]*other_dim_size, data_type)

  cur_rowcol = 0
  for i_array in range(0, len(in_array_list)):
    cur_add_shape = in_array_list[i_array].shape[add_dim]
    if add_dim == 0:
      output[cur_rowcol:(cur_rowcol+cur_add_shape)]\
          = in_array_list[i_array]
    elif add_dim == 1:
      output[:,cur_rowcol:(cur_rowcol+cur_add_shape)]\
          = in_array_list[i_array]

    cur_rowcol = cur_rowcol + cur_add_shape + num_sep_cols

  return output
