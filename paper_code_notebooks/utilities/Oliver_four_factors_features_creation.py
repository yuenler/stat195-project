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
                        
        
        columns_home=["teamEFG%","teamTO%","teamOREB%","Team Free Throws Percenage"]


        columns_away=["opptEFG%","opptTO%","opptOREB%","Opponent Free Throws Percenage"]
        
        datetime_object = datetime.strptime(Match_Date, '%Y-%m-%d')
        
        first_date=datetime_object - relativedelta(years=1)
        
        df_all_years=Data_Frame[(Data_Frame['Match Date'] <  datetime_object) &(Data_Frame['Tournament']==Tournament)]
        
        
        feat=pd.DataFrame(["d"], columns=['val0'])
    
        
        
        # LAST 10 MATCHES 

        df2=df_all_years[(df_all_years['Team']==Home_Team) | (df_all_years['Opponent Team']==Home_Team)].tail(10)
        
        
        current_home_mean=(self.check(df2[df2["Team"]==Home_Team].groupby(["Team"]).mean()[columns_home]).values+self.check(df2[df2["Opponent Team"]==Home_Team].groupby(["Opponent Team"]).mean()[columns_away]).values)/2
    

    
    
        df3=df_all_years[(df_all_years['Team']==Away_Team) | (df_all_years['Opponent Team']==Away_Team)].tail(10)
        
        
        current_away_mean=(self.check(df3[df3["Team"]==Away_Team].groupby(["Team"]).mean()[columns_home]).values+self.check(df3[df3["Opponent Team"]==Away_Team].groupby(["Opponent Team"]).mean()[columns_away]).values)/2
        
        
        feat["home_EFG%"]=current_home_mean[0][0]
        
        feat["home_TO%"]=current_home_mean[0][1]
        
        feat["home_OREB%"]=current_home_mean[0][2]
        
        feat["home_FTRate"]=current_home_mean[0][3]
   

        
        feat["away_EFG%"]=current_away_mean[0][0]
        
        feat["away_TO%"]=current_away_mean[0][1]
        
        feat["away_OREB%"]=current_away_mean[0][2]
        
        feat["away_FTRate"]=current_away_mean[0][3]
        
        
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

        chunks = np.array_split(x1, 6)
         
        result = pool.map(partial(self.features,Data_Frame=Data_Frame), chunks)


        data=pd.concat(result).reset_index(drop=True)

        y = x1[['Team Result']].reset_index(drop=True)
        
        all_data = pd.concat([data,y],axis=1)

        return all_data
    
    


