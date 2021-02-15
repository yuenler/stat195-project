import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
from pi_rating import pi_rating
from Elo_rating_system import Elo_rating_system
from pagerank_teams_ranking_system import pagerank_teams_ranking_system
from multiprocessing import Pool
from functools import partial
from sklearn.preprocessing import MinMaxScaler
#from sklearn.decomposition import PCA


class features_creation:

    
    def check(self,dataframe):
        if (dataframe.empty) & (isinstance(dataframe, pd.DataFrame)) :
            return  pd.DataFrame(-0.1, index=np.arange(1), columns=dataframe.columns)
        
        elif (dataframe.empty) &  (isinstance(dataframe, pd.Series))  :
            return  pd.Series(-0.1, index=np.arange(1))
        else:
            return dataframe 

    def create_features(self,Data_Frame,Match_Date,Home_Team, Away_Team,Tournament):
        
        # Rating parameters
        if Tournament == 'Basket League':
            k0 = 39
            elo_lamda = 1.8
            pi_lamda = 0.09
            gamma = 0.55
            
        elif Tournament == 'Liga ACB':
            k0 = 53
            elo_lamda = 2.1
            pi_lamda = 0.08
            gamma = 0.58
            
        elif Tournament == 'Euroleague':
            k0 = 8
            elo_lamda = 2.5
            pi_lamda = 0.09
            gamma = 0.57
        
        elif Tournament == 'Eurocup':
            k0 = 19
            elo_lamda = 2.5
            pi_lamda = 0.15
            gamma = 0.61
            
        else:
            print('problem')
            
            
            
        
        columns_home=["teamFIC","Team Performance Index","team_Game_Score","teamDrtg","teamOrtg","teamPlay%","Team Points","teamTS%","teamEFG%"]


        columns_away=["opptFIC","Opponent Performance Index","oppt_Game_Score","opptDrtg","opptOrtg","opptPlay%","Opponent Points","opptTS%","opptEFG%"]
        
        datetime_object = datetime.strptime(Match_Date, '%Y-%m-%d')
        
        first_date=datetime_object - relativedelta(years=1)
        
        df=Data_Frame[(Data_Frame['Match Date'] <  datetime_object) & (Data_Frame['Match Date'] > first_date) &(Data_Frame['Tournament']==Tournament)]
        
        df_all_years=Data_Frame[(Data_Frame['Match Date'] <  datetime_object) &(Data_Frame['Tournament']==Tournament)]
        
        feat=pd.DataFrame(["d"], columns=['val0'])
        
        

        
        
        # tradition winner between 
        
        hist_bhwm=np.mean(df_all_years["Winner Team"][(df_all_years["Team"]==Home_Team) & 
                                        (df_all_years['Opponent Team']==Away_Team)]==Home_Team)

        hist_bawm=np.mean(df_all_years["Winner Team"][(df_all_years["Team"]==Home_Team) & 
                                            (df_all_years['Opponent Team']==Away_Team)]==Away_Team)
        
        if math.isnan(hist_bhwm):
            hist_bhwm=0
        if math.isnan(hist_bawm):
            hist_bawm=0
            
        feat["tradition_winner_match"]=hist_bhwm-hist_bawm
        
        
        hist_bhwg=np.mean(df_all_years["Winner Team"][((df_all_years["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)) |
                                        ((df_all_years["Team"]==Away_Team) & (df_all_years['Opponent Team']==Home_Team)) ]==Home_Team)

        hist_bawg=np.mean(df_all_years["Winner Team"][((df_all_years["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)) |
                                        ((df_all_years["Team"]==Away_Team) & (df_all_years['Opponent Team']==Home_Team)) ]==Away_Team)
        
        if math.isnan(hist_bhwg):
            hist_bhwg=0
        if math.isnan(hist_bawg):
            hist_bawg=0
        
        feat["tradition_winner_general"]=hist_bhwg-hist_bawg

        
        # tradition points difference between
        feat["tradition_pointsdiff_match"]=np.mean(df_all_years["Points difference"][(df_all_years["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)])
        
        hist_points_bH =np.mean(self.check(df_all_years["Points difference"][(df_all_years["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)]))
        
        hist_points_bA =np.mean(self.check(df_all_years["Points difference"][(df_all_years["Team"]==Away_Team) &  (df_all_years['Opponent Team']==Home_Team)]))
            
        feat["tradition_pointsdiff_general"]=hist_points_bH-hist_points_bA

        
        
        # tradition Ediff between 
        

        feat["tradition_Ediff_match"]=np.mean(df_all_years["teamEDiff"][(df_all_years["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)])
        
        
            
        hist_Ediff_bH= (np.mean(self.check(df_all_years["teamEDiff"][(df["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)]))+
                                    np.mean(self.check(df_all_years["opptEDiff"][(df["Team"]==Away_Team) & (df_all_years['Opponent Team']==Home_Team)])))/2
        

            
        hist_Ediff_bA= (np.mean(self.check(df_all_years["opptEDiff"][(df["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)]))+
                                    np.mean(self.check(df_all_years["teamEDiff"][(df["Team"]==Away_Team) & (df_all_years['Opponent Team']==Home_Team)])))/2
        
        feat["tradition_Ediff_general"]=hist_Ediff_bH-hist_Ediff_bA
        
        
        # last match winner between 
        
        hist_bhwlm=np.mean(df_all_years["Winner Team"][(df_all_years["Team"]==Home_Team) & 
                                        (df_all_years['Opponent Team']==Away_Team)].tail(1)==Home_Team)

        hist_bawlm=np.mean(df_all_years["Winner Team"][(df_all_years["Team"]==Home_Team) & 
                                        (df_all_years['Opponent Team']==Away_Team)].tail(1)==Away_Team)
        
        if math.isnan(hist_bhwlm):
            hist_bhwlm=0
        if math.isnan(hist_bawlm):
            hist_bawlm=0
            
        feat["tradition_winner_last_match"]=hist_bhwlm-hist_bawlm
        
        # last match points difference between
        feat["tradition_pointsdiff_last_match"]=np.mean(df_all_years["Points difference"][(df_all_years["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)].tail(1))
        
        # last match Ediff between
        feat["tradition_Ediff_between_last_match"]=np.mean(df_all_years["teamEDiff"][(df_all_years["Team"]==Home_Team) & (df_all_years['Opponent Team']==Away_Team)].tail(1))
        
        
        #pi-ratings
        teams1 = np.array([df_all_years["Home Team"],df_all_years["Away Team"]]).transpose()

        outcomes1 = np.array([df_all_years["Team Points"],df_all_years["Opponent Points"]]).transpose()
        
        pi_ratings = pi_rating().calculate_pi_ratings(teams = teams1,outcomes = outcomes1,el = pi_lamda, gamma = gamma,return_e =False)
        
        try :
            pi_hometeam=pi_ratings[Home_Team][0]
        except KeyError:
            pi_hometeam=-10 # pi-rating has and negative values so we push value lower than zero
        try :
            pi_awayteam=pi_ratings[Away_Team][1]
        except KeyError:
            pi_awayteam=-10 # pi-rating has and negative values so we push value lower than zero
        
        feat["pi_ratings"]= pi_hometeam - pi_awayteam
        
        
        # pi-rating expected
        #e_score_diff_H = (10**(abs(pi_hometeam)/3) - 1)
        #e_score_diff_A = (10**(abs(pi_awayteam)/3) - 1)
        
        #if pi_hometeam < 0:
                #e_score_diff_H = -e_score_diff_H
            
        #if pi_awayteam < 0:
                #e_score_diff_A = -e_score_diff_A


        #feat["pi_ratings_expected"]= e_score_diff_H - e_score_diff_A
        
        
        
        # Elo rating system 
        
        Elo_rating = Elo_rating_system()
        
        for j in np.unique(np.array(list(df_all_years["Home Team"].unique())+list(df_all_years["Away Team"].unique()))):
            Elo_rating.addTeam(j)
        for k in range(len(df_all_years)):
                Elo_rating.recordMatch(df_all_years["Home Team"].iloc[k],df_all_years["Away Team"].iloc[k],k0 = k0,lamda = elo_lamda
                                       ,winner=df_all_years["Winner Team"].iloc[k],diff=df_all_years['Points difference'].iloc[k])
        try:   
            elo_home=Elo_rating.getTeamRating(Home_Team)
        except AttributeError:
            elo_home=0
        try:
            elo_away=Elo_rating.getTeamRating(Away_Team)
        except AttributeError:
            elo_away=0

        feat["elo"]= elo_home-elo_away

        # elo expected
        
        #elo_expected_home=( 1+10**( ( elo_away-elo_home )/400.0 ) ) ** -1
        
        #feat["elo_expected"]=elo_expected_home
        
        
        
        #pagerank
        
        d = pagerank_teams_ranking_system().generate_graph_feature(data_frame = df,Tournament = Tournament)
        
        try:
            pagerank_home=d[Home_Team]
        except KeyError:
            pagerank_home=0
            
        try:
            pagerank_away=d[Away_Team]
        except KeyError:
            pagerank_away=0
        

        feat["pagerank"]=pagerank_home-pagerank_away
        
        
        # winner history of teams

        hist_hw=np.mean(df["Winner Team"][(df['Team']==Home_Team) | (df['Opponent Team']==Home_Team)]==Home_Team)

        hist_aw=np.mean(df["Winner Team"][(df['Team']==Away_Team) | (df['Opponent Team']==Away_Team)]==Away_Team)
        
        if math.isnan(hist_hw):
            hist_hw=0
        if math.isnan(hist_aw):
            hist_aw=0
        
        feat["history_winner"]=hist_hw-hist_aw
        
        
        # history points difference of teams 
        
        hist_hpointsdiff=(np.mean(df["Points difference"][(df['Team']==Home_Team)]) - np.mean(df["Points difference"][(df['Opponent Team']==Home_Team)]))/2

        hist_apointsdiff=(np.mean(df["Points difference"][(df['Team']==Away_Team)]) - np.mean(df["Points difference"][(df['Opponent Team']==Away_Team)]))/2
        
        if math.isnan(hist_hpointsdiff) & math.isnan(hist_apointsdiff):
            feat["history_pointsdiff"]=0
        
        # if one of two teams has not information we push the value 
        elif math.isnan(hist_hpointsdiff):
            if hist_apointsdiff>0:
                feat["history_pointsdiff"]= -hist_apointsdiff
            else:
                feat["history_pointsdiff"]= -0.5
            
        elif math.isnan(hist_apointsdiff):
            if hist_hpointsdiff>0:
                feat["history_pointsdiff"]= hist_hpointsdiff
            else:
                feat["history_pointsdiff"]= 0.5
        else:
            feat["history_pointsdiff"]=hist_hpointsdiff-hist_apointsdiff
                
        
        
        
        
        hist_hpointsdiffs=(np.std(self.check(df["Points difference"][(df['Team']==Home_Team)])) + np.std(self.check(df["Points difference"][(df['Opponent Team']==Home_Team)])))/2

        hist_apointsdiffs=(np.std(self.check(df["Points difference"][(df['Team']==Away_Team)])) + np.std(self.check(df["Points difference"][(df['Opponent Team']==Away_Team)])))/2
        
        
        feat["history_pointsdiff_sd"]=hist_hpointsdiffs-hist_apointsdiffs    
        
        # history Ediff of teams
        
        
        hist_hEDiff=(np.mean(df["teamEDiff"][(df['Team']==Home_Team)]) + np.mean(df["opptEDiff"][(df['Opponent Team']==Home_Team)]))/2

        hist_aEDiff=(np.mean(df["teamEDiff"][(df['Team']==Away_Team)]) + np.mean(df["opptEDiff"][(df['Opponent Team']==Away_Team)]))/2
        
        
        if math.isnan(hist_hEDiff) | math.isnan(hist_aEDiff):
            feat["history_Ediff"]=0
        elif math.isnan(hist_hEDiff):
            if hist_aEDiff>0:
                feat["history_Ediff"]= -hist_aEDiff
            else:
                feat["history_Ediff"]= -0.5
            
        elif math.isnan(hist_aEDiff):
            if hist_hEDiff>0:
                feat["history_Ediff"]= hist_hEDiff
            else:
                feat["history_Ediff"]= 0.5
        else:
            feat["history_Ediff"]=hist_hEDiff-hist_aEDiff
        
        


        hist_hEDiffs=(np.std(self.check(df["teamEDiff"][(df['Team']==Home_Team)])) + np.std(self.check(df["opptEDiff"][(df['Opponent Team']==Home_Team)])))/2

        hist_aEDiffs=(np.std(self.check(df["teamEDiff"][(df['Team']==Away_Team)])) + np.std(self.check(df["opptEDiff"][(df['Opponent Team']==Away_Team)])))/2

        feat["history_Ediff_sd"]=hist_hEDiffs-hist_aEDiffs
        
        # important stats mean
        
        history_home_mean=(self.check(df[df["Team"]==Home_Team].groupby(["Team"]).mean()[columns_home]).values+self.check(df[df["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).mean()[columns_away]).values)/2
        history_away_mean=(self.check(df[df["Team"]==Away_Team].groupby(["Team"]).mean()[columns_home]).values+self.check(df[df["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).mean()[columns_away]).values)/2
        
        
        history_mean_diff=history_home_mean[0]-history_away_mean[0]
        
        
        feat["history_FIC"]=history_mean_diff[0]
        
        feat["history_Performance_Index"]=history_mean_diff[1]
        
        feat["history_Game_Score"]=history_mean_diff[2]
        
        feat["history_Drtg"]=history_mean_diff[3]
        
        feat["history_Ortg"]=history_mean_diff[4]
        
        feat["history_Play"]=history_mean_diff[5]
        
        feat["history_Points"]=history_mean_diff[6]
        
        feat["history_TS"]=history_mean_diff[7]
        
        feat["history_EFG"]=history_mean_diff[8]
        
        
    
    
        # important stats sd
    
        history_home_sd=(self.check(df[df["Team"]==Home_Team].groupby(["Team"]).std()[columns_home]).values+self.check(df[df["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).std()[columns_away]).values)/2
        history_away_sd=(self.check(df[df["Team"]==Away_Team].groupby(["Team"]).std()[columns_home]).values+self.check(df[df["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).std()[columns_away]).values)/2

        
        
        history_sd_diff=history_home_sd[0]-history_away_sd[0]
        
        
            
        feat["history_FIC_sd"]=history_sd_diff[0]
        
        feat["history_Performance_Index_sd"]=history_sd_diff[1]
        
        feat["history_Game_Score_sd"]=history_sd_diff[2]
        
        feat["history_Drtg_sd"]=history_sd_diff[3]
        
        feat["history_Ortg_sd"]=history_sd_diff[4]
        
        feat["history_Play_sd"]=history_sd_diff[5]
        
        feat["history_Points_sd"]=history_sd_diff[6]
        
        feat["history_TS_sd"]=history_sd_diff[7]
        
        feat["history_EFG_sd"]=history_sd_diff[8]
    
        # important stats received mean
    
        history_home_received_mean=(self.check(df[df["Team"]==Home_Team].groupby(["Team"]).mean()[columns_away]).values+self.check(df[df["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).mean()[columns_home]).values)/2
        history_away_received_mean=(self.check(df[df["Team"]==Away_Team].groupby(["Team"]).mean()[columns_away]).values+self.check(df[df["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).mean()[columns_home]).values)/2  
        
        
        history_mean_received_diff=history_home_received_mean[0]-history_away_received_mean[0]
        
        feat["history_FIC_received"]=history_mean_received_diff[0]
        
        feat["history_Performance_Index_received"]=history_mean_received_diff[1]
        
        feat["history_Game_Score_received"]=history_mean_received_diff[2]
        
        # SOME WITH THE OPPOSITE OF THE ACHIEVED
        #feat["history_Drtg_received"]=history_mean_received_diff[3]
        #feat["history_Ortg_received"]=history_mean_received_diff[4]
        
        feat["history_Play_received"]=history_mean_received_diff[5]
        
        feat["history_Points_received"]=history_mean_received_diff[6]
        
        feat["history_TS_received"]=history_mean_received_diff[7]
        
        feat["history_EFG_received"]=history_mean_received_diff[8]
    
        # important stats received sd
    
        history_home_received_sd=(self.check(df[df["Team"]==Home_Team].groupby(["Team"]).std()[columns_away]).values+self.check(df[df["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).std()[columns_home]).values)/2
        history_away_received_sd=(self.check(df[df["Team"]==Away_Team].groupby(["Team"]).std()[columns_away]).values+self.check(df[df["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).std()[columns_home]).values)/2
    
        
        
        history_sd_received_diff=history_home_received_sd[0]-history_away_received_sd[0]
        
        feat["history_FIC_received_sd"]=history_sd_received_diff[0]
        
        feat["history_Performance_Index_received_sd"]=history_sd_received_diff[1]
        
        feat["history_Game_Score_received_sd"]=history_sd_received_diff[2]

        # SOME WITH THE OPPOSITE OF THE ACHIEVED
        #feat["history_Drtg_received_sd"]=history_sd_received_diff[3]
        #feat["history_Ortg_received_sd"]=history_sd_received_diff[4]
        
        feat["history_Play_received_sd"]=history_sd_received_diff[5]
        
        feat["history_Points_received_sd"]=history_sd_received_diff[6]
        
        feat["history_TS_received_sd"]=history_sd_received_diff[7]
        
        feat["history_EFG_received_sd"]=history_sd_received_diff[8]
        
    
        
        
        # LAST 10 MATCHES 

        df2=df_all_years[(df_all_years['Team']==Home_Team) | (df_all_years['Opponent Team']==Home_Team)].tail(10)
        
        try:
            #match_dt1=str(df2['Match Date'].iloc[0].year)+"-"+ str(df2['Match Date'].iloc[0].month)+"-"+str(df2['Match Date'].iloc[0].day)
        
            df_dt1=df_all_years[df_all_years['Match Date']>df2['Match Date'].iloc[0]]
            
            teams2=np.array([df_dt1["Home Team"],df_dt1["Away Team"]]).transpose()

            outcomes2=np.array([df_dt1["Team Points"],df_dt1["Opponent Points"]]).transpose()
        
            pi_ratings1=pi_rating().calculate_pi_ratings(teams2,outcomes2,el = pi_lamda, gamma = gamma,return_e =False)
        
            try :
                pi_hometeam1=pi_ratings1[Home_Team][0]
            except KeyError:
                pi_hometeam1=-10
        
            
            Elo_rating = Elo_rating_system()
            for j in np.unique(np.array(list(df_dt1["Home Team"].unique())+list(df_dt1["Away Team"].unique()))):
                Elo_rating.addTeam(j)
            for k in range(len(df_dt1)):
                Elo_rating.recordMatch(df_dt1["Home Team"].iloc[k],df_dt1["Away Team"].iloc[k], k0=k0,lamda = elo_lamda ,
                                       winner=df_dt1["Winner Team"].iloc[k],diff=df_dt1['Points difference'].iloc[k])

            try:
                elo1= Elo_rating.getTeamRating(Home_Team)
            except AttributeError:
                elo1=0
            
            d1=pagerank_teams_ranking_system().generate_graph_feature(df_dt1,Tournament)
        
            try:
                pagerank_home1=d1[Home_Team]
            except KeyError:
                pagerank_home1=0
            
        except:
            elo1=0
            pagerank_home1=0
            pi_hometeam1=-10

        cf_w1=np.mean(df2["Winner Team"]==Home_Team)
        
        cf_pointsdiff1=(np.mean(df2["Points difference"][(df2['Team']==Home_Team)]) - np.mean(df2["Points difference"][(df2['Opponent Team']==Home_Team)]))/2
        cf_pointsdiffs1=(np.std(self.check(df2["Points difference"][(df2['Team']==Home_Team)])) + np.std(self.check(df2["Points difference"][(df2['Opponent Team']==Home_Team)])))/2
        
        cf_EDiff1=(np.mean(df2["teamEDiff"][(df2['Team']==Home_Team)]) + np.mean(df2["opptEDiff"][(df2['Opponent Team']==Home_Team)]))/2
        cf_EDiffs1=(np.std(self.check(df2["teamEDiff"][(df2['Team']==Home_Team)])) + np.std(self.check(df2["opptEDiff"][(df2['Opponent Team']==Home_Team)])))/2
        
        
        current_home_mean=(self.check(df2[df2["Team"]==Home_Team].groupby(["Team"]).mean()[columns_home]).values+self.check(df2[df2["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).mean()[columns_away]).values)/2
        current_home_sd=(self.check(df2[df2["Team"]==Home_Team].groupby(["Team"]).std()[columns_home]).values+self.check(df2[df2["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).std()[columns_away]).values)/2
        current_home_received_mean=(self.check(df2[df2["Team"]==Home_Team].groupby(["Team"]).mean()[columns_away]).values+self.check(df2[df2["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).mean()[columns_home]).values)/2
        current_home_received_sd=(self.check(df2[df2["Team"]==Home_Team].groupby(["Team"]).std()[columns_away]).values+self.check(df2[df2["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).std()[columns_home]).values)/2
        
        
        
        
        
        

        df3=df_all_years[(df_all_years['Team']==Away_Team) | (df_all_years['Opponent Team']==Away_Team)].tail(10)
        
        try:
            #match_dt2=str(df3['Match Date'].iloc[0].year)+"-"+ str(df3['Match Date'].iloc[0].month)+"-"+str(df3['Match Date'].iloc[0].day)
        
            df_dt2=df_all_years[df_all_years['Match Date']>df3['Match Date'].iloc[0]]
            
            
            teams3=np.array([df_dt2["Home Team"],df_dt2["Away Team"]]).transpose()

            outcomes3=np.array([df_dt2["Team Points"],df_dt2["Opponent Points"]]).transpose()
        
            pi_ratings2=calculate_pi_ratings(teams3,outcomes3,el = pi_lamda, gamma = gamma,return_e =False)
        
            try :
                pi_awayteam1=pi_ratings2[Away_Team][0]
            except KeyError:
                pi_awayteam1=-10
        

            Elo_rating = Elo_rating_system()
            for j in np.unique(np.array(list(df_dt2["Home Team"].unique())+list(df_dt2["Away Team"].unique()))):
                Elo_rating.addTeam(j)
            for k in range(len(df_dt2)):
                Elo_rating.recordMatch(df_dt2["Home Team"].iloc[k],df_dt2["Away Team"].iloc[k],k0=k0,lamda = elo_lamda,
                                       winner=df_dt2["Winner Team"].iloc[k],diff=df_dt2['Points difference'].iloc[k])

                
            try:
                elo2= Elo_rating.getTeamRating(Away_Team)
            except AttributeError:
                elo2=0
            d2=generate_graph_feature(df_dt2,Tournament)
        
            try:
                pagerank_away1=d2[Away_Team]
            except KeyError:
                pagerank_away1=0
                
        except:
            elo2=0
            pagerank_away1=0
            pi_awayteam1=-10
        
        cf_w2=np.mean(df3["Winner Team"]==Away_Team)

        
        cf_pointsdiff2=(np.mean(df3["Points difference"][(df3['Team']==Away_Team)]) - np.mean(df3["Points difference"][(df3['Opponent Team']==Away_Team)]))/2
        cf_pointsdiffs2=(np.std(self.check(df3["Points difference"][(df3['Team']==Away_Team)])) + np.std(self.check(df3["Points difference"][(df3['Opponent Team']==Away_Team)])))/2
        
        cf_EDiff2=(np.mean(df3["teamEDiff"][(df3['Team']==Away_Team)]) + np.mean(df3["opptEDiff"][(df3['Opponent Team']==Away_Team)]))/2
        cf_EDiffs2=(np.std(self.check(df3["teamEDiff"][(df3['Team']==Away_Team)])) + np.std(self.check(df3["opptEDiff"][(df3['Opponent Team']==Away_Team)])))/2
        
        
        current_away_mean=(self.check(df3[df3["Team"]==Away_Team].groupby(["Team"]).mean()[columns_home]).values+self.check(df3[df3["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).mean()[columns_away]).values)/2
        current_away_sd=(self.check(df3[df3["Team"]==Away_Team].groupby(["Team"]).std()[columns_home]).values+self.check(df3[df3["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).std()[columns_away]).values)/2
        current_away_received_mean=(self.check(df3[df3["Team"]==Away_Team].groupby(["Team"]).mean()[columns_away]).values+self.check(df3[df3["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).mean()[columns_home]).values)/2  
        current_away_received_sd=(self.check(df3[df3["Team"]==Away_Team].groupby(["Team"]).std()[columns_away]).values+self.check(df3[df3["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).std()[columns_home]).values)/2
    
        
        
        
        
        feat["Current_form_pi_ratings"]= pi_hometeam1 - pi_awayteam1


        # pi-rating expected
        #Current_e_score_diff_H = (10**(abs(pi_hometeam1)/3) - 1)
        #Current_e_score_diff_A = (10**(abs(pi_awayteam1)/3) - 1)
        
        #if pi_hometeam1 < 0:
                #Current_e_score_diff_H = -Current_e_score_diff_H
            
        #if pi_awayteam1 < 0:
                #Current_e_score_diff_A= -Current_e_score_diff_A



        #feat["Current_form_pi_ratings_expected"]= Current_e_score_diff_H - Current_e_score_diff_A
        
        
        feat["Current_form_elo"]=elo1-elo2
        
        #elo expected
        #Current_elo_expected_home=( 1+10**( ( elo2-elo1 )/400.0 ) ) ** -1
        #feat["Current_form_elo_expected"]=Current_elo_expected_home
        
        feat["Current_form_pagerank"]=pagerank_home1-pagerank_away1
        
        
        if math.isnan(cf_w1):
            cf_w1=0
        if math.isnan(cf_w2):
            cf_w2=0  

        feat["Current_form_winner"]=cf_w1-cf_w2
        
        if math.isnan(cf_pointsdiff1) & math.isnan(cf_pointsdiff2):
            feat["Current_form_pointsdiff"]=0
        
        elif math.isnan(cf_pointsdiff1):
            if cf_pointsdiff2>0:
                feat["Current_form_pointsdiff"]= -cf_pointsdiff2
            else:
                feat["Current_form_pointsdiff"]= -0.5
            
        elif math.isnan(cf_pointsdiff2):
            if cf_pointsdiff1>0:
                feat["Current_form_pointsdiff"]= cf_pointsdiff1
            else:
                feat["Current_form_pointsdiff"]= 0.5
        else:
            feat["Current_form_pointsdiff"]=cf_pointsdiff1-cf_pointsdiff2
        
        
        feat["Current_form_pointsdiff_sd"]=cf_pointsdiffs1-cf_pointsdiffs2
        

        if math.isnan(cf_EDiff1) | math.isnan(cf_EDiff2):
            feat["Current_form_EDiff"]=0
            
        elif math.isnan(cf_EDiff1):
            if cf_EDiff2>0:
                feat["Current_form_EDiff"]= -cf_EDiff2
            else:
                feat["Current_form_EDiff"]= -0.5
            
        elif math.isnan(cf_EDiff2):
            if cf_EDiff1>0:
                feat["Current_form_EDiff"]= cf_EDiff1
            else:
                feat["Current_form_EDiff"]= 0.5
        else:
            feat["Current_form_EDiff"]=cf_EDiff1-cf_EDiff2
            
            
        
        feat["Current_form_EDiff_sd"]=cf_EDiffs1-cf_EDiffs2
        
        
        
        current_mean_diff=current_home_mean[0]-current_away_mean[0]
        
        
        feat["Current_form_FIC"]=current_mean_diff[0]
        
        feat["Current_form_Performance_Index"]=current_mean_diff[1]
        
        feat["Current_form_Game_Score"]=current_mean_diff[2]
        
        feat["Current_form_Drtg"]=current_mean_diff[3]
        
        feat["Current_form_Ortg"]=current_mean_diff[4]
        
        feat["Current_form_Play"]=current_mean_diff[5]
        
        feat["Current_form_Points"]=current_mean_diff[6]
        
        feat["Current_form_TS"]=current_mean_diff[7]
        
        feat["Current_form_EFG"]=current_mean_diff[8]
        
        
        current_sd_diff=current_home_sd[0]-current_away_sd[0]
        
        feat["Current_form_FIC_sd"]=current_sd_diff[0]
        
        feat["Current_form_Performance_Index_sd"]=current_sd_diff[1]
        
        feat["Current_form_Game_Score_sd"]=current_sd_diff[2]
        
        feat["Current_form_Drtg_sd"]=current_sd_diff[3]
        
        feat["Current_form_Ortg_sd"]=current_sd_diff[4]
        
        feat["Current_form_Play_sd"]=current_sd_diff[5]
        
        feat["Current_form_Points_sd"]=current_sd_diff[6]
        
        feat["Current_form_TS_sd"]=current_sd_diff[7]
        
        feat["Current_form_EFG_sd"]=current_sd_diff[8]
        
        
        
        current_mean_received_diff=current_home_received_mean[0]-current_away_received_mean[0]
        
        feat["Current_form_FIC_received"]=current_mean_received_diff[0]
        
        feat["Current_form_Performance_Index_received"]=current_mean_received_diff[1]
        
        feat["Current_form_Game_Score_received"]=current_mean_received_diff[2]

        # SOME WITH THE OPPOSITE OF THE ACHIEVED
        #feat["Current_Drtg_received"]=current_mean_received_diff[3]
        #feat["Current_Ortg_received"]=current_mean_received_diff[4]
        
        feat["Current_form_Play_received"]=current_mean_received_diff[5]
        
        feat["Current_form_Points_received"]=current_mean_received_diff[6]
        
        feat["Current_form_TS_received"]=current_mean_received_diff[7]
        
        feat["Current_form_EFG_received"]=current_mean_received_diff[8]
        
        
        current_sd_received_diff=current_home_received_sd[0]-current_away_received_sd[0]
        
        feat["Current_form_FIC_received_sd"]=current_sd_received_diff[0]
        
        feat["Current_form_Performance_Index_received_sd"]=current_sd_received_diff[1]
        
        feat["Current_form_Game_Score_received_sd"]=current_sd_received_diff[2]

        # SOME WITH THE OPPOSITE OF THE ACHIEVED
        #feat["Current_Drtg_received_sd"]=current_sd_received_diff[3]
        #feat["Current_Ortg_received_sd"]=current_sd_received_diff[4]
        
        feat["Current_form_Play_received_sd"]=current_sd_received_diff[5]
        
        feat["Current_form_Points_received_sd"]=current_sd_received_diff[6]
        
        feat["Current_form_TS_received_sd"]=current_sd_received_diff[7]
        
        feat["Current_form_EFG_received_sd"]=current_sd_received_diff[8]


        
        #Tournament

        l_df=df[df["Tournament"]==Tournament]
        
        feat["Tournament_Points_difference"]=np.mean(l_df["Points difference"])
        feat["Tournament_Points_difference_sd"]=np.std(l_df["Points difference"])
        
        feat["Tournament_EDiff"] = np.mean(l_df["teamEDiff"])
        feat["Tournament_EDiff_sd"] = np.std(l_df["teamEDiff"])
        
        
        
        tournament_home_mean=self.check(l_df.groupby(["Tournament"]).mean()[columns_home]).values
        tournament_away_mean=self.check(l_df.groupby(["Tournament"]).mean()[columns_away]).values
        
        
        tournament_mean_diff=tournament_home_mean[0]-tournament_away_mean[0]
        
        
        feat["Tournament_FIC"]=tournament_mean_diff[0]
        
        feat["Tournament_Performance_Index"]=tournament_mean_diff[1]
        
        feat["Tournament_Game_Score"]=tournament_mean_diff[2]
        
        feat["Tournament_Drtg"]=tournament_mean_diff[3]

        #Same information with Tournament_Drtg
        #feat["Tournament_Ortg"]=tournament_mean_diff[4]
        
        feat["Tournament_Play"]=tournament_mean_diff[5]
        
        #feat["Tournament_Points"]=tournament_mean_diff[6]
        
        feat["Tournament_TS"]=tournament_mean_diff[7]
        
        feat["Tournament_EFG"]=tournament_mean_diff[8]
        
        
    
    
        # important stats sd
    
        tournament_home_sd=self.check(l_df.groupby(["Tournament"]).std()[columns_home]).values
        tournament_away_sd=self.check(l_df.groupby(["Tournament"]).std()[columns_away]).values
        
        
        tournament_sd_diff=tournament_home_sd[0]-tournament_away_sd[0]
        
        
        feat["Tournament_FIC_sd"]=tournament_sd_diff[0]
        
        feat["Tournament_Performance_Index_sd"]=tournament_sd_diff[1]
        
        feat["Tournament_Game_Score_sd"]=tournament_sd_diff[2]
        
        feat["Tournament_Drtg_sd"]=tournament_sd_diff[3]
        
        #Same information with Tournament_Drtg
        #feat["Tournament_Ortg_sd"]=tournament_sd_diff[4]
        
        feat["Tournament_Play_sd"]=tournament_sd_diff[5]
        
        feat["Tournament_Points_sd"]=tournament_sd_diff[6]
        
        feat["Tournament_TS_sd"]=tournament_sd_diff[7]
        
        feat["Tournament_EFG_sd"]=tournament_sd_diff[8]
        
        
        

        feat["Tournament_home_winner"]=np.mean((l_df["Home Team"]==l_df["Winner Team"]))
        
        return feat.iloc[:,1:]

    
    def features(self,x1,Data_Frame):
        data=[]
        x1['Match Date'] = pd.to_datetime(x1['Match Date'])
        for i in  range(len(x1)):
            data.append(self.create_features(Data_Frame,Match_Date=str(x1['Match Date'].dt.date.iloc[i]),
                                             Home_Team=str(x1['Home Team'].iloc[i]),Away_Team=str(x1['Away Team'].iloc[i]),
                                             Tournament=str(x1['Tournament'].iloc[i])))
    
        data2=pd.concat(data).fillna(0).reset_index().iloc[:,1:]

        return data2 


    def run_features_creations(self,pool,Data_Frame,Tournament,Date):

        x1=Data_Frame[(Data_Frame['Tournament'] ==Tournament)&(Data_Frame['Match Date'] >Date)]

        #x2=Data_Frame[(Data_Frame['Tournament'] ==Tournament)&(Data_Frame['Match Date'] <= Date)]

        #teams1=np.array([x2["Home Team"],x2["Away Team"]]).transpose()

        #outcomes1=np.array([x2["Team Points"],x2["Opponent Points"]]).transpose()

        #best= pi_rating().optimize_pi_ratings(teams = teams1, outcomes = outcomes1)

        chunks = np.array_split(x1, 6)
         
        result = pool.map(partial(self.features,Data_Frame=Data_Frame), chunks)


        data=pd.concat(result)

        data=pd.concat([data.reset_index().iloc[:,1:],pd.get_dummies(x1['Phase'],drop_first=True).reset_index().iloc[:,1:]],axis=1)

        y = x1[['Team Result']].reset_index(drop=True)
        
        all_data = pd.concat([data.reset_index(drop=True),y],axis=1)

        return all_data
    
    
    def features_count(self,current_features,tournament):
        try:
            old_features_count = pd.read_csv('Important_Features/features_'+tournament+'.csv',sep=',')
        except:
            old_features_count = pd.DataFrame({'feature_name','Count'})

        current_features = current_features[current_features['value']!=0]
        current_features.drop(columns = ['value'],inplace = True)
        current_features['Count'] = 1

        features_concat = pd.concat([old_features_count,current_features])

        new_feutures = features_concat.groupby(['feature_name']).agg('sum').reset_index().sort_values('Count',
                                                                                                      ascending = False)
        new_feutures.to_csv('Important_Features/features_'+tournament+'.csv',sep = ',',index = None, header=True)
        
    
    def run_features_creations_alternative_analysis(self,pool,Data_Frame,Tournament,Date,Date2,analysis='Mid-Season',play_offs_name =["Playoffs"]):

        if analysis=='Mid-Season':
            x1=Data_Frame[(Data_Frame['Tournament'] ==Tournament)&(Data_Frame['Match Date'] >Date)&(Data_Frame['Match Date'] <Date2)&(~Data_Frame['Phase'].isin(play_offs_name))]
            
            
            #middle_season_date = x1["Match Date"][(x1["Home Team"]==x1["Away Team"].iloc[0]) & (x1["Away Team"]==x1["Home Team"].iloc[0])].dt.date.values[0]
            
            
            #x2=Data_Frame[(Data_Frame['Tournament'] ==Tournament)&(Data_Frame['Match Date'] <= middle_season_date)]

            #teams1=np.array([x2["Home Team"],x2["Away Team"]]).transpose()

            #outcomes1=np.array([x2["Team Points"],x2["Opponent Points"]]).transpose()

            #best= pi_rating().optimize_pi_ratings(teams = teams1, outcomes = outcomes1)

            chunks = np.array_split(x1, 6)

            result = pool.map(partial(self.features,Data_Frame=Data_Frame), chunks)


            data=pd.concat(result)

            data=pd.concat([data.reset_index().iloc[:,1:],
                              pd.get_dummies(x1['Phase'],drop_first=True).reset_index().iloc[:,1:]],axis=1)

            y = x1['Team Result']

            data_scaled = MinMaxScaler().fit_transform(data)
            #pca = PCA(n_components=10)
            #data_scaled = pca.fit_transform(data)

            x_train=data_scaled[:int(len(x1)/2)]

            y_train=y.iloc[:int(len(x1)/2)]
            
            x_test=data_scaled[int(len(x1)/2):int(len(x1))]
            y_test=y.iloc[int(len(x1)/2):int(len(x1))]
            
        elif analysis=='Playoffs':
            
            x1=Data_Frame[(Data_Frame['Tournament'] ==Tournament)&(Data_Frame['Match Date'] >Date)&(Data_Frame['Match Date'] <Date2)]
                      

            chunks = np.array_split(x1, 6)

            result = pool.map(partial(self.features,Data_Frame=Data_Frame), chunks)


            data=pd.concat(result)

            data=pd.concat([data.reset_index().iloc[:,1:],
                              pd.get_dummies(x1['Phase'],drop_first=True).reset_index().iloc[:,1:]],axis=1)

            y = x1['Team Result']

            data_scaled = MinMaxScaler().fit_transform(data)

            x_train=data_scaled[:len(x1[~x1['Phase'].isin(play_offs_name)])]

            y_train=y.iloc[:len(x1[~x1['Phase'].isin(play_offs_name)])]
            
            x_test=data_scaled[len(x1[~x1['Phase'].isin(play_offs_name)]):]
            y_test=y.iloc[len(x1[~x1['Phase'].isin(play_offs_name)]):]


        return x1,data,x_train,y_train,x_test,y_test



