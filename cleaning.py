
# clean position variable
df.position = df.position.apply(lambda x: x.replace('\n', ''))

# drop b-ref position (interested in nba2k position) and rookie status (need to first fetch stats for rookies)
df = df.drop(['Pos', 'rookie'], axis = 1)

### inch to cm
# 1) str to 2 columns
def convert_row(row):
    empty_dict = {}
    # extract feet and inch for each row
    feet = int(row.height.split('\"')[0].replace('\'', ''))
    inches = int(row.height.split('\"')[1].replace('\'', ''))
    empty_dict['feet'] = feet
    empty_dict['inches'] = inches
    new_row = row.append(pd.Series(empty_dict))    
    return new_row

convert_row(df.iloc[0])

# apply to whole df
df = df.apply(lambda row: convert_row(row), axis = 1)

# 2) two columns to 1 column in cm: TODO
