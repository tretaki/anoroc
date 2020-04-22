""" Exract data from csv files """
import pandas

confirmed, death, recovered = None, None, None

# no recovered data for us
confirmed_us, death_us = None, None


def load(file_confirmed, file_death, file_recovered):
    # load the data
    confirmed = pandas.read_csv(file_confirmed)
    death = pandas.read_csv(file_death)
    recovered = pandas.read_csv(file_recovered)

    return confirmed, death, recovered


def load_us(file_confirmed, file_death):
    # load the data for united states
    # no data for recovered
    confirmed_us = pandas.read_csv(file_confirmed)
    death_us = pandas.read_csv(file_death)

    # change the name of Georgia to Georgia US, because of the country
    # Georgia name confilct
    confirmed_us.loc[
        confirmed_us["Province_State"] == "Georgia",
        confirmed_us.columns == "Province_State",
    ] = "Georgia US"
    death_us.loc[
        death_us["Province_State"] == "Georgia", death_us.columns == "Province_State",
    ] = "Georgia US"

    return confirmed_us, death_us


def merge_global_and_us_data(confirmed, death, confirmed_us, death_us):
    # merge data for us and global into common data frame

    # clean data form us data frame
    confirmed_us = confirmed_us.drop(
        ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Combined_Key"], axis=1
    )

    death_us = death_us.drop(
        [
            "UID",
            "iso2",
            "iso3",
            "code3",
            "FIPS",
            "Admin2",
            "Combined_Key",
            "Population",
        ],
        axis=1,
    )

    confirmed_us.rename(
        columns={
            "Long_": "Long",
            "Province_State": "Province/State",
            "Country_Region": "Country/Region",
        },
        inplace=True,
    )
    death_us.rename(
        columns={
            "Long_": "Long",
            "Province_State": "Province/State",
            "Country_Region": "Country/Region",
        },
        inplace=True,
    )

    # swap columns
    confirmed_us["Country/Region"] = confirmed_us["Province/State"]
    confirmed_us["Province/State"] = "US States"

    death_us["Country/Region"] = death_us["Province/State"]
    death_us["Province/State"] = "US States"

    # check if column names are the same for dataframes to be merged
    if list(confirmed)[:5] == list(confirmed_us)[:5]:
        confirmed = pandas.concat([confirmed, confirmed_us])
    else:
        print("The data for global and US cannot be merged. Returning global data.")

    if list(confirmed)[:5] == list(confirmed_us)[:5]:
        death = pandas.concat([death, death_us])
    else:
        print("The data for global and US cannot be merged. Returning global data.")

    return confirmed, death
