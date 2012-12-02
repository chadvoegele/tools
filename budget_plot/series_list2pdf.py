def series_list2pdf(output_filename, series_input):
  import matplotlib.pyplot as plt
  import matplotlib.dates as mdates
  from matplotlib.backends.backend_pdf import PdfPages
  
  pp = PdfPages(output_filename)
  color = ['r','g','k']

  for i_series in range(0,len(series_input)):
    fig = plt.figure(figsize=(10,6))
    ax = plt.axes()
    if isinstance(series_input[i_series], list):
      for y_series in range(0, len(series_input[i_series])):
        new_series = series_input[i_series][y_series]
        ax.plot(new_series.get_x(), new_series.get_y(),\
            color[y_series]+'-', label=new_series.get_des())
    else:
      new_series = series_input[i_series]
      ax.plot(new_series.get_x(), new_series.get_y(),\
          color[y_series]+'-', label=new_series.get_des())

    leg = ax.legend()
    ax.xaxis.set_label_text('Time')
    ax.yaxis.set_label_text('Amount ($)')
    month_locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(month_locator)
    dt_fmter = mdates.AutoDateFormatter(month_locator)
    ax.xaxis.set_major_formatter(dt_fmter)
    plt.savefig(pp, format='pdf')

  pp.close()
