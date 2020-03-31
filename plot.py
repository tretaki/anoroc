""" plotting fuctions for anoroc """
import numpy
import matplotlib.pyplot as plt
import extract
import data


def countries(countries, title=None, debug=False):
    """ Plot data with matplotlib.

        Make four graphs: logscale cumulative cases, new cases,
        cumulative deaths, new deaths
    """

    # count confirmed cases
    count, dates = extract.get_countries(countries, data.confirmed)
    new_cases = count - numpy.insert(count, 0, 0)[:-1]

    # count death cases
    count_d, dates_d = extract.get_countries(countries, data.death)
    new_cases_d = count_d - numpy.insert(count_d, 0, 0)[:-1]

    # count recovered cases
    count_r, dates_r = extract.get_countries(countries, data.recovered)
    new_cases_r = count_r - numpy.insert(count_r, 0, 0)[:-1]

    if count.any() == 0:
        print("Data set empty. Probably you misspelled country name.")
        return

    fig, axs = plt.subplots(4, sharex=True)

    axs[0].set_title(title)

    plt.xticks(rotation=90)
    label_c = "Confirmed: %s" % count[-1]
    label_r = "Recovered: %s" % count_r[-1]
    axs[0].plot(dates, count, "ro-", label=label_c)
    axs[0].plot(dates, count_r, "go-", label=label_r)
    axs[0].set_yscale("log")
    axs[0].legend()
    axs[1].bar(dates, new_cases)
    axs[2].plot(dates_d, count_d, "ro-")
    axs[3].bar(dates_d, new_cases_d)

    axs[0].set_ylabel("Cumulative Cases\n Logscale", color="r")
    axs[1].set_ylabel("New Cases", color="b")
    axs[2].set_ylabel("Cumulative Deaths", color="r")

    death_rate = count_d[-1] / count[-1] * 100.0
    death_rate = "%3.1f" % death_rate
    label_d = "Deaths: %s\nDeath Rate: %s" % (count_d[-1], death_rate)
    axs[2].annotate(label_d, xy=(1, count_d[-1] * 0.65))

    axs[3].set_ylabel("New Deaths", color="b")

    if not debug:
        plt.show()
    else:
        return death_rate
