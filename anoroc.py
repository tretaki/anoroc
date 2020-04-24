#!/usr/bin/env python3
import wget
import os
import argparse
import constants
import plot
import data
import bokeh
import region
import extract


prog_descrip = """Pull csv corona data from github repo. Plot country cases."""

parser = argparse.ArgumentParser(description=prog_descrip)
parser.add_argument(
    "-u", "--update", action="store_true", help="Download and update the csv file."
)

parser.add_argument(
    "-c", "--country", help="Input name of the country which you want to plot."
)

parser.add_argument(
    "-r",
    "--region",
    help="Input name of the region which you want to plot. You can choose from Africa, Asia, Europe, North America, Oceania, South America, United States.",
)

parser.add_argument(
    "-e",
    "--exclude",
    help="Input name of the country which you want to be excluded from the region.",
)

args = parser.parse_args()

# update the csv data if the update flag is passed
if args.update:
    if os.path.exists(constants.FILE_CONFIRMED):
        os.remove(constants.FILE_CONFIRMED)
    if os.path.exists(constants.FILE_DEATH):
        os.remove(constants.FILE_DEATH)
    if os.path.exists(constants.FILE_RECOVERED):
        os.remove(constants.FILE_RECOVERED)
    if os.path.exists(constants.FILE_CONFIRMED_US):
        os.remove(constants.FILE_CONFIRMED_US)
    if os.path.exists(constants.FILE_DEATH_US):
        os.remove(constants.FILE_DEATH_US)

# download csv if file doesn't exist
if not os.path.exists(constants.FILE_CONFIRMED):
    print("\n\nDownloading data.")
    wget.download(constants.URL_CONFIRMED, out=constants.FILE_CONFIRMED)
if not os.path.exists(constants.FILE_DEATH):
    wget.download(constants.URL_DEATH, out=constants.FILE_DEATH)
if not os.path.exists(constants.FILE_RECOVERED):
    wget.download(constants.URL_RECOVERED, out=constants.FILE_RECOVERED)
if not os.path.exists(constants.FILE_CONFIRMED_US):
    wget.download(constants.URL_CONFIRMED_US, out=constants.FILE_CONFIRMED_US)
if not os.path.exists(constants.FILE_DEATH_US):
    wget.download(constants.URL_DEATH_US, out=constants.FILE_DEATH_US)

# load the data from csv files
data.confirmed, data.death, data.recovered = data.load(
    constants.FILE_CONFIRMED, constants.FILE_DEATH, constants.FILE_RECOVERED
)

data.confirmed_us, data.death_us = data.load_us(
    constants.FILE_CONFIRMED_US, constants.FILE_DEATH_US
)

data.confirmed, data.death = data.merge_global_and_us_data(
    data.confirmed, data.death, data.confirmed_us, data.death_us
)


if __name__ == "__main__":

    figures = None

    if args.country:
        country = args.country
        figures = plot.plot_countries([str(country)], title=country)
    elif args.region and args.exclude:
        region_name = args.region
        region, excluded = region.get(
            region_name, region.countries, data.confirmed, exclude=[str(args.exclude)]
        )
        if region and excluded:
            figures = plot.make_all_plots_region(
                region, title=region_name + " excluding " + args.exclude
            )
        elif region:
            print(args.exclude + " not in " + args.region)
            print("Plotting data for the whole region.")
            figures = plot.make_all_plots_region(region, title=region_name)
    elif args.region:
        region_name = args.region
        region, _ = region.get(region_name, region.countries, data.confirmed)
        if region:
            figures = plot.make_all_plots_region(region, title=region_name)
    elif args.update:
        count, dates = extract.get_countries(["Italy"], data.confirmed)
        last_data_point = dates[-1]
        print("\n\nFresh data downloaded. Contains data up to %s." % last_data_point)
    else:
        print("\nNo country selected. Plotting data for whole world.")
        world, _ = region.get("World", region.countries, data.confirmed)
        if world:
            figures = plot.make_all_plots_region(world, title="World", number=7)

    if figures:

        plot.embed(figures)

        # save output to html file
        bokeh.io.output_file(constants.FILE_BOKEH)
        bokeh.io.save(figures)
