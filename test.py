
from get_data import get_teams_dict, get_soup, get_data, combine_df, get_stats, save_as_csv
import pandas as pd
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

df = pd.merge(ratings, stats, how='inner', left_on="name", right_on="Player").drop('Player', axis = 1) # inner join


save_as_csv(df, "2019_ratings_stats.csv")

print(df.head().T)

