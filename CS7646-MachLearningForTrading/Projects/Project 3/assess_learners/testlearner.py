""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import math  		  	   		  		 			  		 			     			  	 
import sys  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np
import matplotlib.pyplot as plt	  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import DTLearner as dtl  
import RTLearner as rtl 
import BagLearner as bgl
  		  	   		  		 			  		 			     			  	 
def clean_csv(datafile):
    data = np.genfromtxt(datafile, delimiter=",")  		  	   		  		 			  		 			     			  	 
    if "Istanbul.csv" in datafile.name:  		  	   		  		 			  		 			     			  	 
        data = data[1:, 1:]
    return data 

def experiment_one():
    in_sample_rmse = np.asarray([], dtype=float)
    out_sample_rmse = np.asarray([], dtype=float)
    max_leaf_size = 100
    
    # Calculate in/out sample RSME values
    for leaf_size in range(1,max_leaf_size+1):
        learner = dtl.DTLearner(leaf_size, verbose=False)  
        learner.add_evidence(train_x, train_y) 		  	   		  		 			  		 			     			  	 
                                                                                        
        pred_y = learner.query(train_x)
        in_sample_rmse = np.append(in_sample_rmse, math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0]))		  	   		  		 			  		 			     			  	 
        		  	   		  		 			  		 			     			  	                                                   
        pred_y = learner.query(test_x)		  	   		  		 			  		 			     			  	 
        out_sample_rmse = np.append(out_sample_rmse, math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])) 		  	   		  		 			  		 			     			  	 
        		  	   		  		 			  		 			     					  		 			  		 			     			  	
    # Plot figure
    initialize_figure(title="Experiment 1 - DTLearner Overfitting", leaf_size=max_leaf_size, y_label="Root Square Mean Error (RSME)")
    plt.plot(in_sample_rmse, label="In sample - RSME")
    plt.plot(out_sample_rmse, label="Out of sample - RSME")
    plt.legend()
    plt.savefig("./images/Figure_1.png")

def experiment_two():
    in_sample_rmse = np.asarray([], dtype=float)
    out_sample_rmse = np.asarray([], dtype=float)
    max_leaf_size = 50
    
    # Calculate in/out sample RSME values
    for leaf_size in range(1,max_leaf_size+1):
        learner = bgl.BagLearner(learner=dtl.DTLearner, kwargs= {"leaf_size": leaf_size}, bags=20, boost=False, verbose=False)  
        learner.add_evidence(train_x, train_y) 		  	   		  		 			  		 			     			  	 
                                                                                        
        pred_y = learner.query(train_x)
        in_sample_rmse = np.append(in_sample_rmse, math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0]))		  	   		  		 			  		 			     			  	 
        		  	   		  		 			  		 			     			  	                                                   
        pred_y = learner.query(test_x)		  	   		  		 			  		 			     			  	 
        out_sample_rmse = np.append(out_sample_rmse, math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])) 		  	   		  		 			  		 			     			  	 

    # Plot figure
    initialize_figure(title="Experiment 2 - Bagging (DTLearner) Overfitting Effect", leaf_size=max_leaf_size, y_label="Root Square Mean Error (RSME)")  		  		 			  		 			     					  		 			  		 			     			  	
    plt.plot(in_sample_rmse, label="In sample - RSME")
    plt.plot(out_sample_rmse, label="Out of sample - RSME")
    plt.legend()
    plt.savefig("./images/Figure_2.png")

