import os
import requests
from bs4 import BeautifulSoup
import csv
import re

import pandas as pd
import numpy as np

# TODO: modify functions to accept as input the soup instead of the url: this way, we only need to execute once the request


def get_soup(url):
    # request to the page
    page = requests.get(url)
    # extract the test
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def get_teams_dict(url):
    '''
    Gets a dictionary with the teams and their corresponding URLs for the given season
    Format: {URL: team} so that for a given URL we can extract the team's name
    TODO: maybe it doesn't have much sense to do this? Could we extract the name through the URL?
    '''
    # get contents
    soup = get_soup(url)
    # teams
    teams = soup.find("ul", {"class": "list-group"})

    url_teams = []
    team_list = []

    for team in teams.find_all('li'):
        url_teams.append(team.a['href'])
        team_list.append(team.a.text)
    # create the dictionary with the lists of teams and urls
    dict_team_url = {url_teams[i]: team_list[i]
                     for i in range(0, len(team_list))}

    return dict_team_url


# modify the function to add the results to an existing df

def get_data(url, team):
    '''
    Get data from each team and each URL
    The data on the site is divided by Teams
    '''
    # define empty dictionary
    names, positions, heights, brands, injury, two_ways, all_stars, rookies, ratings = (
        [] for i in range(9))

    # get contents
    soup = get_soup(url)

    # get the data for each player in the table

    # table containing all players
    table = soup.find("tbody")

    for player in table.find_all("tr"):

        # name of the player
        name = player.find_all("td")[1].a.text
        names.append(name)

        # pos
        pos = player.find_all("td")[3].text
        positions.append(pos)

        # rating
        rating = player.find_all("td")[2].span.text
        ratings.append(rating)

        # height
        height = player.find_all("td")[4].text
        heights.append(height)

        # brand
        brand = player.find_all("td")[5].text
        brands.append(brand)

        # check if all star
        if len(player.find_all("td")[1].find_all("i", {"class": "fa fa-star"})) > 0:
            all_star = 1
        else:
            all_star = 0
        all_stars.append(all_star)

        # check if injured
        if len(player.find_all("td")[1].find_all("i", {"class": "fa fa-plus-circle"})) > 0:
            injured = 1
        else:
            injured = 0
        injury.append(injured)

        # check if two-way
        if len(player.find_all("td")[1].find_all("i", {"class": "fa fa-arrows-h"})) > 0:
            two_way = 1
        else:
            two_way = 0
        two_ways.append(two_way)

        # check if rookie
        if len(player.find_all("td")[1].find_all("small")) == 1:
            rookie = 1
        else:
            rookie = 0
        rookies.append(rookie)

    teams = [team for i in range(len(names))]
    df_rat = pd.DataFrame({'name': names, 'team': teams, 'position': positions,
                           'height': heights, 'brand': brands, 'all_star': all_stars,
                           'injured': injury, 'two_way': two_ways, 'rookie': rookies,
                           'rating': ratings})
    return df_rat


def combine_df(url_teams, dict_team_url):
    '''
    Combine the datasets obtained from each iteration of get_data
    '''

    df_list = []
    for url in url_teams:
        df = get_data(url, dict_team_url[url])
        df_list.append(df)
    combined_df = pd.concat(df_list)
    return combined_df


def get_stats(url):

    # get contents
    soup = get_soup(url)

    col_names = []
    for i in range(1, len(soup.tbody.find_all('tr')[1].find_all('td'))+1):
        col_names.append(soup.thead.find_all(
            'th')[i].text.replace('%', '.pct'))

    players = soup.tbody.find_all('tr')
    stats_df = pd.DataFrame(
        np.zeros((0, len(soup.tbody.find_all('tr')[1].find_all('td')))))

    # loop through the players
    for player in players:

        if player['class'] != ['thead']:

            # create list for every player
            player_as_list = []

            # loop through the player's stats
            for col in range(0, len(soup.tbody.find_all('tr')[1].find_all('td'))):
                player_as_list.append(player.find_all('td')[col].text)

            # obtain dataframe
            df = pd.DataFrame(player_as_list)
            # append to the whole dataframe; transposed
            stats_df = stats_df.append(df.T)

    # modify column names and index
    stats_df.columns = col_names
    stats_df.index = np.arange(len(stats_df))

    # change blank spaces for NAs:
    stats_df = stats_df.replace(r'^\s*$', np.nan, regex=True)

    return stats_df


# ## Ratings ----------
# start getting  list of the url where we can obtain all the data: one URL per team
url = 'https://nba2k19.2kratings.com/current-teams-on-nba-2k19'
teams_dict = get_teams_dict(url)
ratings = combine_df(teams_dict, teams_dict)

# # Creamos el fichero
# ratings.to_csv("2k19_ratings.csv", index=False)


# Stats for 17-18 season --------
# normal
stats_1718 = get_stats(
    'https://www.basketball-reference.com/leagues/NBA_2018_per_game.html')
# advanced
stats_1718_adv = get_stats('https://www.basketball-reference.com/leagues/NBA_2018_advanced.html')


# merge
complete_stats_1718 = pd.merge(stats_1718, stats_1718_adv, how='inner', on=["Player", 'Pos', 'Age', 'Tm', 'G'])

complete_stats_1718.columns = ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MPG', 'FG', 'FGA', 'FG.pct',
       '3P', '3PA', '3P.pct', '2P', '2PA', '2P.pct', 'eFG.pct', 'FT', 'FTA',
       'FT.pct', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
       'MP_Total', 'PER', 'TS.pct', '3PAr', 'FTr', 'ORB.pct', 'DRB.pct', 'TRB.pct',
       'AST.pct', 'STL.pct', 'BLK.pct', 'TOV.pct', 'USG.pct', 'empty1', 'OWS',
       'DWS', 'WS', 'WS/48', 'empty2', 'OBPM', 'DBPM', 'BPM', 'VORP']
# drop columns with NA created with the scraping part
stats  = complete_stats_1718.drop(['empty1', 'empty2'], axis = 1)

# stats.to_csv("2k19_ratings.csv", index=False)

df = pd.merge(ratings, stats, how='inner', left_on="name", right_on="Player").drop('Player', axis = 1) # inner join: less results but easier to clean


df.to_csv("2019_ratings_stats.csv", index=False)
