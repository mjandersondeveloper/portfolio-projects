""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
Note, this is NOT a correct DTLearner; Replace with your own implementation.  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
Student Name: Marcus Anderson (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: manderson332 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 903648648 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	   		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
class DTLearner(object):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This is a decision tree learner object that is implemented incorrectly. You should replace this DTLearner with  		  	   		  		 			  		 			     			  	 
    your own correct DTLearner from Project 3.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param leaf_size: The maximum number of samples to be aggregated at a leaf, defaults to 1.  		  	   		  		 			  		 			     			  	 
    :type leaf_size: int  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    def __init__(self, leaf_size=1, verbose=False):  		  	   		  		 			  		 			     			  	 
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = np.array([])

    def author(self):  		  	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
        return "manderson332"  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    def add_evidence(self, data_x, data_y):  		  	   		  		 			  		 			     			  	 
        # Add Ytrain as the last column in the Xtrain array
        # https://numpy.org/doc/stable/reference/generated/numpy.reshape.html
        combined_data = np.append(data_x, np.reshape(data_y, (-1,1)), axis=1)
        self.tree = self.build_tree(combined_data, self.leaf_size)
  		  	   	  		 			  		 			     			  	 
    def query(self, points):  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
        return np.asarray([self.predicted_points(point, 0) for point in points]) 		  	   		  		 			  		 			     			  	 

    def build_tree(self, data, leaf_size):
        if data.shape[0] <= leaf_size or len(np.unique(data[:,-1])) == 1:
            return self.set_leaf(data)
        else:
            # https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html
            correlations = np.asarray([np.corrcoef(data[:,i], data[:,-1])[0,1] for i in range(data.shape[1] - 1)])
            np.seterr(invalid='ignore')

            # https://numpy.org/doc/stable/reference/generated/numpy.nanargmax.html
            feature_index = np.nanargmax(np.abs(correlations))
            split_val = np.median(data[:,feature_index])

            left_split = data[:,feature_index] <= split_val
            # Extra kill condition, check if all split_vals are in the left subtree
            if np.sum(left_split == False) == 0:
                return self.set_leaf(data)
            left_tree = self.build_tree(data[left_split], leaf_size)

            right_split = data[:,feature_index] > split_val
            right_tree = self.build_tree(data[right_split], leaf_size)

            root = np.asarray([[feature_index, split_val, 1, left_tree.shape[0] + 1]], dtype=object)

            # https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html
            return np.concatenate((root, left_tree, right_tree), axis=0)

    def set_leaf(self, data):
        return np.asarray([["leaf", data[:,-1][0], None, None]], dtype=object)

    def predicted_points(self, point, node):
        # https://edstem.org/us/courses/32834/discussion/2541009
        if (self.tree[node, 0]) == "leaf":
            return self.tree[node, 1]
        
        left_right_tree_val = 2 if point[self.tree[node, 0]] <= self.tree[node, 1] else 3
        next_node = node + self.tree[node, left_right_tree_val]
    
        return self.predicted_points(point, next_node)   	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    print("the secret clue is 'zzyzx'")  		  	   		  		 			  		 			     			  	 
