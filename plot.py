""" plotting fuctions for anoroc """
import numpy
import pandas
import extract
import data
import region
import constants
from bokeh.io import output_file, save
from bokeh.models import (
    Panel,
    Tabs,
    DatetimeTickFormatter,
    Div,
    HoverTool,
    Label,
    ColumnDataSource,
    Select,
    CustomJS,
    RadioButtonGroup,
)
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import brewer, d3

WIDTH = 700
HEIGHT = 350


def bokeh_vstack_bar_region(
    figure, max, xdata, count_all, data_all, color="black", alpha=0.5
):

    """ Creates a vstack plot on a bokeh canvas.
    """

    # constants
    bar_width = 50000000  # with the datetime axis, the width is defined in seconds
    legend_location = "top_left"

    # data for producing vstack plot
    data_vstack = {}
    data_vstack["Dates"] = xdata

    # rest of countries
    rest = count_all.copy()

    # create data sources
    for country in max:
        count_country, dates = extract.get_countries([country], data_all)
        new_country = count_country - numpy.insert(count_country, 0, 0)[:-1]
        data_vstack[country] = new_country

        # subtract country data form the rest
        rest -= new_country

    data_vstack["Others"] = rest

    stacks = max.copy()
    stacks.append("Others")

    figure.vbar_stack(
        stackers=stacks,
        x="Dates",
        color=brewer["Spectral"][len(stacks)],
        legend_label=stacks,
        source=data_vstack,
        width=bar_width,
        line_color=color,
        line_width=0.5,
    )

    figure.legend.items.reverse()
    figure.legend.location = legend_location


def bokeh_vstack_area_region(
    figure, max, xdata, count_all, data_all, color="black", alpha=0.5
):

    """ Creates a vstack plot on a bokeh canvas.
    """

    # data for producing vstack plot
    data_vstack = {}
    data_vstack["Dates"] = xdata

    # rest of countries
    rest = count_all.copy()

    # create data sources
    for country in max:
        count_country, dates = extract.get_countries([country], data_all)
        data_vstack[country] = count_country

        # subtract country data form the rest
        rest -= count_country

    data_vstack["Others"] = rest

    stacks = max.copy()
    stacks.append("Others")

    figure.varea_stack(
        stackers=stacks,
        x="Dates",
        color=brewer["Spectral"][len(stacks)],
        legend_label=stacks,
        source=data_vstack,
    )

    figure.vline_stack(
        stackers=stacks, x="Dates", source=data_vstack, color=color, alpha=alpha
    )

    figure.legend.items.reverse()
    figure.legend.location = "top_left"


def boheh_add_line(
    figure, xdata, ydata, name="Count", legend=True, color="red", alpha=0.7
):
    """ Adds dataset as line points to the bokeh figure.
    """

    # constants
    line_width = 3
    legend_location = "top_left"

    data = {"Dates": xdata, name: ydata}
    source = ColumnDataSource(data)

    # add line
    figure.line(
        "Dates",
        name,
        source=source,
        line_width=line_width,
        color=color,
        name=name,
        alpha=alpha,
        legend_label=name,
    )

    if legend:
        figure.legend.location = legend_location


def boheh_add_line_points(
    figure, xdata, ydata, name="Count", legend=True, color="red", alpha=0.7
):
    """ Adds dataset as line points to the bokeh figure.
    """

    # constants
    line_width = 3
    point_size = 7
    legend_location = "top_left"

    data = {"Dates": xdata, name: ydata}
    source = ColumnDataSource(data)

    # add line
    figure.line(
        "Dates",
        name,
        source=source,
        line_width=line_width,
        color=color,
        alpha=alpha,
        name=name,
    )

    # add points
    properties = dict(size=point_size, color=color, fill_color="white", name=name)
    if legend:
        properties["legend_label"] = name

    figure.circle("Dates", name, source=source, **properties)

    if legend:
        figure.legend.location = legend_location


