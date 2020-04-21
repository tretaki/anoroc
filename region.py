""" Extract countries for a region """
# Get the countries in continents from countries.yaml
import yaml
import extract
import constants

with open(constants.FILE_COUNTRIES_LIST, "r") as file:
    countries = yaml.load(file, Loader=yaml.FullLoader)


def get(region_name, countries, data, exclude=[]):
    """ Makes a list of countries in the region.

    Parameters
    ----------
    region_name : string
        Choose one of the continents (e.g. "Asia") or "World".
    countries : dictionary
        List of countries under certain continent, from countries.yaml.
    data : numpy array
        All data loaded from the csv file.
    exclude: list
        List of countries you want to exclude.

    Returns
    -------
    region_name: string
        Region name. If some countries are excluded that is written in the name.
    region: list
        Returns the countries in the region.
    """

    continents = list(countries.keys()) + ["World"]

    if region_name not in continents:
        print(
            "Region name not valid. Choose from: \nAfrica, Asia, Europe, North America, Oceania, South America"
        )
        return None, None

    region = []

    # make the list of countries on certain continent or whole world
    for country in data["Country/Region"]:
        if region_name == "World":
            region.append(country)
        elif country in countries[region_name]:
            region.append(country)

    # deduplicate the list with multiple entries for the same country
    region = list(set(region))

    # remove excluded countries from the list
    if type(exclude) is str:
        exclude = [
            exclude,
        ]

    excluded = []
    for ex in exclude:
        if ex in region:
            excluded.append(ex)
            region.remove(ex)

    return region, excluded


def max_countries(region, data, number=3):
    """ Returns the 3 (number) countries with most cases in the region.

    Parameters
    ----------
    region : list
        List of countries in the region.
    data : numpy array
        All data loaded from the csv file.

    Returns
    -------
    countries: list
        Returns the countries in with maximal number of cases in the region.

    """

    # not enough countries in one region
    if number > len(region):
        number = len(region)

    all_countries = {}

    for country in region:

        count = extract.get_country(country, data)

        all_countries[country] = count[0][-1]

    all_countries = sorted(all_countries, key=all_countries.get, reverse=True)

    return all_countries[:number]


def max_countries_per_capita(region, data, number=3, limit=50):
    """ Returns the 3 (number) countries with most cases per capita in the region.

    Parameters
    ----------
    region : list
        List of countries in the region.
    data : numpy array
        All data loaded from the csv file.

    Returns
    -------
    countries: list
        Returns the countries in with maximal number of cases in the region.

    """

    # not enough countries in one region
    if number > len(region):
        number = len(region)

    all_countries = {}

    for country in region:

        count = extract.get_country(country, data)

        population = extract.get_population([country], countries)

        if not population:
            continue
        if count[0][-1] < limit:
            continue

        population = population[country]

        all_countries[country] = count[0][-1] / float(population)

    all_countries = sorted(all_countries, key=all_countries.get, reverse=True)

    return all_countries[:number]


def countries_at_least(region, data, number_cases=1000):
    """ Returns the countries with as least 1000 (number_cases) in the region.

    Parameters
    ----------
    region : list
        List of countries in the region.
    data : numpy array
        All data loaded from the csv file.

    Returns
    -------
    countries: list
        Returns the countries in with maximal number of cases in the region.

    """

    all_countries = {}

    for country in region:

        count = extract.get_country(country, data)

        all_countries[country] = count[0][-1]

    # extract countries with at least number_cases of cases
    countries = {k: v for (k, v) in all_countries.items() if v > number_cases}

    # get the list sorted by the number of cases
    countries = sorted(countries, key=all_countries.get, reverse=True)

    return countries
