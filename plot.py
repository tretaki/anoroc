""" plotting fuctions for anoroc """
import numpy
import pandas
import extract
import data
import constants
from bokeh.io import output_file, save
from bokeh.models import (
    Panel,
    Tabs,
    DatetimeTickFormatter,
    Div,
    HoverTool,
    Label,
    Select,
    CustomJS,
)
from bokeh.layouts import gridplot, column, row
from bokeh.plotting import figure
from bokeh.embed import components

WIDTH = 700
HEIGHT = 350


def bokeh_select_scale(figs, title="Change Scale"):
    names = [fig.name for fig in figs]
    drop = Select(title=title, value=names[0], options=names, width=100)
    # toggle = Toggle(label="Scale", button_type="success")
    for fig in figs[1:]:
        fig.visible = False

    callback = CustomJS(
        args=dict(figs=figs),
        code="""
        let selected = cb_obj.value;
        for(let fig of figs){
            fig.visible = fig.name == selected;
        }
    """,
    )

    drop.js_on_change("value", callback)

    return [drop] + figs


def boheh_add_line(figure, xdata, ydata, legend=None, color="red", alpha=0.7):
    """ Adds dataset as line points to the bokeh figure.
    """

    # constants
    line_width = 3
    point_size = 7
    legend_location = "top_left"

    # add line
    figure.line(xdata, ydata, line_width=line_width, color=color, alpha=alpha)

    # add points
    properties = dict(size=point_size, color=color, fill_color="white")
    if legend:
        properties["legend_label"] = legend

    figure.circle(xdata, ydata, **properties)

    if legend:
        figure.legend.location = legend_location


def boheh_add_vbars(figure, xdata, ydata, legend=None, color="red", alpha=0.7):
    """ Adds dataset as vertical bars to the bokeh figure.
    """

    # constants
    bar_width = 50000000
    legend_location = "top_left"

    # add line
    properties = dict(width=bar_width, color=color, alpha=alpha)
    if legend:
        properties["legend_label"] = legend
    figure.vbar(x=xdata, top=ydata, bottom=0, **properties)

    if legend:
        figure.legend.location = legend_location


def bokeh_canvas(xlabel, ylabel, logscale=False, hover=False, name=None):
    """ Make a bokeh empty canvas with defined properties.
    """

    # constants
    # date format of x-axis
    format = "%b %d"

    if hover:
        TOOLTIPS = [
            ("Count", "$y{i}"),
        ]
    else:
        TOOLTIPS = None

    plot_options = dict(
        width=WIDTH,
        plot_height=HEIGHT,
        x_axis_type="datetime",
        active_drag=None,
        sizing_mode="scale_width",
    )

    # set to log y-axis if needed
    if logscale:
        plot_options["y_axis_type"] = "log"

    # set name if needed
    if name:
        plot_options["name"] = name

    plot = figure(
        x_axis_label=xlabel, y_axis_label=ylabel, tooltips=TOOLTIPS, **plot_options,
    )

    plot.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    return plot


def bokeh_lin_log_tabs(tab1, tab2):
    """ Create linar and logarithmic tabs from two plots.
    """

    tab1 = Panel(child=tab1, title="Linear")
    tab2 = Panel(child=tab2, title="Logarithmic")

    return Tabs(tabs=[tab1, tab2])


def countries(countries, title=None, debug=False):
    """ Plot data with Bokeh.

        Make four graphs: logscale cumulative cases, new cases,
        cumulative deaths, new deaths. Save bokeh output into html file.

        return: bokeh plots as a column
    """

    # count confirmed cases
    count, dates = extract.get_countries(countries, data.confirmed)
    new_cases = count - numpy.insert(count, 0, 0)[:-1]
    dates = pandas.to_datetime(dates)

    # count recovered cases
    count_r, dates_r = extract.get_countries(countries, data.recovered)
    new_cases_r = count_r - numpy.insert(count_r, 0, 0)[:-1]
    dates = pandas.to_datetime(dates_r)

    # count death cases
    count_d, dates_d = extract.get_countries(countries, data.death)
    new_cases_d = count_d - numpy.insert(count_d, 0, 0)[:-1]
    dates = pandas.to_datetime(dates_d)

    if count.any() == 0:
        print("Data set empty. Probably you misspelled country name.")
        return

    # calculate death rate
    death_rate = count_d[-1] / count[-1] * 100.0

    # make death rate label
    death_rate_label = Label(
        x=10,
        y=HEIGHT * 0.75,
        x_units="screen",
        y_units="screen",
        text="Death Rate: %3.1f" % death_rate,
        text_font_size="10pt",
        background_fill_color="white",
        background_fill_alpha=1.0,
    )

    # create linear tab for cases
    tab1 = bokeh_canvas("Date", "Cumulative Cases", hover=True, name="Lin")
    boheh_add_line(tab1, dates, count, legend="Confirmed", color="red")
    boheh_add_line(tab1, dates, count_r, legend="Recovered", color="green")
    boheh_add_line(tab1, dates, count_d, legend="Died", color="black")

    # create log tab for cases
    tab2 = bokeh_canvas(
        "Date", "Cumulative Cases", logscale=True, hover=True, name="Log"
    )
    boheh_add_line(tab2, dates, count, legend="Confirmed", color="red")
    boheh_add_line(tab2, dates, count_r, legend="Recovered", color="green")
    boheh_add_line(tab2, dates, count_d, legend="Died", color="black")

    # make tabs cases
    plot1 = bokeh_lin_log_tabs(tab1, tab2)
    # plot1 = column(bokeh_select_scale([tab1, tab2]))

    # make new cases plot
    plot2 = bokeh_canvas("Date", "New Cases")
    boheh_add_vbars(plot2, dates, new_cases, legend="Confirmed", color="red")
    boheh_add_vbars(plot2, dates, new_cases_r, legend="Recovered", color="green")
    boheh_add_vbars(plot2, dates, new_cases_d, legend="Died", color="black")

    # create linear tab for deaths
    tab1 = bokeh_canvas("Date", "Cumulative Deaths", hover=True)
    boheh_add_line(tab1, dates, count_d, color="black")

    # create log tab for cases
    tab2 = bokeh_canvas("Date", "Cumulative Deaths", logscale=True, hover=True)
    boheh_add_line(tab2, dates, count_d, color="black")

    # add death label
    tab1.add_layout(death_rate_label)
    tab2.add_layout(death_rate_label)

    # make tabs deaths
    plot3 = bokeh_lin_log_tabs(tab1, tab2)

    # make new cases plot
    plot4 = bokeh_canvas("Date", "New Deaths")
    boheh_add_vbars(plot4, dates, new_cases_d, color="black")

    # put plots into a column
    plots = column(plot1, plot2, plot3, plot4, sizing_mode="scale_width")
    # plots = column(plot1, plot2, sizing_mode="scale_width")

    # title for html file
    title = "<h2>" + title + "</h2>"
    title = Div(text=title)

    # save output to html file
    output_file(constants.FILE_BOKEH)
    save(column(title, plots))

    return plots


def embed(figures):
    script, div = components(figures)

    with open(constants.FILE_BOKEH_EMBED, "w") as f:
        f.write(div)
        f.write(script)
