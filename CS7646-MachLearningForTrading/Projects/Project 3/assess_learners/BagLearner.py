""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
class BagLearner(object):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This is a Bag Learner.  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    def __init__(self, learner, kwargs={}, bags=20, boost=False, verbose=False):  		  	   		  		 			  		 			     			  	 
        self.learner_collection = [learner(**kwargs) for b in range(bags)]
        self.boost = boost
        self.verbose = verbose
	  	   		  		 			  		 			     			  	   		  	   		  		 			  		 			     			  	 
    def author(self):  		  	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
        return "manderson332" 		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    def add_evidence(self, data_x, data_y):  		  	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
        if self.boost:
            pass # TODO: Implement if time permits
        else:
            train_data = data_x.shape[0]
            for leaner in self.learner_collection:
                # https://numpy.org/doc/stable/reference/random/generated/numpy.random.choice.html
                n_prime = np.random.choice(train_data, size=train_data, replace=True)
                sample_x_data, sample_y_data = data_x[n_prime], data_y[n_prime]
                leaner.add_evidence(sample_x_data, sample_y_data)           
  		  	   		  		 			  		 			     			  	 
    def query(self, points):  		  	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
        predicted_points = [learner.query(points) for learner in self.learner_collection]
        return np.mean(predicted_points, axis=0)	  	   		  		 			  		 			     			  	    		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    print("the secret clue is 'zzyzx'")  		  	   		  		 			  		 			     			  	 
