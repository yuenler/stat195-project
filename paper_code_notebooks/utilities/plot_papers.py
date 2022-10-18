import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#plt.rcParams['axes.facecolor']= 'efeae1'
class plot_papers:
    
    
    def plot_tournament_per_model(self, evaluation_results, title, metric, loc=0, ylimit=0.35):
        models = ['Logistic Regression', 'Random Forest', 'XGBoost', 'Ensemble Learning']
        tournaments = ['Euroleague', 'Eurocup','Greek Basket League', 'Liga ACB']
        colors = ['tab:blue','tab:red','tab:orange','tab:green']
        #linestyles = ['-', '--', '-.', ':']
        markers = ['o','s','v','^']
        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)


        for i in range(len(evaluation_results)):
            ax.plot(models,evaluation_results[i],'o',label=tournaments[i],color=colors[i],#linewidth=4,linestyle= linestyles[i],
                    marker=markers[i],markersize=12)



        ax.set_title(title, fontsize=30)
        ax.set_ylabel(metric, fontsize=20)
        ax.set_xlabel('Predictive Models', fontsize=20)
        ax.legend(loc=loc,prop={'size': 18})
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        ax.xaxis.set_tick_params(labelsize=20)
        ax.yaxis.set_tick_params(labelsize=20)
        plt.ylim(top=ylimit)
        
        return plt
    
    def bar_plot_tournament_per_model(self, evaluation_results, title, metric, loc=0, ylimit=0.35):
        
        evaluation_results = np.array(evaluation_results).transpose()
        
        models = ['Logistic Regression', 'Random Forest', 'XGBoost', 'Ensemble Learning']
        tournaments = [ 'Euroleague', 'Eurocup','Greek Basket League', 'Liga ACB']
        colors = ['tab:purple','tab:brown','tab:pink','tab:green']


        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)

        index = np.arange(0,8,2)
        space = 0
        for i in range(len(evaluation_results)):
            ax.bar(index+space,evaluation_results[i],label=models[i],color=colors[i],width = 0.25)
            space += 0.25


        ax.set_title(title, fontsize=30)
        ax.set_ylabel(metric, fontsize=20)
        ax.set_xlabel('Tournaments', fontsize=20)
        ax.legend(loc=loc,prop={'size': 18})
        plt.xticks(index + 0.25*1.5, tournaments,fontsize=20)
        plt.yticks(fontsize=20)
        ax.xaxis.set_tick_params(labelsize=20)
        ax.yaxis.set_tick_params(labelsize=20)
        plt.ylim(top=ylimit)
        
        return plt
    
    def bar_plot_difference_baseline_full_information_model(self, differences, title, loc=0, ylimit=0.35):
        
        differences = np.array(differences)
        
        metrics = ['Brier Score' , 'Accuracy' , 'F1-Score']
        tournaments = ["Euroleague","Eurocup","Greek Basket League","Liga ACB"]
        colors = ['tab:orange','tab:red','tab:blue','tab:cyan']

        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)


        index = np.arange(0,6,2)
        space = 0
        for i in range(len(tournaments)):
            ax.bar(index+space,differences[:,i],label=tournaments[i],color= colors[i], width = 0.25)
            space += 0.25

        ax.set_title(title, fontsize=30)
        ax.set_ylabel('Differences Of Values', fontsize=20)
        ax.set_xlabel('Metrics', fontsize=20)
        ax.legend(loc=loc, prop={'size': 18})
        plt.xticks(index + 0.25*1.5, metrics,fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(top=ylimit)
        ax.xaxis.set_tick_params(labelsize=20)
        
        return plt
    
    def plot_difference_baseline_full_information_model(self, differences, title, loc=0, ylimit=0.35):
        
        metrics = ['Brier Score' , 'Accuracy' , 'F1-Score']
        tournaments = ["Euroleague","Eurocup","Greek Basket League","Liga ACB"]
        colors = ['tab:red','tab:blue','tab:green']
        #colors = ['tab:purple','tab:cyan','tab:olive']
        #linestyles = ['-', '--', ':']
        markers = ['o','s','v']

        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)



        for i in range(len(differences)):
            ax.plot(tournaments,differences[i],'o',label=metrics[i],color=colors[i],#linewidth=4,linestyle= linestyles[i],
                    marker=markers[i],markersize=12)



        ax.set_title(title, fontsize=30)
        ax.set_ylabel('Differences Of Values', fontsize=20)
        ax.set_xlabel('Tournaments', fontsize=20)
        ax.legend(loc=loc, prop={'size': 18})
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(top=ylimit)
        ax.xaxis.set_tick_params(labelsize=20)
        
        return plt
    
    def barplot_comparison_train_set(self, full_greek_all, full_greek_same,full_spain_all,full_spain_same ,full_euroleague_all,
                                     full_euroleague_same,full_eurocup_all,full_eurocup_same, 
                                     baseline_greek_all,baseline_greek_same,
                                     baseline_spain_all, baseline_spain_same, baseline_euroleague_all ,
                                     baseline_euroleague_same, baseline_eurocup_all, baseline_eurocup_same, 
                                     title, metric, season,loc=0,letters_position=0.05, ylimit=0.35):
        
        full_greek_all_mean = np.mean(full_greek_all)
        full_greek_same_mean = np.mean(full_greek_same)
        full_spain_all_mean = np.mean(full_spain_all)
        full_spain_same_mean = np.mean(full_spain_same)
        full_euroleague_all_mean = np.mean(full_euroleague_all)
        full_euroleague_same_mean = np.mean(full_euroleague_same)
        full_eurocup_all_mean = np.mean(full_eurocup_all)
        full_eurocup_same_mean = np.mean(full_eurocup_same)


        baseline_greek_all_mean = np.mean(baseline_greek_all)
        baseline_greek_same_mean = np.mean(baseline_greek_same)
        baseline_spain_all_mean = np.mean(baseline_spain_all)
        baseline_spain_same_mean = np.mean(baseline_spain_same)
        baseline_euroleague_all_mean = np.mean(baseline_euroleague_all)
        baseline_euroleague_same_mean = np.mean(baseline_euroleague_same)
        baseline_eurocup_all_mean = np.mean(baseline_eurocup_all)
        baseline_eurocup_same_mean = np.mean(baseline_eurocup_same)
        
        
        full_greek_all_std = np.std(full_greek_all)
        full_greek_same_std = np.std(full_greek_same)
        full_spain_all_std = np.std(full_spain_all)
        full_spain_same_std = np.std(full_spain_same)
        full_euroleague_all_std = np.std(full_euroleague_all)
        full_euroleague_same_std = np.std(full_euroleague_same)
        full_eurocup_all_std = np.std(full_eurocup_all)
        full_eurocup_same_std = np.std(full_eurocup_same)


        baseline_greek_all_std = np.std(baseline_greek_all)
        baseline_greek_same_std = np.std(baseline_greek_same)
        baseline_spain_all_std = np.std(baseline_spain_all)
        baseline_spain_same_std = np.std(baseline_spain_same)
        baseline_euroleague_all_std = np.std(baseline_euroleague_all)
        baseline_euroleague_same_std = np.std(baseline_euroleague_same)
        baseline_eurocup_all_std = np.std(baseline_eurocup_all)
        baseline_eurocup_same_std = np.std(baseline_eurocup_same)
        
        
        
        full_all_train_mean = [full_euroleague_all_mean,full_eurocup_all_mean, full_greek_all_mean,full_spain_all_mean]
        
        full_same_year_train_mean = [full_euroleague_same_mean,full_eurocup_same_mean, full_greek_same_mean,full_spain_same_mean]

        baseline_all_train_mean = [baseline_euroleague_all_mean, baseline_eurocup_all_mean,
                                   baseline_greek_all_mean,baseline_spain_all_mean]
        
        baseline_same_year_train_mean = [baseline_euroleague_same_mean, baseline_eurocup_same_mean, 
                                         baseline_greek_same_mean,baseline_spain_same_mean]
        
        full_all_train_std = [full_euroleague_all_std,full_eurocup_all_std, full_greek_all_std,full_spain_all_std]
        full_same_year_train_std = [full_euroleague_same_std,full_eurocup_same_std, full_greek_same_std,full_spain_same_std]

        baseline_all_train_std = [baseline_euroleague_all_std,baseline_eurocup_all_std, baseline_greek_all_std,baseline_spain_all_std]
        baseline_same_year_train_std =[baseline_euroleague_same_std,
                                       baseline_eurocup_same_std,baseline_greek_same_std,baseline_spain_same_std]
        
        n_groups = 4
        fig, ax = plt.subplots(figsize=(15,8))
        index = index = np.arange(n_groups)
        bar_width = 0.15
        opacity = 0.8

        rects1 = plt.bar(index, full_all_train_mean,yerr=full_all_train_std, width = bar_width,alpha=opacity,
                         color='blue',label='(a) Full Information Model All years',ecolor='black',capsize=10)

        rects2 = plt.bar(index+bar_width, full_same_year_train_mean,yerr=full_same_year_train_std, width = bar_width,
                 alpha=opacity,color='royalblue',label='(b) Full Information Model '+season,ecolor='black',capsize=10)


        rects3 = plt.bar(index+2*bar_width, baseline_all_train_mean,yerr=baseline_all_train_std, width = bar_width,
                 alpha=opacity,color='green',label='(c) Baseline All years',ecolor='black',capsize=10)

        rects4 = plt.bar(index+3*bar_width, baseline_same_year_train_mean,yerr=baseline_same_year_train_std, 
                 width = bar_width,alpha=opacity,color='seagreen',label='(d) Baseline '+season,ecolor='black',capsize=10)

        plt.xlabel('Tournament',fontsize=20)
        plt.ylabel(metric,fontsize=20)
        plt.title(title,fontsize=30)
        plt.xticks(index + bar_width*1.5, ("Euroleague","Eurocup", "Greek Basket League","Liga ACB" ))
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(top=ylimit)
        plt.legend(loc=loc,prop={'size': 18})
        ax.tick_params(axis='both', which='major', pad=20)

        plt.tight_layout()
        
        rects = ax.patches

        # Make some labels.
        labels = ['(a)']*4 + ['(b)']*4 + ['(c)']*4+['(d)']*4

        for rect, label in zip(rects, labels):
            #height = rect.get_x()
            ax.text(rect.get_x() + rect.get_width() / 2,letters_position, label, color = 'black',
                    ha='center', va='bottom', size=14)
        
        return plt
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        