def experiment_three():
    max_leaf_size = 50
    
    # Calculate in/out sample mean absolute error values
    dtl_in_sample_mae, dtl_out_sample_mae, rtl_in_sample_mae, rtl_out_sample_mae = calculate_mean_absolute_error(max_leaf_size)
    
     # Plot figure
    initialize_figure(title="Experiment 3 - DTLearner vs. RTLearner - Mean Absolute Error", leaf_size=max_leaf_size, y_label="Mean Absolute Error (MAE)")  		  		 			  		 			     					  		 			  		 			     			  	
    plt.plot(dtl_in_sample_mae, label="In sample - MAE (DTLeaner)")
    plt.plot(dtl_out_sample_mae, label="Out of sample - MAE (DTLeaner)")
    plt.plot(rtl_in_sample_mae, label="In sample - MAE (RTLeaner)")
    plt.plot(rtl_out_sample_mae, label="Out of sample - MAE (RTLeaner)")
    plt.legend()
    plt.savefig("./images/Figure_3.png")

    # Calculate in/out sample mean absolute percentage error values
    dtl_in_sample_mape = dtl_in_sample_mae * 100
    dtl_out_sample_mape = dtl_out_sample_mae * 100
    rtl_in_sample_mape = rtl_in_sample_mae * 100
    rtl_out_sample_mape = rtl_out_sample_mae * 100

    # Plot figure
    initialize_figure(title="Experiment 3 - DTLearner vs. RTLearner - Mean Absolute Percentage Error", leaf_size=max_leaf_size, y_label="Mean Absolute Percentage Error (MAPE)")  		  		 			  		 			     					  		 			  		 			     			  	
    plt.plot(dtl_in_sample_mape, label="In sample - MAPE (DTLeaner)")
    plt.plot(dtl_out_sample_mape, label="Out of sample - MAPE (DTLeaner)")
    plt.plot(rtl_in_sample_mape, label="In sample - MAPE (RTLeaner)")
    plt.plot(rtl_out_sample_mape, label="Out of sample - MAPE (RTLeaner)")
    plt.legend()
    plt.savefig("./images/Figure_4.png")

    # Calculate in/out sample maximum error values
    dtl_in_sample_me, dtl_out_sample_me, rtl_in_sample_me, rtl_out_sample_me = calculate_maximum_error(max_leaf_size)
    
    # Plot figure
    initialize_figure(title="Experiment 3 - DTLearner vs. RTLearner - Maximum Error", leaf_size=max_leaf_size, y_label="Maximum Error (ME)")  		  		 			  		 			     					  		 			  		 			     			  	
    plt.plot(dtl_in_sample_me, label="In sample - ME (DTLeaner)")
    plt.plot(dtl_out_sample_me, label="Out of sample - ME (DTLeaner)")
    plt.plot(rtl_in_sample_me, label="In sample - ME (RTLeaner)")
    plt.plot(rtl_out_sample_me, label="Out of sample - ME (RTLeaner)")
    plt.legend()
    plt.savefig("./images/Figure_5.png", bbox_inches = "tight") # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html
    
def calculate_mean_absolute_error(max_leaf_size):
    dtl_in_sample_mae = np.asarray([], dtype=float)
    dtl_out_sample_mae = np.asarray([], dtype=float)
    rtl_in_sample_mae = np.asarray([], dtype=float)
    rtl_out_sample_mae = np.asarray([], dtype=float)

    for leaf_size in range(1,max_leaf_size+1):
        dtl_learner = dtl.DTLearner(leaf_size, verbose=False)  
        rtl_learner = rtl.RTLearner(leaf_size, verbose=False)  
        
        dtl_learner.add_evidence(train_x, train_y) 	
        rtl_learner.add_evidence(train_x, train_y) 		  	   		  		 			  		 			     			  	                                                                   
	  	   		  		 			  		 			     			  	 
        dtl_pred_y = dtl_learner.query(train_x)
        rtl_pred_y = rtl_learner.query(train_x)

        # https://www.geeksforgeeks.org/how-to-calculate-mean-absolute-error-in-python/
        dtl_in_sample_mae = np.append(dtl_in_sample_mae, np.sum(np.abs(train_y - dtl_pred_y)) / train_y.shape[0])
        rtl_in_sample_mae = np.append(rtl_in_sample_mae, np.sum(np.abs(train_y - rtl_pred_y)) / train_y.shape[0])		  	   		  		 			  		 			     			  	 
	
        dtl_pred_y = dtl_learner.query(test_x)
        rtl_pred_y = rtl_learner.query(test_x)		  	   		  		 			  		 			     			  	 
		  	   		  		 			  		 			     			  	 
        dtl_out_sample_mae = np.append(dtl_out_sample_mae, np.sum(np.abs(test_y - dtl_pred_y)) / test_y.shape[0])  	   		  		 			  		 			     			  	 
        rtl_out_sample_mae = np.append(rtl_out_sample_mae, np.sum(np.abs(test_y - rtl_pred_y)) / test_y.shape[0]) 	  	   		  		 			  		 			     			  	 
     		  	   		  		 			  		 			     			  	                                              		  	   		  		 			  		 			     				  	   		  		 			  		 			     					  		 			  		 			     			  	 
    return dtl_in_sample_mae, dtl_out_sample_mae, rtl_in_sample_mae, rtl_out_sample_mae

