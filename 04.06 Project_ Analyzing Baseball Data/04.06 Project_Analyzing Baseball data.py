##04.06 Project_Analyzing Baseball data.py
"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
##
## Provided code from Week 3 Project
##

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a LIST of ORDERED dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values (as a tuple) for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a DICTIONARY of ORDERED dictionaries where the outer dictionary
      maps the value in the key_field column to the corresponding row in the
      CSV file.  The inner Ordered dictionaries map the field names to the
      field values (as a tuple) for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

##
## Provided formulas for common batting statistics
##

# Typical cutoff used for official statistics
MINIMUM_AB = 500

def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0

def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0

def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """

    batting_year = list(filter(lambda dict:int(dict[yearid])==year, statistics))
    return batting_year



def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    answer = []
    for row in statistics:
        #the argument for "formula" passed can be used directly to call
        #the function of the same name without any special handling.
        result = formula(info, row)
        answer.append((row[info["playerid"]], result))

    #key = lambda sorts on the second tuple element
    answer.sort(key=lambda pair: pair[1], reverse=True)
    return answer[0:numplayers]


def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    answer = []
    master = read_csv_as_nested_dict(info["masterfile"], \
                                     info["playerid"], info["separator"], info["quote"])
    for name_id, stat in top_ids_and_stats:
        first_name = master[name_id][info["firstname"]]
        last_name =  master[name_id][info["lastname"]]
        answer.append("{:.3f} --- {} {}".format(stat, first_name, last_name))
    return answer


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """
    stats_full = read_csv_as_list_dict(info["battingfile"],\
                                       info["separator"], info["quote"])
    stats_year = filter_by_year(stats_full, year, info["yearid"])
    top_names = top_player_ids(info, stats_year, formula, numplayers)
    answer = lookup_player_names(info, top_names)

    return answer


##
## Part 2: Functions to compute top batting statistics by career
##

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
    aggr_dict = {}
    for row in statistics:
        if row[playerid] not in aggr_dict:
            aggr_dict[row[playerid]] = {field:int(row[field]) for field in fields}
            aggr_dict[row[playerid]][playerid]=row[playerid]
            #~ print(aggr_dict)
        else:
            for field in fields:
                aggr_dict[row[playerid]][field]= aggr_dict[row[playerid]][field] +\
                int(row[field])

    return aggr_dict


#~ print(aggregate_by_player_id([{'stat1': '3', 'stat3': '5', 'player': '1', 'stat2': '4'},
#~ {'stat1': '2', 'stat3': '8', 'player': '1', 'stat2': '1'},
#~ {'stat1': '5', 'stat3': '4', 'player': '1', 'stat2': '7'}],
#~ 'player', ['stat1', 'stat2', 'stat3']))

def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
    stats_full = read_csv_as_list_dict(info["battingfile"],\
                                       info["separator"], info["quote"])

    aggr_stats = aggregate_by_player_id(stats_full, info['playerid'], info["battingfields"])

    aggr_stats_list = list(aggr_stats.values())

    top_names = top_player_ids(info, aggr_stats_list, formula, numplayers)

    answer = lookup_player_names(info, top_names)

    return answer

##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

    try:
        year = int(input('Enter year between 1871 and 2016: '))
        if year < 1871 or year > 2016:
            print('Year is out of range')
            return
    except ValueError as e:
        print('Error:',e)
        return

    print("Top 5 batting averages in", year)
    top_batting_average = compute_top_stats_year(baseballdatainfo, batting_average, 5, year)
    for player in top_batting_average:
        print(player)
    print("")

    print("Top 10 batting averages in", year)
    top_batting_average = compute_top_stats_year(baseballdatainfo, batting_average, 10, year)
    for player in top_batting_average:
        print(player)
    print("")

    print("Top 10 on-base percentage in", year)
    top_onbase = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, year)
    for player in top_onbase:
        print(player)
    print("")

    print("Top 10 slugging percentage in", year)
    top_slugging = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, year)
    for player in top_slugging:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in", year)
    top_ops = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, year)
    for player in top_ops:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")


# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

test_baseball_statistics()
