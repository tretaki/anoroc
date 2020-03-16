# anoroc

Get the corona csv data from: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

Plot the individual country confirmed cases data.

## Usage

python anoroc.py -c Italy

If you want to re-download and update the data use -u flag.

python anoroc.py -u -c Italy

## TODOs

+ Add tests.
+ Expand extract_region() function to be able to exclude regions.
+ Add death and recovered data.
+ Improve plot functions to be able to plot multiple countries at same time.