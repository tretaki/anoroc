""" Exract data from csv files """
import pandas
import constants

# load the data
confirmed = pandas.read_csv(constants.FILE_CONFIRMED)
death = pandas.read_csv(constants.FILE_DEATH)
recovered = pandas.read_csv(constants.FILE_RECOVERED)