def boheh_add_vbars(
    figure, xdata, ydata, name="Count", legend=True, color="red", alpha=0.7
):
    """ Adds dataset as vertical bars to the bokeh figure.
    """

    # constants
    bar_width = 50000000  # with the datetime axis, the width is defined in seconds
    legend_location = "top_left"

    # data
    data = {"Dates": xdata, name: ydata}
    source = ColumnDataSource(data)

    # add bars
    properties = dict(
        width=bar_width, color=color, alpha=alpha, name=name, source=source,
    )
    if legend:
        properties["legend_label"] = name
    figure.vbar(x="Dates", top=name, bottom=0, **properties)

    if legend:
        figure.legend.location = legend_location


def bokeh_canvas(xlabel, ylabel, logscale=False, hover=False):
    """ Make a bokeh empty canvas with defined properties.
    """

    # constants

    # date format of x-axis
    format = "%b %d"

    # add hover
    if hover:
        TOOLTIPS = "$name: @$name{i}"
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

    plot = figure(
        x_axis_label=xlabel, y_axis_label=ylabel, tooltips=TOOLTIPS, **plot_options,
    )

    plot.xaxis.formatter = DatetimeTickFormatter(
        days=[format], months=[format], years=[format],
    )

    return plot


def bokeh_lin_log_tabs(tab1, tab2, name=None):
    """ Create linar and logarithmic tabs from two plots.
    """

    tab1 = Panel(child=tab1, title="Linear")
    tab2 = Panel(child=tab2, title="Logarithmic")

    return Tabs(tabs=[tab1, tab2], name=name)


def toggle_lin_log_scale(fig1, fig2):

    figs = [fig1, fig2]

    fig2.visible = False

    toggle = RadioButtonGroup(
        labels=["Linear", "Logarithmic"], width=120, height=30, active=0
    )

    callback = CustomJS(
        args=dict(figs=figs),
        code="""
        let active = cb_obj.active;
        
        if (cb_obj.active == 1){
            figs[0].visible = false;
            figs[1].visible = true;
        }
        else{
            figs[0].visible = true;
            figs[1].visible = false;
        }
    """,
    )

    toggle.js_on_click(callback)

    return column([toggle] + figs)


def select_figure(figs, title="Select Country"):
    names = [fig.name for fig in figs]
    selector = Select(
        title=title,
        value=names[0],
        options=names,
        width=300,
        height=50,
        sizing_mode="fixed",
    )

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

    selector.js_on_change("value", callback)

    return [selector] + figs


def create_countries_selector(countries):

    plots = []

    for country in countries:
        plot = plot_countries([country])
        plot.name = country
        plots.append(plot)

    return column(select_figure(plots), sizing_mode="stretch_width")


