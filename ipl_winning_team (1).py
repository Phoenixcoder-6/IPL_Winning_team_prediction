# -*- coding: utf-8 -*-
"""IPL winning team.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hWhZcc5jbELBwh3NRA9MmB5jlTUB1qrE

**Headers**
"""

import numpy as np
import pandas as pd

"""**Load datasets**"""

match = pd.read_csv('matches.csv')
delivery = pd.read_csv('deliveries.csv')

match.head()

match.shape

match.info()

# Count of null values in each column
null_counts = match.isnull().sum()
print(null_counts)

# Display only columns with null values
null_columns = null_counts[null_counts > 0]
print(null_columns)

#Visualizing Null value
import seaborn as sns
import matplotlib.pyplot as plt

# Heatmap to visualize null values
plt.figure(figsize=(10, 6))
sns.heatmap(match.isnull(), cbar=False, cmap="viridis")
plt.title("Null Values in Match Dataset")
plt.show()

# Forward fill
match = match.fillna(method='ffill')

# Backward fill
match = match.fillna(method='bfill')

null_counts = match.isnull().sum()
print(null_counts)

#NaN value Checking
# Count of NaN values in each column
nan_counts = match.isna().sum()
print(nan_counts)

# Remove duplicate rows
match = match.drop_duplicates()
match.shape

import pandas as pd
from sklearn.preprocessing import StandardScaler

# Assuming 'match' is your DataFrame
# Let's first check the initial state of the relevant columns
print("Initial Data Summary:")
print(match[[ 'win_by_runs', 'win_by_wickets']].describe())

# Initialize the StandardScaler
scaler = StandardScaler()

# Apply standardization to the specified numeric columns
match[[ 'win_by_runs', 'win_by_wickets']] = scaler.fit_transform(
    match[[ 'win_by_runs', 'win_by_wickets']]
)

# Review the standardized data
print("Standardized Data Summary:")
print(match[['win_by_runs', 'win_by_wickets']].describe())

print("Cleaned Dataset:")
print(match.head())
match.describe()

"""#For Deliveries dataset"""

delivery.head()

delivery.info()

total_score_df = delivery.groupby(['match_id','inning']).sum()['total_runs'].reset_index()

total_score_df = total_score_df[total_score_df['inning'] == 1]

total_score_df

match_df = match.merge(total_score_df[['match_id','total_runs']],left_on='id',right_on='match_id')

match_df

match_df['team1'].unique()

teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

match_df['team2'].unique()

match_df['team1'] = match_df['team1'].str.replace('Delhi Daredevils','Delhi Capitals')
match_df['team2'] = match_df['team2'].str.replace('Delhi Daredevils','Delhi Capitals')

match_df['team1'] = match_df['team1'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
match_df['team2'] = match_df['team2'].str.replace('Deccan Chargers','Sunrisers Hyderabad')

match_df = match_df[match_df['team1'].isin(teams)]
match_df = match_df[match_df['team2'].isin(teams)]

match_df.shape

# Check unique values in team1 and team2 columns
print(match_df['team1'].unique())
print(match_df['team2'].unique())

# Check if 'Delhi Daredevils' or 'Deccan Chargers' are still in the team1 or team2 columns
print(match_df[match_df['team1'].str.contains('Delhi Daredevils|Deccan Chargers', na=False)])
print(match_df[match_df['team2'].str.contains('Delhi Daredevils|Deccan Chargers', na=False)])

match_df.head(5)

match_df = match_df[match_df['dl_applied'] == 0]

match_df = match_df[['match_id','city','winner','total_runs']]

delivery_df = match_df.merge(delivery,on='match_id')

delivery_df = delivery_df[delivery_df['inning'] == 2]

delivery_df.info()

delivery_df

# Ensure 'total_runs_y' is numeric
delivery_df['total_runs_y'] = pd.to_numeric(delivery_df['total_runs_y'], errors='coerce')

# Apply cumulative sum within each match_id group
delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs_y'].cumsum()

delivery_df['runs_left'] = delivery_df['total_runs_x'] - delivery_df['current_score']

delivery_df['balls_left'] = 126 - (delivery_df['over']*6 + delivery_df['ball'])

delivery_df

# Step 1: Fill NaNs and convert 'player_dismissed' to binary
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].fillna("0")
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].apply(lambda x: "1" if x != "0" else "0")
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].astype(int)

# Step 2: Calculate cumulative sum for 'player_dismissed' within each 'match_id'
delivery_df['wickets_taken'] = delivery_df.groupby('match_id')['player_dismissed'].cumsum()

# Step 3: Calculate remaining wickets
delivery_df['wickets'] = 10 - delivery_df['wickets_taken']

# Display the result
delivery_df.head()

delivery_df.head()

# crr = runs/overs
delivery_df['crr'] = (delivery_df['current_score']*6)/(120 - delivery_df['balls_left'])

delivery_df['rrr'] = (delivery_df['runs_left']*6)/delivery_df['balls_left']

def result(row):
    return 1 if row['batting_team'] == row['winner'] else 0

delivery_df['result'] = delivery_df.apply(result,axis=1)

final_df = delivery_df[['batting_team','bowling_team','city','runs_left','balls_left','wickets','total_runs_x','crr','rrr','result']]

final_df = final_df.sample(final_df.shape[0])

final_df.sample()

final_df.dropna(inplace=True)

final_df = final_df[final_df['balls_left'] != 0]

X = final_df.iloc[:,:-1]
y = final_df.iloc[:,-1]
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=1)

