# IPL_Winning_team_prediction

This project aims to predict the probability of winning for each team in an IPL (Indian Premier League) match using ML algorithms based on factors like the batting team, bowling team, city, current score, overs completed, and wickets lost. The project uses a logistic regression model in a pipeline setup with data preprocessing steps.



# Table of Contents
- [Project Overview](#ProjectOverview)
- [Dataset](#Dataset)
- [Model Training and Preprocessing](#Model_Training_And_Preprocessing)
- Usage
- Requirements
- Installation
- Future Work

## ProjectOverview: 

The goal of this project is to predict the probability that a team will win a given IPL match based on current in-game factors. This model could be useful for fans, analysts, or applications looking to provide live predictions during games.


## Dataset:
The dataset used in this project includes columns such as:

- batting_team: The team currently batting.
- bowling_team: The team currently bowling.
- city: The city where the match is taking place.
- target: The total runs target set for the batting team.
- score: The current score of the batting team.
- overs: The number of overs completed by the batting team.
- wickets: The number of wickets lost by the batting team.
- Additional columns and data preprocessing steps ensure that the model receives appropriate features for accurate predictions.


## Model_Training_And_Preprocessing:

The project uses a logistic regression model in a Pipeline that includes:

- Data Preprocessing: One-hot encoding for categorical features like batting_team, bowling_team, and city.
- Model: Logistic Regression, trained on the preprocessed data.
  
The pipeline allows for easy transformation and prediction in one go, streamlining the workflow.

## Requirements:

To run this project, you’ll need the following Python libraries:
- scikit-learn
- pandas
- numpy


## Installation:

- Clone this repository:

      git clone https://github.com/your-username/ipl-winning-team-prediction.git
      cd ipl-winning-team-prediction
    
- Install the dependencies:

      pip install -r requirements.txt
    
Run the model file directly in your preferred environment (e.g., Jupyter Notebook, Google Colab).

Future Work
License



The goal of this project is to predict the probability that a team will win a given IPL match based on current in-game factors. This model could be useful for fans, analysts, or applications looking to provide live predictions during games.
