#!/usr/bin/env python3
import wget
import os
import argparse
import constants
import plot
import data
import region


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
    help="Input name of the region which you want to plot. You can choose from Africa, Asia, Europe, North America, Oceania, South America.",
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

# download csv if file doesn't exist
if not os.path.exists(constants.FILE_CONFIRMED):
    print("\n\nDownloading data.")
    wget.download(constants.URL_CONFIRMED, out=constants.FILE_CONFIRMED)
if not os.path.exists(constants.FILE_DEATH):
    wget.download(constants.URL_DEATH, out=constants.FILE_DEATH)
if not os.path.exists(constants.FILE_RECOVERED):
    wget.download(constants.URL_RECOVERED, out=constants.FILE_RECOVERED)


if __name__ == "__main__":

    if args.country:
        country = args.country
        plot.countries([str(country)], title=country)
    elif args.region and args.exclude:
        region_name = args.region
        region, excluded = region.get(
            region_name, region.countries, data.confirmed, exclude=[str(args.exclude)]
        )
        if region and excluded:
            plot.countries(region, title=region_name + " excluding " + args.exclude)
        elif region:
            print(args.exclude + " not in " + args.region)
            print("Plotting data for the whole region.")
            plot.countries(region, title=region_name)
    elif args.region:
        region_name = args.region
        region, _ = region.get(region_name, region.countries, data.confirmed)
        if region:
            plot.countries(region, title=region_name)
    elif args.update:
        print("\n\nFresh data downloaded.")
    else:
        print("\nNo country selected. Plotting data for whole world.")
        world, _ = region.get("World", region.countries, data.confirmed)
        if world:
            plot.countries(world, title="World")
