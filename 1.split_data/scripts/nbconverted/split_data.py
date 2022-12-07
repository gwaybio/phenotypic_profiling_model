#!/usr/bin/env python
# coding: utf-8

# # Split feature data
# ## Create tsv file with indexes for held out data, training data, and testing data
# ### Import libraries

# In[1]:


import pandas as pd
import numpy as np
import pathlib

from sklearn.utils import shuffle

import sys
sys.path.append("../utils")
from split_utils import get_features_data


# ### Load data and set holdout/test parameters

# In[2]:


# load x (features) and y (labels) dataframes
load_path = pathlib.Path("../0.download_data/data/training_data.csv.gz")
training_data = get_features_data(load_path)
print(training_data.shape)

# ratio of data to be reserved for testing (ex 0.15 = 15%)
test_ratio = 0.15


# In[3]:


# test_data is pandas dataframe with test split, stratified by Mitocheck_Phenotypic_Class
test_data = training_data.groupby("Mitocheck_Phenotypic_Class", group_keys=False).apply(
    lambda x: x.sample(frac=test_ratio)
)
test_indexes = test_data.index
# remove test indexes
training_data = training_data.drop(pd.Index(data=test_indexes))

train_indexes = np.array(training_data.index)
print(training_data.shape)


# In[4]:


# create pandas dataframe with all indexes and their respective labels
index_data = []
for index in test_indexes:
    index_data.append({"label": "test", "index": index})
for index in train_indexes:
    index_data.append({"label": "train", "index": index})
index_data = pd.DataFrame(index_data)
index_data


# ### Save indexes

# In[5]:


# make results dir for saving
results_dir = pathlib.Path("indexes/")
results_dir.mkdir(parents=True, exist_ok=True)
# save indexes as tsv file
index_data.to_csv(f"{results_dir}/data_split_indexes.tsv", sep="\t")

