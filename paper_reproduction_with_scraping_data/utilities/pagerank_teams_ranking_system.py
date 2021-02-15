import networkx as nx
import numpy as np

class pagerank_teams_ranking_system():
    
    def generate_graph_feature(self,data_frame,Tournament):
        
        #last_date=data_frame['Match Date'].tail(1).iloc[0]
        #first_date=str(last_date.year-2)+"-"+str(last_date.month)+"-"+str(last_date.day)
        dG = nx.DiGraph()
        df =  data_frame[(data_frame["Tournament"]==Tournament)]#& (data_frame['Match Date']>first_date)]
        G=np.mean(df.groupby(["Team","Opponent Team"]).count().max())
        for i in range(len(df)):
            team = df["Team"].iloc[i]
            df_team = df[(df["Team"]==team)]
                
            dG.add_node(team)
                
            for i in df_team["Opponent Team"]:
                if not dG.has_node(i):
                    dG.add_node(i)

                if not dG.has_edge(team, i):
                    g=len(df_team[(df_team["Opponent Team"]==i)])
                    weight=(np.sum(df_team["Winner Team"][(df_team["Opponent Team"]==i)]==i)/g)*1/(G-g+1)
                    dG.add_edge(team, i, weight= weight)

        return(nx.pagerank(dG))