def calculate_maximum_error(max_leaf_size):
    dtl_in_sample_me = np.asarray([], dtype=float)
    dtl_out_sample_me = np.asarray([], dtype=float)
    rtl_in_sample_me = np.asarray([], dtype=float)
    rtl_out_sample_me = np.asarray([], dtype=float)

    for leaf_size in range(1,max_leaf_size+1):
        dtl_learner = dtl.DTLearner(leaf_size, verbose=False)  
        rtl_learner = rtl.RTLearner(leaf_size, verbose=False)  
        
        dtl_learner.add_evidence(train_x, train_y) 	
        rtl_learner.add_evidence(train_x, train_y) 		  	   		  		 			  		 			     			  	                                                                   
	  	   		  		 			  		 			     			  	 
        dtl_pred_y = dtl_learner.query(train_x)
        rtl_pred_y = rtl_learner.query(train_x)

        # https://www.mydatamodels.com/learn/guide/a-path-to-discover-ai/regression-algorithms-which-machine-learning-metrics/
        dtl_in_sample_me = np.append(dtl_in_sample_me, np.max(np.abs(train_y - dtl_pred_y)))
        rtl_in_sample_me = np.append(rtl_in_sample_me, np.max(np.abs(train_y - rtl_pred_y)))		  	   		  		 			  		 			     			  	 
	
        dtl_pred_y = dtl_learner.query(test_x)
        rtl_pred_y = rtl_learner.query(test_x)		  	   		  		 			  		 			     			  	 
		  	   		  		 			  		 			     			  	 
        dtl_out_sample_me = np.append(dtl_out_sample_me, np.max(np.abs(test_y - dtl_pred_y)))  	   		  		 			  		 			     			  	 
        rtl_out_sample_me = np.append(rtl_out_sample_me, np.max(np.abs(test_y - rtl_pred_y))) 	  	   		  		 			  		 			     			  	 
     		  	   		  		 			  		 			     			  	                                              		  	   		  		 			  		 			     				  	   		  		 			  		 			     					  		 			  		 			     			  	 
    return dtl_in_sample_me, dtl_out_sample_me, rtl_in_sample_me, rtl_out_sample_me

def initialize_figure(title, leaf_size, y_label):
    plt.figure()
    plt.title(title)    
    plt.xlim(0,leaf_size)
    plt.xlabel("Leaf Size")
    plt.ylabel(y_label)

if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    # Set random seed
    np.random.seed(903648648) 

    if len(sys.argv) != 2:  		  	   		  		 			  		 			     			  	 
        print("Usage: python testlearner.py <filename>")  		  	   		  		 			  		 			     			  	 
        sys.exit(1)  		  	   		  		 			  		 			     			  	 
    inf = open(sys.argv[1])
    inf_clean = clean_csv(inf)
    data = inf_clean
  		  		 			  		 			     			  	   	   		  		 			  		 			     			  	
    # compute how much of the data is training and testing  		  	   		  		 			  		 			     			  	 
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows
    
    # select random train rows
    random_train_rows = np.random.choice(data.shape[0], size=train_rows, replace=False)
    
    # select remaining rows in the data array
    # https://numpy.org/doc/stable/reference/generated/numpy.setdiff1d.html
    # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
    random_test_rows = np.setdiff1d(np.arange(data.shape[0]), random_train_rows)
      	   		  		 			  		 			     			  	 
    # separate out training and testing data  		  	   		  		 			  		 			     			  	 
    train_x = data[random_train_rows, 0:-1]
    train_y = data[random_train_rows, -1]  		  	   		  		 			  		 			     			  	 
    test_x = data[random_test_rows, 0:-1]  		  	   		  		 			  		 			     			  	 
    test_y = data[random_test_rows, -1]

    # Plot Experiment 1
    experiment_one() 

    # Plot Experiment 2
    experiment_two()	  

    # Plot Experiment 3
    experiment_three()       		  		 			  		 			     			  	   		  		 			  		 			     			  	 		  		 			     					  	   		  		 			  		 			     			