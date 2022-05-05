#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# This script parses weather data from an FZJ inside website

import requests
from bs4 import BeautifulSoup


# Python module to execute

def get_weather_data():
    url = "https://www.fz-juelich.de/gs/DE/UeberUns" \
          "/Organisation/S-U/Meteorologie/wetter/wd402_node.html"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    weather_dict = make_weather_dict(url, soup)  # {header: data}

    # configures arg-dependent states of other arguments
    # (such as --inverse in inverts every args boolean status)
    config_args(args)

    if args.order is None:
        ret = value_to_string(args, weather_dict, r)
        return ret
    else:
        ret = value_to_string_order(args, weather_dict, r, args.order)
        return ret


def make_weather_dict(url, soup):
    # Parses the table containing the needed information to get all table rows.
    weather_tablerows = soup.table.find_all("tr")

    # Creates a dictionary with headers as keys and data as values
    # (i.e. Luftdruck: 1016.6 hPa).
    # `.replace(u'\xa0', u' ')` replaces parsing errors with whitespaces
    weather_data = {
        "source": url,
        "title": soup.title.get_text(strip=True),
        "date": soup.u.get_text(strip=True)
    }

    for row in weather_tablerows:
        weather_td = row.find_all("td")  # td, table data

        weather_data[weather_td[0].get_text(strip=True).replace(u'\xa0', u' ')] \
            = weather_td[1].get_text(strip=True).replace(u'\xa0', u' ')

    return weather_data


if __name__ == "__main__":
    ret = get_weather_data()
    print(ret, end='')
