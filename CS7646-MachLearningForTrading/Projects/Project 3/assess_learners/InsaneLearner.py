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
import BagLearner as bgl
import LinRegLearner as lrl		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	    		  		 			  		 			     			  	 
class InsaneLearner(object):  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    def __init__(self, verbose=False, **kwargs):  		  	   		  		 			  		 			     			  	 
        self.learner_collection = [bgl.BagLearner(lrl.LinRegLearner, kwargs, 20) for b in range(20)]
        self.verbose = verbose	  		 			     			  	    		  		 			  		 			     			  	 
    def author(self):  		  	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
        return "manderson332" 		  	   		  		 			  		 			     			  	  	   		  		 			  		 			     			  	 
    def add_evidence(self, data_x, data_y):  		  	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
        for leaner in self.learner_collection: leaner.add_evidence(data_x, data_y)            	   		  		 			  		 			     			  	 
    def query(self, points):  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
        predicted_points = [learner.query(points) for learner in self.learner_collection]
        return np.mean(predicted_points, axis=0)	 			  		 			     			  	 	  	   		  		 			  		 			     			  	   	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    print("the secret clue is 'zzyzx'")
    """  		  	   		  		 			  		 			     			  	 
    This is a Insane Learner.		  	   		  		 			  		 			     			  	   	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 