def plot_countries(countries, title=None):
    """ Plot countries data with Bokeh.

        Make four graphs: logscale cumulative cases, new cases,
        cumulative deaths, new deaths. Save bokeh output into html file.

        Paremeters
        ----------
        countries: list
            List of country names.
        title: string
            Title of the plot.
        
        Returns
        -------
        plots: bokeh plots as a column
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

    # calculate deaths per capita
    population = sum(extract.get_population(countries, region.countries).values())
    death_per_capita = count_d[-1] / float(population) * 1e6

    # make death rate label and per capita label
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
    death_per_capita_label = Label(
        x=10,
        y=HEIGHT * 0.70,
        x_units="screen",
        y_units="screen",
        text="Deaths per million: %3.1f" % death_per_capita,
        text_font_size="10pt",
        background_fill_color="white",
        background_fill_alpha=1.0,
    )

    # create linear tab for cases
    tab1 = bokeh_canvas(None, "Cumulative Cases", hover=True)
    boheh_add_line_points(tab1, dates, count, name="Confirmed", color="red")
    boheh_add_line_points(tab1, dates, count_r, name="Recovered", color="green")
    boheh_add_line_points(tab1, dates, count_d, name="Died", color="black")

    # create log tab for cases
    tab2 = bokeh_canvas(None, "Cumulative Cases", logscale=True, hover=True)
    boheh_add_line_points(tab2, dates, count, name="Confirmed", color="red")
    boheh_add_line_points(tab2, dates, count_r, name="Recovered", color="green")
    boheh_add_line_points(tab2, dates, count_d, name="Died", color="black")

    # make tabs cases
    plot1 = toggle_lin_log_scale(tab1, tab2)

    # make new cases plot
    plot2 = bokeh_canvas(None, "New Cases", hover=True)
    boheh_add_vbars(plot2, dates, new_cases, name="Confirmed", color="red")
    boheh_add_vbars(plot2, dates, new_cases_r, name="Recovered", color="green")
    boheh_add_vbars(plot2, dates, new_cases_d, name="Died", color="black")

    # create linear tab for deaths
    tab1 = bokeh_canvas(None, "Cumulative Deaths", hover=True)
    boheh_add_line_points(
        tab1, dates, count_d, name="Died", legend=False, color="black"
    )

    # create log tab for cases
    tab2 = bokeh_canvas(None, "Cumulative Deaths", logscale=True, hover=True)
    boheh_add_line_points(
        tab2, dates, count_d, name="Died", legend=False, color="black"
    )

    # add death label
    tab1.add_layout(death_rate_label)
    tab2.add_layout(death_rate_label)
    # add death per capita label
    tab1.add_layout(death_per_capita_label)
    tab2.add_layout(death_per_capita_label)

    # make tabs deaths
    plot3 = toggle_lin_log_scale(tab1, tab2)

    # make new cases plot
    plot4 = bokeh_canvas(None, "New Deaths", hover=True)
    boheh_add_vbars(plot4, dates, new_cases_d, name="Died", legend=False, color="black")

    # title for html file
    if title:
        title = "<p>" + title + "</p>"
        title = Div(text=title)

    # put plots into a column
    plots = column(plot1, plot2, plot3, plot4, sizing_mode="scale_width")

    return plots


def plot_region_stacks(countries_all, title=None, number=3):
    """ Plot region data with Bokeh.

        Make four graphs: cumulative cases (with max countries),
        cumulative deaths (with max countries). Save bokeh output into html file.

        Paremeters
        ----------
        countries_all : list
        List of all countries in the region. 
        title: string
            Title of the plot.
        
        Returns
        -------
        plots: bokeh plots as a column
    """

    # count confirmed cases
    count_c, dates = extract.get_countries(countries_all, data.confirmed)
    new_cases_c = count_c - numpy.insert(count_c, 0, 0)[:-1]
    dates = pandas.to_datetime(dates)

    # check if dataset empty
    if count_c.any() == 0:
        print("Data set empty. Probably you misspelled country name.")
        return

    # count death cases
    count_d, dates_d = extract.get_countries(countries_all, data.death)
    new_cases_d = count_d - numpy.insert(count_d, 0, 0)[:-1]
    dates = pandas.to_datetime(dates_d)

    # get max countries (cuntries with max cases)
    max_confirmed = region.max_countries(countries_all, data.confirmed, number=number)
    max_deaths = region.max_countries(countries_all, data.death, number=number)

    # plot confirmed
    plot1 = bokeh_canvas(None, "Cumulative Confirmed Cases", hover=True)
    bokeh_vstack_area_region(plot1, max_confirmed, dates, count_c, data.confirmed)

    # plot new confirmed
    plot2 = bokeh_canvas(None, "New Confirmed Cases", hover=True)
    bokeh_vstack_bar_region(plot2, max_confirmed, dates, new_cases_c, data.confirmed)

    # plot deaths
    plot3 = bokeh_canvas(None, "Cumulative Deaths", hover=True)
    bokeh_vstack_area_region(plot3, max_deaths, dates, count_d, data.death)

    # plot new deaths
    plot4 = bokeh_canvas(None, "New Deaths", hover=True)
    bokeh_vstack_bar_region(plot4, max_deaths, dates, new_cases_d, data.death)

    plots_per_capita = plot_per_capita(countries_all)

    # title for html file
    if title:
        title = "<h3>" + title + "</h3>"
        title = Div(text=title)

    # put plots into a column
    plots = column(
        plots_per_capita, plot1, plot2, plot3, plot4, sizing_mode="scale_width"
    )

    return plots


def data_countries_per_capita(countries):
    """ Extract per capita data for a country or list of countries.
        Data is given per milion people.

        Produce data: cumulative cases, cumulative deaths per capita.

        Paremeters
        ----------
        countries : list
        List of country names.
        
        Returns
        -------
        cases_per_capita: numpy array
        deths_per_capita: numpy array
        dates: numpy array
    """

    # count confirmed cases
    count_c, dates = extract.get_countries(countries, data.confirmed)
    dates = pandas.to_datetime(dates)

    # count death cases
    count_d, dates_d = extract.get_countries(countries, data.death)

    countries_population = extract.get_population(countries, region.countries)

    total_population = sum(countries_population.values())

    cases_per_capita = count_c / float(total_population) * 1e6
    deaths_per_capita = count_d / float(total_population) * 1e6

    return cases_per_capita, deaths_per_capita, dates


def plot_per_capita(countries_all, title=None):
    """ Plot per capita cases with bokeh.

        Make two graphs: cumulative cases, cumulative deaths per capita.

        Paremeters
        ----------
        countries_all : list
        List of all countries you wanna plot.
        title: string
            Title of the plot.
        
        Returns
        -------
        plots: bokeh plots as a column
    """

    # plot for cases
    plot1 = bokeh_canvas(None, "Confirmed Cases per million Inhabitants", hover=True)

    # plot for deaths
    plot2 = bokeh_canvas(None, "Deaths per million Inhabitants", hover=True)

    # fix hover tool to show decimals
    hover = plot1.select(dict(type=HoverTool))
    TOOLTIPS = "$name: @$name{4.1f}"
    hover.tooltips = TOOLTIPS
    hover = plot2.select(dict(type=HoverTool))
    hover.tooltips = TOOLTIPS

    colors = d3["Category20"][20]

    # take only first 13 countries
    countries_all_c = region.max_countries_per_capita(
        countries_all, data.confirmed, number=13, limit=1000,
    )

    for country, color in zip(countries_all_c, colors):
        # get the data
        cases_per_capita, deaths_per_capita, dates = data_countries_per_capita(
            [country]
        )

        boheh_add_line(
            plot1, dates, cases_per_capita, name=country, color=color, alpha=1.0
        )

    # take only first 13 countries
    countries_all_d = region.max_countries_per_capita(
        countries_all, data.death, number=13, limit=100
    )

    for country, color in zip(countries_all_d, colors):
        # get the data
        cases_per_capita, deaths_per_capita, dates = data_countries_per_capita(
            [country]
        )

        boheh_add_line(
            plot2, dates, deaths_per_capita, name=country, color=color, alpha=1.0
        )

    plots = column(plot1, plot2, sizing_mode="scale_width")

    return plots


def make_all_plots_region(countries_all, title=None, number=3):

    plots_detailed = plot_countries(countries_all, title=title)

    title_stacks = "Contribution of Individual Countries"

    plots_stacks = plot_region_stacks(countries_all, title=title_stacks, number=number)

    selector_countries = region.countries_at_least(countries_all, data.confirmed)

    plots_selectors = create_countries_selector(selector_countries)

    return plots_detailed, plots_stacks, plots_selectors


def embed(figures):

    if type(figures) == tuple and len(figures) == 3:

        script, div = components(figures[0])

        with open(constants.FILE_BOKEH_EMBED_DETAILS, "w") as f:
            f.write(div)
            f.write(script)

        script, div = components(figures[1])

        with open(constants.FILE_BOKEH_EMBED_STACKS, "w") as f:
            f.write(div)
            f.write(script)

        script, div = components(figures[2])

        with open(constants.FILE_BOKEH_EMBED_SELECTORS, "w") as f:
            f.write(div)
            f.write(script)
