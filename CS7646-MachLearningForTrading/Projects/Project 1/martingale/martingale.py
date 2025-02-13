""""""  		  	   		  		 			  		 			     			  	 
"""Assess a betting strategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Student Name: Marcus Anderson(replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: manderson332 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 903648648 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np
import matplotlib.pyplot as plt	  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
    :rtype: str  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return "manderson332"  # replace tb34 with your Georgia Tech username.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def gtid():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT ID of the student  		  	   		  		 			  		 			     			  	 
    :rtype: int  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return 903648648  # replace with your GT ID number  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def get_spin_result(win_prob):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		  		 			  		 			     			  	 
    :type win_prob: float  		  	   		  		 			  		 			     			  	 
    :return: The result of the spin.  		  	   		  		 			  		 			     			  	 
    :rtype: bool  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    result = False  		  	   		  		 			  		 			     			  	 
    if np.random.random() <= win_prob:  		  	   		  		 			  		 			     			  	 
        result = True  		  	   		  		 			  		 			     			  	 
    return result 

def simple_simluator(total_episodes):    
    spin_winnings = np.empty((total_episodes, 1001), int)
    for episode_num in range(total_episodes):
        episode_winnings = 0
        spin_num = 1
        spin_results = np.zeros(1001, int)
        while spin_num <= 1000:
            bet_won = False
            bet_amount = 1
            while bet_won == False and spin_num <= 1000:
                if episode_winnings < 80:
                    bet_won = get_spin_result(0.47)
                    if bet_won == True:
                        episode_winnings += bet_amount
                    else:
                        episode_winnings -= bet_amount
                        bet_amount *= 2
                spin_results[spin_num] = episode_winnings
                spin_num +=1
        spin_winnings[episode_num] = spin_results
    return spin_winnings

def realistic_simluator(total_episodes, bank_roll):    
    spin_winnings = np.empty((total_episodes, 1001), int)
    for episode_num in range(total_episodes):
        episode_winnings = 0
        spin_num = 1
        spin_results = np.zeros(1001, int)
        while spin_num <= 1000:
            bet_won = False
            bet_amount = 1
            while bet_won == False and spin_num <= 1000:
                if -bank_roll < episode_winnings < 80:
                    bet_amount = determine_bet_amount(episode_winnings, bet_amount, -bank_roll)
                    bet_won = get_spin_result(0.47)
                    if bet_won == True:
                        episode_winnings += bet_amount
                    else:
                        episode_winnings -= bet_amount
                        bet_amount *= 2
                spin_results[spin_num] = episode_winnings
                spin_num +=1
        spin_winnings[episode_num] = spin_results
    return np.array(spin_winnings)		  		 			     			  	 

def determine_bet_amount(rem_cash, bet, bank_roll_limit):
    return bet if rem_cash - bet > bank_roll_limit else abs(bank_roll_limit) - abs(rem_cash)

def initialize_figure(title):
    plt.figure()
    plt.title(title)    
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel("Spin Number")
    plt.ylabel("Winnings")

def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Method to test your code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    np.random.seed(gtid())  # do this only once  		  	   		  		 			  		 			     			  	 
    # add your code here to implement the experiments

    # Experiment 1
    
    # Episode variables
    ten_episodes = simple_simluator(10)
    one_thousand_episodes = simple_simluator(1000)
    
    # Statistics variables
    episode_means = np.mean(one_thousand_episodes, axis = 0)
    episode_medians = np.median(one_thousand_episodes, axis = 0)
    episode_standard_deviations = np.std(one_thousand_episodes, axis = 0)

    # Experiment 1 - Figure 1
    initialize_figure("Figure 1")

    # Plot
    for i in range(10):
        plt.plot(ten_episodes[i], label = "Episode " + str(i+1))

    plt.legend()
    plt.savefig("./images/Figure_1.png")

    # Experiment 1 - Figure 2 
    initialize_figure("Figure 2")

    # Plot
    episode_means_plus_std = episode_means + episode_standard_deviations
    episode_means_minus_std = episode_means - episode_standard_deviations
    plt.plot(episode_means, label = "Mean")
    plt.plot(episode_means_plus_std, label = "Mean + SD")
    plt.plot(episode_means_minus_std, label = "Mean - SD")

    plt.legend()
    plt.savefig("./images/Figure_2.png")

    # Experiment 1 - Figure 3   
    initialize_figure("Figure 3")

    # Plot
    medians_plus_std = episode_medians + episode_standard_deviations
    medians_minus_std = episode_medians - episode_standard_deviations
    plt.plot(episode_medians, label = "Median")
    plt.plot(medians_plus_std, label = "Median + SD")
    plt.plot(medians_minus_std, label = "Median - SD")

    plt.legend()
    plt.savefig("./images/Figure_3.png")

    
    # Experiment 2

    # Episode variables
    one_thousand_episodes = realistic_simluator(1000,256)

    # Statistics variables
    episode_means = np.mean(one_thousand_episodes, axis = 0)
    episode_medians = np.median(one_thousand_episodes, axis = 0)
    episode_standard_deviations = np.std(one_thousand_episodes, axis = 0)

    # Experiment 2 - Figure 4
    initialize_figure("Figure 4")

    # Plot
    episode_means_plus_std = episode_means + episode_standard_deviations
    episode_means_minus_std = episode_means - episode_standard_deviations
    plt.plot(episode_means, label = "Mean")
    plt.plot(episode_means_plus_std, label = "Mean + SD")
    plt.plot(episode_means_minus_std, label = "Mean - SD")

    plt.legend()
    plt.savefig("./images/Figure_4.png")

    # Experiment 2 - Figure 5
    initialize_figure("Figure 5")

    # Plot
    medians_plus_std = episode_medians + episode_standard_deviations
    medians_minus_std = episode_medians - episode_standard_deviations
    plt.plot(episode_medians, label = "Median")
    plt.plot(medians_plus_std, label = "Median + SD")
    plt.plot(medians_minus_std, label = "Median - SD")
    
    plt.legend()
    plt.savefig("./images/Figure_5.png")
	  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 