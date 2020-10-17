"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    nested_dict = {}
    with open(filename, "r", newline="") as csvfile:
        csv_dict_data = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csv_dict_data:
            nested_dict[row[keyfield]] = row
    return nested_dict

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
        filename: name of csv file
        separator: charcter that separate fields
        quote: character used to optionally quote fields
    Outputs:
        Returns a list of dictionarys where the dictionary map the field names
        to the field values for that row 
    """
    list_dict = []
    with open(filename, "r", newline="") as csvfile:
        csv_dict_data = csv.DictReader(csvfile, delimiter=separator, quotechar=quote) 
        for row in csv_dict_data:
            list_dict.append(row)
    return list_dict

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    country_code_list = read_csv_as_list_dict(codeinfo["codefile"],
                                              codeinfo["separator"], codeinfo["quote"])
    code_convert_dict = {}
    for value in country_code_list:
        plot_code = value[codeinfo["plot_codes"]]
        data_code = value[codeinfo["data_codes"]]
        code_convert_dict[plot_code] = data_code
    return code_convert_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    code_reconcile_dict = {}
    unfound_code_set = set()
    convert_dict = build_country_code_converter(codeinfo)
    convert_dict_casefold = {}
    for key, value in convert_dict.items():
        convert_dict_casefold[key.casefold()] = value.casefold()
    gdp_code_case_convert = {} #map casefold data_code to original data_code
    for key in gdp_countries:
        gdp_code_case_convert[key.casefold()] = key
    for plot_code in plot_countries:
        if plot_code.casefold() in convert_dict_casefold:        
            data_code = convert_dict_casefold[plot_code.casefold()]
            if data_code in gdp_code_case_convert:
                code_reconcile_dict[plot_code] = gdp_code_case_convert[data_code]
            else:
                unfound_code_set.add(plot_code)
        else:
            unfound_code_set.add(plot_code)
    return code_reconcile_dict, unfound_code_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    code_gdp_dict = {}
    unfound_code_set = set()
    no_data_code_set = set()
    gdp_countries = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"], 
                                            gdpinfo["separator"], gdpinfo["quote"])

    convert_dict = build_country_code_converter(codeinfo)
    convert_dict_casefold = {}
    for key, value in convert_dict.items():
        convert_dict_casefold[key.casefold()] = value.casefold()
    gdp_countries_casefold = {} #map casefold data_code to gdp in year
    for key, value in gdp_countries.items():
        gdp_countries_casefold[key.casefold()] = value[year]
    for plot_code in plot_countries:
        if plot_code.casefold() in convert_dict_casefold:     
            data_code = convert_dict_casefold[plot_code.casefold()]
            if data_code not in gdp_countries_casefold:
                unfound_code_set.add(plot_code)
            else:    
                if gdp_countries_casefold[data_code] == "":
                    no_data_code_set.add(plot_code)
                else:
                    code_gdp_dict[plot_code] = math.log10(float(gdp_countries_casefold[data_code]))
        else:
            unfound_code_set.add(plot_code)
    return code_gdp_dict, unfound_code_set, no_data_code_set


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    code_gdp_dict, unfound_code_set, no_data_code_set = \
                    build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
    world_map = pygal.maps.world.World()
    world_map.title = "GDP by country for " + year + " (log scale), unified by common country name"
    world_map.add("GDP for" + year, code_gdp_dict)
    world_map.add("Missing from Worldmap", unfound_code_set)
    world_map.add("No GDP data", no_data_code_set)
    world_map.render_in_browser()



def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()
