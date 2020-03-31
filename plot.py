""" plotting fuctions for anoroc """
import numpy
import pandas
import extract
import data
import constants
from bokeh.io import output_file, save
from bokeh.models import Panel, Tabs, DatetimeTickFormatter, Div, HoverTool
from bokeh.layouts import gridplot, column
from bokeh.plotting import figure

WIDTH = 700
HEIGHT = 300


def countries(countries, title=None, debug=False):
    """ Plot data with Bokeh.

        Make four graphs: logscale cumulative cases, new cases,
        cumulative deaths, new deaths
    """

    # count confirmed cases
    count, dates = extract.get_countries(countries, data.confirmed)
    new_cases = count - numpy.insert(count, 0, 0)[:-1]
    dates = pandas.to_datetime(dates)

    # count death cases
    count_d, dates_d = extract.get_countries(countries, data.death)
    new_cases_d = count_d - numpy.insert(count_d, 0, 0)[:-1]

    # count recovered cases
    count_r, dates_r = extract.get_countries(countries, data.recovered)
    new_cases_r = count_r - numpy.insert(count_r, 0, 0)[:-1]

    if count.any() == 0:
        print("Data set empty. Probably you misspelled country name.")
        return

    # date format of x-axis
    format = "%b %d"

    TOOLTIPS = [
        ("Count", "$y{i}"),
    ]

    plot_options = dict(
        width=WIDTH,
        plot_height=HEIGHT,
        # tools="pan,wheel_zoom,hover",
        x_axis_type="datetime",
        # toolbar_location="below",
    )

    t1 = figure(
        x_axis_label="Date",
        y_axis_label="Cumulative Cases",
        tooltips=TOOLTIPS,
        **plot_options,
    )

    t1.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    t1.line(dates, count, line_width=3, color="red", alpha=0.7)
    t1.circle(
        dates, count, size=7, color="red", fill_color="white", legend_label="Cases"
    )
    t1.line(dates, count_r, line_width=3, color="green", alpha=0.7)
    t1.circle(
        dates,
        count_r,
        size=7,
        color="green",
        fill_color="white",
        legend_label="Recovered",
    )

    t1.legend.location = "top_left"
    tab1 = Panel(child=t1, title="Linear")

    t2 = figure(
        x_axis_label="Date",
        y_axis_label="Cumulative Cases",
        y_axis_type="log",
        tooltips=TOOLTIPS,
        **plot_options,
    )

    t2.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    t2.line(dates, count, line_width=3, color="red", alpha=0.7)
    t2.circle(
        dates, count, size=7, color="red", fill_color="white", legend_label="Cases"
    )
    t2.line(dates, count_r, line_width=3, color="green", alpha=0.7)
    t2.circle(
        dates,
        count_r,
        size=7,
        color="green",
        fill_color="white",
        legend_label="Recovered",
    )

    t2.legend.location = "top_left"

    tab2 = Panel(child=t2, title="Log")

    p1 = Tabs(tabs=[tab1, tab2])

    p2 = figure(x_axis_label="Date", y_axis_label="New Cases", **plot_options)

    p2.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    p2.vbar(
        x=dates,
        top=new_cases,
        bottom=0,
        width=50000000,
        color="red",
        alpha=0.9,
        legend_label="Cases",
    )
    p2.vbar(
        x=dates,
        top=new_cases_r,
        bottom=0,
        width=50000000,
        color="green",
        alpha=0.7,
        legend_label="Recovered",
    )

    p2.legend.location = "top_left"

    t1 = figure(
        x_axis_label="Date",
        y_axis_label="Cumulative Deaths",
        tooltips=TOOLTIPS,
        **plot_options,
    )

    t1.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    t1.line(dates, count_d, line_width=3, color="black", alpha=0.7)
    t1.circle(
        dates, count_d, size=7, color="black", fill_color="white",
    )

    tab1 = Panel(child=t1, title="Linear")

    t2 = figure(
        x_axis_label="Date",
        y_axis_label="Comulative Deaths",
        y_axis_type="log",
        tooltips=TOOLTIPS,
        **plot_options,
    )

    t2.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    t2.line(dates, count, line_width=3, color="black", alpha=0.7)
    t2.circle(dates, count, size=7, color="black", fill_color="white")

    tab2 = Panel(child=t2, title="Log")

    p3 = Tabs(tabs=[tab1, tab2])

    p4 = figure(x_axis_label="Date", y_axis_label="New Deaths", **plot_options)

    p4.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    p4.vbar(
        x=dates, top=new_cases_d, bottom=0, width=50000000, color="black", alpha=0.5
    )

    # make a grid
    grid = gridplot([[p1, p3], [p2, p4]], toolbar_location="below")

    output_file(constants.FILE_BOKEH)

    title = "<h2>" + title + "</h2>"
    title = Div(text=title)
    save(column(title, grid))
