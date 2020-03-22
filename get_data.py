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

def get_2019_data(url, team):
    '''
    Get data from each team and each URL
    The data on the site is divided by Teams
    '''
    print('- Getting data for {} team'.format(team))
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
    print('    Done. Output size: {}'.format(df_rat.shape))
    return df_rat


def get_2018_data(url, team):
    '''
    Get data from each team and each URL
    The data on the site is divided by Teams
    '''
    print('- Getting data for {} team'.format(team))
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
                           'height': heights,'all_star': all_stars,
                           'injured': injury, 'two_way': two_ways, 'rookie': rookies,
                           'rating': ratings})
    df_rat['brand'] = np.nan
    df_rat['game'] = '2K18'
    print('    Done. Output size: {}'.format(df_rat.shape))
    return df_rat


def combine_df(url_teams, dict_team_url, scrapper_function):
    '''
    Combine the datasets obtained from each iteration of get_data
    '''
    print('- Getting players 2K data') #TODO add season info
    df_list = []
    for url in url_teams:
        df = scrapper_function(url, dict_team_url[url])
        df_list.append(df)
    combined_df = pd.concat(df_list)
    print('    Done. Output size: {}'.format(combined_df.shape))
    return combined_df


def get_stats(url):

    # get contents
    soup = get_soup(url)
    print('- Getting stats data') #TODO add season info and advanced or normal stats in print
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
    print('    Done. Output size:{}'.format(stats_df.shape))
    return stats_df

def save_as_csv(df, name):
    '''
    Saves a file to .csv in local
    '''
    df.to_csv(name, index=False)
    print('File {} correctly saved as .csv'.format(name))
