import numpy as np
import pandas as pd



class pi_rating:
    
    """
    A class that represents an implementation of the pi -rating System from  https://github.com/larsvancutsem/piratings for R package
    """

    def calculate_pi_ratings(self,teams , outcomes, el = 0.1, gamma = 0.4, b = 10, c = 3, return_e = False) :
        # ================================================================================
        # create local variables and calculate pi ratings
        # ================================================================================


        # create local variables


        # amount_matches:     amount of matches in dataset
        #
        # pi_ratings:         numerical matrix with pi ratings for each match
        #                     for respective columns 1 and 2 in the
        #                     teams matrix
        #
        # teams:              list of unique teams that occur in dataset
        #                     with respective home and away rankings
        #
        # score_diff:         actual score difference Home vs Away
        #
        # pred_score_diff:    predicted score difference Home vs Away
        #
        # abs_error:          list of absolute error in predicted score vs actual score differences
        #
        # home_team:          home team name
        #
        # away_team:          away team name
        #
        # HH_list:            list of home team's home ratings
        #
        # HA_list:            list of home team's away ratings
        #
        # AA_list:            list of away team's away ratings
        #
        # AH_list:            list of away team's home ratings
        #
        # team_rate_HH:       home team home rating
        #
        # team_rate_HA:       home team away rating
        #
        # team_rate_AA:       away team away rating
        #
        # team_rate_AH:       away team home rating
        #
        # e_score_diff_H:     expected score difference
        #                     against the average opponent
        #                     for the home team
        #
        # e_score_diff_A:     expected score difference
        #                     against the average opponent
        #                     for the away team
        #
        # e_score_diff:       expected score difference
        #                     for match
        #
        # prediction_error:   prediction error
        #
        # weighted_error:     weighted error
        #
        # weighted_error_H:   weighted error home team
        #
        # weighted_error_A:   weighted error away team
        #
        # mean_sq_e:          mean squared error
        #


        amount_matches = outcomes.shape[0]
        pi_ratings = np.zeros((amount_matches,2))

        team_list = list(np.unique(teams[:,0]))+ list(np.unique(teams[:,1]))
        
        team_dict={}
        for team in team_list:
            team_dict[team]=[0,0]


        abs_error =[]

        home_team =""

        away_team =""

        HH_list =[]

        HA_list =[]

        AA_list =[]

        AH_list =[]
        
        team_rate_HH =0

        team_rate_HA =0

        team_rate_AA =0

        team_rate_AH =0

        e_score_diff_H =0

        e_score_diff_A =0

        e_score_diff =0

        prediction_error =0

        weighted_error =0

        weighted_error_H =0

        weighted_error_A =0
        
        mean_sq_e =0


        # calculate pi ratings


        for i in range(amount_matches) :
            home_team = teams[i, 0]
            away_team = teams[i, 1]
            score_diff = (outcomes[i, 0] - outcomes[i, 1])

            # retrieve ratings of respective teams
            HH_list.append(team_dict[home_team][0])
            HA_list.append(team_dict[home_team][1])
            AA_list.append(team_dict[away_team][1])
            AH_list.append(team_dict[away_team][0])
            
            team_rate_HH = HH_list[len(HH_list)-1]
            team_rate_HA = HA_list[len(HA_list)-1]
            team_rate_AA = AA_list[len(AA_list)-1]
            team_rate_AH = AH_list[len(AH_list)-1]
            
            pi_ratings[i, 0] = team_rate_HH
            pi_ratings[i, 1]= team_rate_AA
        
            # calculate expected score differences against average team
            e_score_diff_H = (b**(abs(team_rate_HH)/c) - 1)
            e_score_diff_A = (b**(abs(team_rate_AA)/c) - 1)
            
            if team_rate_HH < 0:
                e_score_diff_H = -e_score_diff_H
            
            if team_rate_AA < 0:
                e_score_diff_A = -e_score_diff_A
            

            # calculate expected score difference for match
            e_score_diff = e_score_diff_H - e_score_diff_A

            # calculate prediction error
            prediction_error = abs(score_diff - e_score_diff)

            # store prediction error in list of absolute errors
            abs_error.append(prediction_error)

            # calculate weighted error
            weighted_error = c * np.log10(1 + prediction_error)
        
            if (e_score_diff < score_diff) :
                weighted_error_H = weighted_error
                weighted_error_A = -weighted_error
            else :
                weighted_error_H = -weighted_error
                weighted_error_A = weighted_error
        

            # update ratings
            team_dict[home_team][0] = team_rate_HH + weighted_error_H * el
        
            team_dict[home_team][1] = team_rate_HA + (weighted_error_H * el) * gamma
        
            team_dict[away_team][1] = team_rate_AA + weighted_error_A * el
        
            team_dict[away_team][0] = team_rate_AH + (weighted_error_A * el) * gamma

        # return either matrix with pi ratings or
        if (return_e==False) :
            return(team_dict)
        else:
            mean_sq_e = np.mean(np.power(abs_error, 2))
            return(mean_sq_e)


    def optimize_pi_ratings(self,teams , outcomes, el_in = np.arange(0.01, 0.25, 0.005),gamma_in = np.arange(0.01, 0.9, 0.005), 
                            b_in = 10, c_in = 3):
        el_seq_l = len(el_in)

        gamma_seq_l = len(gamma_in)
        minimum=100000
        best = {}
        current_el = 0

        current_gamma = 0

        result = 0

        result_array = np.zeros((el_seq_l,gamma_seq_l))
        # perform grid optimization
        for i1 in range(el_seq_l) :
            for i2 in range(gamma_seq_l): 
                current_el = el_in[i1]
                current_gamma = gamma_in[i2]
                result = self.calculate_pi_ratings(teams = teams,outcomes = outcomes,el = current_el,
                                            gamma = current_gamma, return_e = True)
                
                result_array[i1,i2] = result
                if result < minimum :
                    minimum=result
                    best["mean squared error"]=minimum
                    best["lambda"]=current_el
                    best["gamma"]=current_gamma 
            
        
        return best,result_array