""" Exract data from csv files """
import pandas

confirmed, death, recovered = None, None, None


def load(file_confirmed, file_death, file_recovered):
    # load the data
    confirmed = pandas.read_csv(file_confirmed)
    death = pandas.read_csv(file_death)
    recovered = pandas.read_csv(file_recovered)

    return confirmed, death, recovered
