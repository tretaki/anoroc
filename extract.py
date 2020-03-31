""" extract fuctions for anoroc """


def get_country(country, data):
    """ Extracts data for country.

    Parameters
    ----------
    country : string
        Name of the country.
    data : numpy array
        All data loaded from the csv file.

    Returns
    -------
    count: numpy array
        Returns the count of cases vs time.

    """

    # extract data
    count = data.loc[data["Country/Region"] == country]

    count = count.to_numpy()
    count = count[:, 4:]  # omit the first 4 columns
    count = count.sum(axis=0)  # add all data in sub-regions

    # extract dates
    dates = data.columns.to_numpy()
    dates = dates[4:]  # omit the first 4 columns

    return count, dates


def get_countries(countries, data):
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

    counts = 0
    for country in countries:
        count, dates = get_country(country, data)
        counts += count

    return counts, dates
