# anoroc

Get the corona csv data from: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

Download and plot confirmed, recovered cases and deaths data.

## Usage

Plot world data.

`python anoroc.py`

Plot one country data.

`python anoroc.py -c Italy`

Plot data for wider region. You can choose from: Africa, Asia, Europe, North America, Oceania, South America, World.

`python anoroc.py -r Asia`

You can exclude country from the data by using -e flag.

`python anoroc.py -r World -e China`

`python anoroc.py -r Europe -e Italy`


If you want to re-download and update the data use -u flag.

`python anoroc.py -u`

`python anoroc.py -u -c Italy`

The output is the bokeh.html file, which you can open in a browser.

## TODOs

+ Add tests.
+ Improve plot functions to be able to plot multiple countries at same time.
+ Clean up bokeh plotting code.