X_train

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

trf = ColumnTransformer([
    ('trf', OneHotEncoder(sparse_output=False, drop='first'), ['batting_team', 'bowling_team', 'city'])
], remainder='passthrough')

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

pipe = Pipeline(steps=[
    ('step1',trf),
    ('step2',LogisticRegression(solver='liblinear'))
])

pipe.fit(X_train,y_train)

y_pred = pipe.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

pipe.predict_proba(X_test)[10]

def match_summary(row):
    print("Batting Team-" + row['batting_team'] + " | Bowling Team-" + row['bowling_team'] + " | Target- " + str(row['total_runs_x']))

def match_progression(x_df,match_id,pipe):
    match = x_df[x_df['match_id'] == match_id]
    match = match[(match['ball'] == 6)]
    temp_df = match[['batting_team','bowling_team','city','runs_left','balls_left','wickets','total_runs_x','crr','rrr']].dropna()
    temp_df = temp_df[temp_df['balls_left'] != 0]
    result = pipe.predict_proba(temp_df)
    temp_df['lose'] = np.round(result.T[0]*100,1)
    temp_df['win'] = np.round(result.T[1]*100,1)
    temp_df['end_of_over'] = range(1,temp_df.shape[0]+1)

    target = temp_df['total_runs_x'].values[0]
    runs = list(temp_df['runs_left'].values)
    new_runs = runs[:]
    runs.insert(0,target)
    temp_df['runs_after_over'] = np.array(runs)[:-1] - np.array(new_runs)
    wickets = list(temp_df['wickets'].values)
    new_wickets = wickets[:]
    new_wickets.insert(0,10)
    wickets.append(0)
    w = np.array(wickets)
    nw = np.array(new_wickets)
    temp_df['wickets_in_over'] = (nw - w)[0:temp_df.shape[0]]

    print("Target-",target)
    temp_df = temp_df[['end_of_over','runs_after_over','wickets_in_over','lose','win']]
    return temp_df,target

temp_df,target = match_progression(delivery_df,74,pipe)
temp_df

import matplotlib.pyplot as plt
plt.figure(figsize=(18,8))
plt.plot(temp_df['end_of_over'],temp_df['wickets_in_over'],color='yellow',linewidth=3)
plt.plot(temp_df['end_of_over'],temp_df['win'],color='#00a65a',linewidth=4)
plt.plot(temp_df['end_of_over'],temp_df['lose'],color='red',linewidth=4)
plt.bar(temp_df['end_of_over'],temp_df['runs_after_over'])
plt.title('Target-' + str(target))

teams

delivery_df['city'].unique()

import pandas as pd

# Example input data; replace with actual values as needed
batting_team = "Mumbai Indians"
bowling_team = "Chennai Super Kings"
selected_city = "Mumbai"
target = 200
score = 150
overs = 15
wickets = 4

runs_left = target - score
balls_left = 120 - (overs * 6)
wickets_left = 10 - wickets
crr = score / overs
rrr = (runs_left * 6) / balls_left

input_df = pd.DataFrame({
    'batting_team': [batting_team],
    'bowling_team': [bowling_team],
    'city': [selected_city],
    'runs_left': [runs_left],
    'balls_left': [balls_left],
    'wickets': [wickets_left],
    'total_runs_x': [target],
    'crr': [crr],
    'rrr': [rrr]
})

result = pipe.predict_proba(input_df)
loss = result[0][0]  # Probability of losing
win = result[0][1]   # Probability of winning

print(f"{batting_team} Win Probability: {round(win * 100, 2)}%")
print(f"{bowling_team} Win Probability: {round(loss * 100, 2)}%")

"""**Making predictions using some user inputs:**"""

import pickle

# Assuming 'model' is your trained model
with open('pipe.pkl', 'wb') as file:
    pickle.dump(pipe, file)

# Teams and cities lists
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

# User inputs
batting_team = input(f'Select the batting team from {teams}: ')
bowling_team = input(f'Select the bowling team from {teams}: ')
selected_city = input(f'Select host city from {cities}: ')
target = int(input('Enter the target score: '))
score = int(input('Enter the current score: '))
overs = float(input('Enter the overs completed: '))
wickets = int(input('Enter the wickets out: '))

# Additional inputs
weather_condition = input('Enter the weather condition (e.g., Sunny, Rainy): ')
pitch_condition = input('Enter the pitch condition (e.g., Dry, Green): ')
recent_team_form = float(input('Enter the recent team form rating (1 to 5 scale): '))

# Calculate derived metrics
runs_left = target - score
balls_left = 120 - (overs * 6)
wickets_left = 10 - wickets
crr = score / overs if overs > 0 else 0
rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

# Create DataFrame for input to the model
input_df = pd.DataFrame({
    'batting_team': [batting_team],
    'bowling_team': [bowling_team],
    'city': [selected_city],
    'runs_left': [runs_left],
    'balls_left': [balls_left],
    'wickets': [wickets_left],
    'total_runs_x': [target],
    'crr': [crr],
    'rrr': [rrr],
    'weather_condition': [weather_condition],
    'pitch_condition': [pitch_condition],
    'recent_team_form': [recent_team_form]
})

# Make prediction
result = pipe.predict_proba(input_df)
loss = result[0][0]
win = result[0][1]

# Display results
print(f"{batting_team} - Probability of winning: {round(win * 100, 2)}%")
print(f"{bowling_team} - Probability of winning: {round(loss * 100, 2)}%")