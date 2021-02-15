from Elo_rating_system import Elo_rating_system
import numpy as np
import pandas as pd


def elo_rating_matches(Data_Frame,Match_Date,k0=1,lamda=1):
    
    df = Data_Frame[(Data_Frame['Match Date'] < Match_Date)]

    Elo_rating = Elo_rating_system()

    for j in np.unique(np.array(list(df["Home Team"].unique())+list(df["Away Team"].unique()))):
        Elo_rating.addTeam(j)
    for p in range(len(df)):
        Elo_rating.recordMatch(df["Home Team"].iloc[p],df["Away Team"].iloc[p],winner=df["Winner Team"].iloc[p],
                      diff =df['Points difference'].iloc[p] ,k0=k0,lamda=lamda)
    return Elo_rating
        
def elo_loss(Elo_rating,Home_Team,Away_Team,real_winner):
    try:   
        elo_home=Elo_rating.getTeamRating(Home_Team)
    except AttributeError:
        elo_home=0
    try:
        elo_away=Elo_rating.getTeamRating(Away_Team)
    except AttributeError:
        elo_away=0

    elo_expected_home=( 1+10**( ( elo_away-elo_home )/400.0 ) ) ** -1

    loss = abs(real_winner - elo_expected_home)


    return loss

def run_elo_tuning(lamda_values,k0_values,matches,Data_Frame):

    loss_array = np.zeros((len(lamda_values),len(k0_values)))
    for lamda in range(len(lamda_values)): 
        for k0 in range(len(k0_values)):
            loss=[]
            for match_date in  matches['Match Date'].unique():
                Elo_rating = elo_rating_matches(Data_Frame=Data_Frame,Match_Date=str(match_date)
                                               ,k0=k0_values[k0],lamda=lamda_values[lamda])

                df_matches_date = matches[matches['Match Date']==match_date]
                for i in  range(len(df_matches_date)): 
                    loss.append(elo_loss(Elo_rating = Elo_rating ,Home_Team=str(df_matches_date['Home Team'].iloc[i]),
                                         Away_Team=str(df_matches_date['Away Team'].iloc[i]),
                                         real_winner = df_matches_date['Team Result'].iloc[i]))

            loss_array[lamda,k0] = np.mean(loss)
            
    return loss_array