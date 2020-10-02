#!/usr/bin/env python
# coding: utf-8

# # A Minimalist Submission -- one-hot encoding and CV blending
# Stripped down to essentials, these 21 lines are all you need to break into the top 20% on the leaderboard. I'll start by presenting the bare code for you to figure out on your own, and then explain it in detail down below.
# 
# This is both a follow-up to my previous "19 lines for top 50%" kernel, and an attempt to replicate -- in compact form -- [a successful kernel by Peter Hurford](https://www.kaggle.com/peterhurford/why-not-logistic-regression). This kernel replaces the target encoding of my earlier kernel with sparse one-hot encoding. Though lower-scoring with untuned LinearRegression, this encoding responds much better to two optimizations: changing the C parameter, and performing CV blending.

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

Xy_train = pd.read_csv("../input/cat-in-the-dat/train.csv", index_col="id")
X_train = Xy_train.drop(columns=["target"])
y_train = Xy_train["target"]
X_test = pd.read_csv("../input/cat-in-the-dat/test.csv", index_col="id")

X_comb_onehot = pd.get_dummies(pd.concat([X_train, X_test]), sparse=True, columns=X_train.columns)
X_train_sparse = X_comb_onehot.loc[y_train.index].sparse.to_coo().tocsr()
X_test_sparse = X_comb_onehot.drop(index=y_train.index).sparse.to_coo().tocsr()

lr_params = dict(solver="lbfgs", C=0.2, max_iter=5000, random_state=0)
models = [LogisticRegression(**lr_params).fit(X_train_sparse[t], y_train[t])
          for t, _ in KFold(5, random_state=0).split(X_train_sparse)]
predictions = np.average([model.predict_proba(X_test_sparse)[:, 1] for model in models], axis=0)

output = pd.DataFrame({"id": X_test.index, "target": predictions})
output.to_csv("submission.csv", index=False)


# ## The code, explained:
# In addition to pandas for data loading and pre-processing, and `LogisticRegression` for the actual classification, we must import numpy and `KFold` to perform CV blending.
# ```
# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import KFold
# ```
# Here we read in the data and separate out the target values from the features. There are no missing values for this particular data set, so no imputation is required.
# ```
# Xy_train = pd.read_csv("../input/cat-in-the-dat/train.csv", index_col="id")
# X_train = Xy_train.drop(columns=["target"])
# y_train = Xy_train["target"]
# X_test = pd.read_csv("../input/cat-in-the-dat/test.csv", index_col="id")
# ```
# For one hot encoding, we must combine together the train and test sets, in order to ensure that train and test end up with identical sets of columns. `pd.get_dummies` then does all the real work, with `sparse=True` insuring that >16,000 resulting columns fit into memory. Alas, with all of those columns to manage, the process is fairly slow -- taking 4 minutes on my machine.
# 
# We then split them apart before using the mystic incantation `.sparse.to_coo().tocsr()` to convert to a format that LinearRegression can handle natively without having to desparsificate the data.
# ```
# X_comb_onehot = pd.get_dummies(pd.concat([X_train, X_test]), sparse=True, columns=X_train.columns)
# X_train_sparse = X_comb_onehot.loc[y_train.index].sparse.to_coo().tocsr()
# X_test_sparse = X_comb_onehot.drop(index=y_train.index).sparse.to_coo().tocsr()
# ```
# Here we train 5 instances of LogisticRegression based upon 5 cross-validation folds. We then evaluate all 5 instances and average their "proba" likelihoods, producing a blended prediction. The `C=0.2` classifier parameter is important. We could probably use anything from 0.1 to 0.3, but the default of 1.0 is too high for this encoded data.
# ```
# lr_params = dict(solver="lbfgs", C=0.2, max_iter=5000, random_state=0)
# models = [LogisticRegression(**lr_params).fit(X_train_sparse[t], y_train[t])
#           for t, _ in KFold(5, random_state=0).split(X_train_sparse)]
# predictions = np.average([model.predict_proba(X_test_sparse)[:, 1] for model in models], axis=0)
# ```
# Now we simply write out the predictions, submit, and profit.
# ```
# output = pd.DataFrame({"id": X_test.index, "target": predictions})
# output.to_csv("submission.csv", index=False)
# ```
