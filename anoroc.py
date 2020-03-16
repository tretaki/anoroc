#!/usr/bin/env python3
import wget
import os
import pandas
import numpy
import matplotlib.pyplot as plt
import argparse


prog_descrip = """Pull csv corona data from github repo. Plot country cases."""

parser = argparse.ArgumentParser(description=prog_descrip)
parser.add_argument(
    "-u", "--update", action="store_true", help="Download and update the csv file."
)

parser.add_argument(
    "-c", "--country", help="Input name of the country which you want to plot."
)

args = parser.parse_args()

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

filename = "cases_data.csv"

# update the csv data if the update flag is passed
if args.update:
    if os.path.exists(filename):
        os.remove(filename)

# download csv if file doesn't exist
if not os.path.exists(filename):
    filename = wget.download(url, out=filename)

# load the data
data = pandas.read_csv(filename)

# get the column names from data frame
cols = data.columns.to_numpy()
dates = cols[4:]


def extract_country(country, data, exclude=False):
    """ Extracts data for country.

    Parameters
    ----------
    country : string
        Name of the country.
    data : numpy array
        All data loaded from the csv file.
    exclude: boolean
        If True it excludes this country from the data.

    Returns
    -------
    count: numpy array
        Returns the count of cases vs time.

    """

    if country == "all":
        result = data
    else:
        if exclude:
            result = data.loc[data["Country/Region"] != country]
        else:
            result = data.loc[data["Country/Region"] == country]

    result = result.to_numpy()
    result = result[:, 4:]  # omitt the first 4 columns
    result = result.sum(axis=0)  # add all data in subregions

    return result


def extract_region(region, data):
    """ Extracts data for wider regions.

    Parameters
    ----------
    region : list
        List of strings with country names
    data : numpy array
        All data loaded from the csv file.

    Returns
    -------
    count: numpy array
        Returns the count of cases vs time.

    """

    count = 0
    for country in region:
        count += extract_country(country, data)

    return count


def plot_country(country, exclude=False):

    count = extract_country(country, data, exclude)
    new_cases = count - numpy.insert(count, 0, 0)[:-1]

    fig, ax1 = plt.subplots()
    plt.xticks(rotation=90)
    ax2 = ax1.twinx()
    ax1.plot(dates, count, "ro-")
    ax2.plot(dates, new_cases, "bo-")
    ax1.set_yscale("log")
    if exclude:
        plt.title("Excluding " + country)
    else:
        plt.title(country)

    ax1.set_ylabel("Comulative Cases", color="r")
    ax2.set_ylabel("New Cases", color="b")
    plt.show()


def plot_region(region, name=""):

    count = extract_region(region, data)
    new_cases = count - numpy.insert(count, 0, 0)[:-1]

    fig, ax1 = plt.subplots()
    plt.xticks(rotation=90)
    ax2 = ax1.twinx()
    ax1.plot(dates, count, "ro-")
    ax2.plot(dates, new_cases, "bo-")
    ax1.set_yscale("log")

    plt.title(name)

    ax1.set_ylabel("Comulative Cases", color="r")
    ax2.set_ylabel("New Cases", color="b")
    plt.show()


EU = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
]

if __name__ == "__main__":
    if args.country:
        plot_country(str(args.country))
    else:
        print("No country selected. Plotting EU instead.")
        plot_region(EU, name="EU")

