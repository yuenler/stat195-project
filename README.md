# Predictions of European Basketball Match Results with Machine Learning Algorithms


## Paper Abstract 
The goal of this paper is to build and compare methods for the prediction of the final outcomes of basketball games. 
    In this study, we analyze data from four different European tournaments: Euroleague, Eurocup, Greek Basket League and Spanish Liga ACB. The data-set consists of information collected by box scores of 5214 games for the period of  2013-2018. The predictions obtained by our implemented methods and models were compared with a “vanilla” model using only the team-name information of each game. In our analysis, we have included new performance indicators constructed by using historical statistics, key performance indicators and measurements from three rating systems (Elo,PageRank, pi-rating). For these three rating systems and every tournament under consideration,  we tune the rating system parameters using specific training data-sets.
    These new game features are improving our predictions efficiently and can be easily obtained in any basketball league. Our predictions were obtained by implementing three different statistics and machine learning algorithms: logistic regression, random forest, and extreme gradient boosting trees. Moreover,  we report predictions based on the combination of these algorithms (ensemble learning). We evaluate our predictions using three predictive measures: Brier Score, accuracy and $F_1$-score. In addition, we evaluate the performance of our algorithms with three different prediction scenarios (full-season, mid-season, and play-offs predictive evaluation). For the mid-season and the play-offs scenarios, we further explore whether incorporating additional results from previous seasons in the learning data-set enhances the predictive performance of the implemented models and algorithms. 
    Concerning the results, there is no clear winner between the machine learning algorithms since they provide identical predictions with small differences. However, models with predictors suggested in this paper out-perform the “vanilla” model by 3-5\% in terms of accuracy. 
    Another conclusion from our results for the play-offs scenarios is that it is not necessary to embed outcomes from previous seasons in our training data-set.  Using data from the current season, most of the time leads to efficient, accurate parameter learning and well-behaved prediction models. 
    Moreover, the Greek league is the less balanced tournament in terms of competitiveness since all our models achieve high predictive accuracy (78\% at the best-performed model). 
    The second less balanced league is the Spanish one with accuracy reaching 72\% while for the two European tournaments the prediction accuracy is considerably lower (about 69\%). 
    Finally, we present the most important features by counting the percentage of appearance in every machine learning algorithm for every one of the three analyses. From this analysis, we may conclude that the best predictors are the rating systems (pi-rating, PageRank, and ELO) and the current form performance indicators (e.g., the two most frequent ones are the game score of Hollinger and the floor impact counter). 
    
    
## DATA AND CODE

All data used in this article have been kindly provided to the authors by the Greek Organization of Football Prognostics (OPAP). 
Due to confidentiality reasons, we cannot publicly provide access to the actual data-set of this study. 


For this reason, we provide the code and an alternative data-set obtained via scrapping to this Git repository of the article. 
More specifically, in the Git repository you can find two sets of code and files: one referring to the paper implementation (with no data available) and a second one with an implementation to the crawled data obtained by https://www.basketball-reference.com/. 
For the crawled data-set we obtained results from  eight tournaments including the ones presented in this work (Greek league, Liga ACB, Euroleague and Eurocup) for a period of five years: 2014/10/04-2020/06/30.  


This Git repository contains data, along with Python code and Jupyter notebooks for the pre-processing of the data and for the tuning of the hyper-parameters for all algorithms. 
Moreover, two main modelling approaches have been implemented: one with  Baseline Vanilla Model and a second one using the Full Information Model. 
For the analyses with the publicly available data, we have specified the training data-set by considering results from four seasons (2014--2018) while season 2018/19 was used for evaluating the prediction efficiency of the methods.  
