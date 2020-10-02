#!/usr/bin/env python
# coding: utf-8

# # **Synopsis of this EDA**
# So, this seems to be a pretty difficult data set. I'm just getting started with Kaggle kernels and competitions and still getting used to dealing with big data sets. Most of the work that went into this kernel was figuring out how to manage a large data set and create useful features while not exceeding memory limits. Slowly but surely, I'm learning how to do this.
# 
# As for the difficulty of this data set, it has another aspect. If the data are useful and effective in distinguishing positive from negative samples, it seems we should, with good visualization, be able to see some basic hallmarks that help distinguish the positive examples. Sure, machine learning models are far more powerful than our eyes to discern differences, but I thought I'd at least be able to see something.
# 
# After all the effort, I haven't been able to see differences. I did some rolling means on the data to smooth the samples, and thought I might be able to see some different low-frequency components between negative and positive examples. As this kernel shows, the smoothed samples look quite identical when viewing several negative and positive examples.
# 
# I then thought I would look at higher frequency components (i.e. components that were eliminated by the mean-based smoothing) by using FFT. These are shown in the second set of visualizations at the end of the kernel. Here again, though, I can't pick out differences. I thought there might be some common peaks among positive examples that set them apart from the negative examples. But, no luck. Anyway, has anyone else had more luck with good feature engineering and visualization that reveals differences in the positive examples?

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
from tqdm import tqdm

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # **Function Definitions**
# ## *Get column ids based on specified filter criteria*
# If fiter_criteria is specified, it should be a dictionary where the keys are one or more metadata column names and the values are single integer values or lists of integers. For example, the following would select rows for 'id_measurement' values 0, 1, 2, 3, and 4 (for a total of 15 rows, since each id_measurement has three phases):
# 
#     filter_criteria = {'id_measurement' : list(range(5))}
# 
# The following would select rows for positive examples only:
# 
#     filter_criteria = {'target' : 1}

# In[ ]:


# Function to select column ids using filter criteria
# Return the column ids and the corresponding metadata
# If filter_criteria is None, get all column ids
def load_metadata_by_filter(dataset_type = 'train', filter_criteria=None):
    # Set paths according to dataset type
    if(dataset_type == 'test'):
        metadata_filepath = '../input/metadata_test.csv'
        data_filepath = '../input/test.parquet'
    else:
        metadata_filepath = '../input/metadata_train.csv'
        data_filepath = '../input/train.parquet'
    # Load metadata
    metadata = pd.read_csv(metadata_filepath)
    # Initialize a filter mask
    filter_mask = [True]*metadata.shape[0]
    # If filter criteria are specified, loop over criteria and generate filter mask
    if(filter_criteria != None):
        for k, v in filter_criteria.items():
            # Initialize temporary filter mask
            temp_filter_mask = [False]*metadata.shape[0]
            # Make sure that v is a list
            if((type(v)==int) | (type(v)==str)): v = [v]
            # Temp filter mask should use OR operation
            for value in v:
                temp_filter_mask = temp_filter_mask | (metadata[k] == int(value))
            # Final filter mask should use AND operation
            filter_mask = filter_mask & temp_filter_mask
    # Mask creation is done; Now, get indexes for data to select
    subset_metadata = metadata.loc[filter_mask]
    metadata_row_idxs = list(subset_metadata.index)
    # Get the data subset for which to calculate statistics
    subset_idxs = [str(idx) for idx in metadata_row_idxs]
    # Return column indexes and corresponding metadata
    return (subset_idxs, subset_metadata)


# ## *Load train or test data for specified column ids*
# After running 'load_metadata_by_filter' to get a set of column ids, 'load_selected_data' can be called to load the data only for those column ids. This will be useful, because loading the entire training set at once uses too much memory (and the test set is even bigger)

# In[ ]:


# Load data according to specified column ids
def load_selected_data(column_ids, dataset_type = 'train'):
    # Set dataset path according to specified type
    if(dataset_type == 'test'):
        data_filepath = '../input/test.parquet'
    else:
        data_filepath = '../input/train.parquet'
    # Import the corresponding data
    data = pq.read_pandas(data_filepath, columns=column_ids).to_pandas()
    # Return the data
    return data


# ## *Compute statistics for selected data over shifted windows*
# Because the training and test datasets are so large, and no attempt will be made to input raw data into a model, this function allows data specified by column ids to be loaded and statistics calculated on it. This function can be used in a loop to import data in chunks and compute statistics on it. Supported statistics are 'mean', 'std', 'min', and 'max'. Statistics are calculated within a window of size 'window_size' shifted by 'offset' over all the data.

# In[ ]:


# Function to compute summary statistics on a selection of data
# 'window_size' is the size of the window for calculating rolling statistics
# 'offset' is how far the window is shifted for each statistics value saved/returned
def compute_summary_statistics(column_ids, window_size, offset, statistic='mean', dataset_type = 'train'):
    # Make sure window_size and offset are integers
    window_size = int(window_size); offset = int(offset)
    # Dictionary mapping stat string to numpy function
    stat_mapping = {'mean':np.mean, 'std':np.std, 'min':np.min, 'max':np.max}
    # Get the stat function
    stat_function = stat_mapping[statistic]
    # Load data in chunks to minimize memory usage, calculate FFT, and store results in a list
    stat_results = []; max_set_size = 300
    for idx in tqdm(range(int(np.ceil(len(column_ids)/max_set_size)))):
        # Get column ids for the current data chunk
        start_idx = max_set_size*idx
        current_column_ids = column_ids[start_idx:start_idx+max_set_size]
        # Load data for the current column ids
        data = load_selected_data(current_column_ids, dataset_type)
        # Take only every other data point to reduce memory usage
        data = data[::2]
        # Get the number of rows in data
        data_len = data.shape[0]
        # Assert that window_size <= data length (i.e. # of rows in the data)
        assert window_size <= data_len, 'Error: window_size must be <= number of rows ({0}) in data!'.format(data_len)
        # List comprehension to calculate statistics
        num_loops = 1 + int((data_len - window_size)/offset)
        summary_data = [stat_function(data.iloc[offset*i:offset*i+window_size].values, axis=0) for i in range(num_loops)]
        # Convert to a dataframe and append to stat_results
        summary_data_df = pd.DataFrame(summary_data, columns=current_column_ids)
        stat_results.append(summary_data_df)
        # Delete unneeded variables to manage memory usage
        del data; del summary_data
    # Concatenate the results (by column) into a single dataframe
    stat_results_df = pd.concat(stat_results, axis=1)
    # Delete stat_results for memory management
    del stat_results
    # Return the dataframe
    return stat_results_df


# ## *Compute rolling mean on FFT results*
# To get information about the frequency components of the data, calculate the FFT (Fast Fourier Transform) of the entire data (800000 data points) for a specified set of column ids. The magnitudes returned by the FFT vary over several orders of magnitude and the results are noisy. Therefore, they should be normalized across samples before calculating summary statistics.

# In[ ]:


# Function to get the FFT (Fast Fourier Transform) on a selection of data and compute rolling means
# 'window_size' is the size of the window for calculating rolling means
# 'offset' is how far the window is shifted for each mean value saved/returned
def compute_fft_statistics(column_ids, window_size, offset, dataset_type = 'train'):
    # Make sure window_size and offset are integers
    window_size = int(window_size); offset = int(offset)
    # Load data in chunks to minimize memory usage, calculate FFT, and store results in a list
    fft_results = []; max_set_size = 300
    for idx in tqdm(range(int(np.ceil(len(column_ids)/max_set_size)))):
        # Get column ids for the current data chunk
        start_idx = max_set_size*idx
        current_column_ids = column_ids[start_idx:start_idx+max_set_size]
        # Load data for the current column ids
        data = load_selected_data(current_column_ids, dataset_type)
        # Take only every other data point to reduce memory usage
        data = data[::2]
        # Calculate the FFT of the data and select only the first half of the result
        fft_data = np.abs(np.fft.fft(data, axis=0))[:int(len(data)/2)]
        # Delete data to manage memory usage
        del data
        # Normalize FFT data by mean across columns (i.e. across samples)
        #fft_data = fft_data / fft_data.mean(axis=1).reshape(-1,1)
        # Get the number of rows in data
        data_len = fft_data.shape[0]
        # Assert that window_size <= data length (i.e. # of rows in the data)
        assert window_size <= data_len, 'Error: window_size must be <= number of rows in data!'
        # Use a list comprehension to calculate rolling means (down columns)
        num_loops = 1 + int((data_len - window_size)/offset)
        summary_data = [np.mean(fft_data[offset*i:offset*i+window_size,:], axis=0) for i in range(num_loops)]
        # Take the log of the data and append results to fft_results
        summary_data = np.log(summary_data)
        fft_results.append(pd.DataFrame(summary_data, columns=current_column_ids))
        # Delete unneeded variables to manage memory usage (hopefully Python will do the garbage collection)
        del fft_data; del summary_data
    # Concatenate the results (by column) into a single dataframe
    all_fft_results = pd.concat(fft_results, axis=1)
    # Delete fft_results for memory management
    del fft_results
    # Return normalized and smoothed FFT results
    return all_fft_results


# # **Data Exploration**
# ## *Check the relative number of negative and positive examples*
# Positive examples (i.e. target == 1) are only 6% of the training set

# In[ ]:


# Import metadata for the training set
_, metadata_train = load_metadata_by_filter('train')

# Get the number of negative and positive examples
num_negative = np.sum(metadata_train.target == 0)
num_positive = np.sum(metadata_train.target == 1)
percent_positive = int(1e3*num_positive/(num_positive + num_negative))/10

# Print information about negative and positive examples
print('Number of training examples:', metadata_train.shape[0])
print('Negative examples: {0}'.format(num_negative))
print('Positive examples: {0} ({1}% of total)'.format(num_positive, percent_positive))


# ## *Get the range of measurement ids in the training set*
# The measurement ids range from 0 to 2903. With three phases for each, this comes to a total of 8712 (i.e. the total size of the training set)

# In[ ]:


# Import metadata for the training set
_, metadata_train = load_metadata_by_filter('train')
# Get the minimum and maximum id_measurement values
min_id_measurement = metadata_train.id_measurement.min()
max_id_measurement = metadata_train.id_measurement.max()
print('Train measurement ids: {0} to {1}'.format(min_id_measurement, max_id_measurement))


# ## *Get column ids for which to plot features*
# Generate two lists of id_measurement values: One containing the first 10 id_measurement values for which all three target values (corresponding to the three phases) are 0 (i.e. negative examples) and the other containing the first 10 id_measurement values for which all three target values are 1 (i.e. positive examples). These will be used to plot features (rolling mean and FFT results) for visual comparison of negative and positive examples.

# In[ ]:


# Import metadata for the training set
_, metadata_train = load_metadata_by_filter('train')
# Loop over id_measurements until 10 all-negative and 10 all-positive target value
# ids (i.e. id_measurement ids for which target values for the three phases are
# all 0 or all 1) have been identified.
negative_ids = []; positive_ids = []; max_ids = 10
for id_measurement in range(metadata_train.id_measurement.max()):
    # Get metadata for id_measurement
    current_metadata = metadata_train[metadata_train.id_measurement == id_measurement]
    # If all target values are 0, add id to the negative list
    if((current_metadata.target == 0).all()):
        if(len(negative_ids) < max_ids): negative_ids.append(id_measurement)
    # If all target values are 1, add id to the positive list
    elif((current_metadata.target == 1).all()):
        if(len(positive_ids) < max_ids): positive_ids.append(id_measurement)
    # If 10 negative and 10 positive ids have been found, break from loop
    if((len(negative_ids) >= max_ids) & (len(positive_ids) >= max_ids)):
        break
# Print the negative and positive id_measurement values
print('Negative ids:', negative_ids)
print('Positive ids:', positive_ids)


# ## *Load and preprocess data for negative and positive examples*
# Now, calculate rolling means and FFT features for the negative and positive examples. Note that window_size for rolling means is double that for FFT results, because the result of FFT analysis is half of the original data.
# 
# Note that, for rolling means, a sliding window of 8000 is used to calculate the means over the data set. The window is moved by 800 on each shift. On the entire dataset, this would reduce the size of the data from 800000 (8e5) rows to only 1 + (800000 - 8000) / 800 = 991 rows. Since the dataset is immediately cut to half the size (i.e. 4e5 rows), the final number of rows after calculating rolling means is 1 + (400000 - 8000) / 800 = 491.
# 
# For the FFT results, the raw data is also cut to half the original size (i.e. 4e5 rows). Since the FFT results are the same dimension, but they are symmetric. So, only the first half of the data is used, reducing the size to 2e5 rows. Finally, a rolling mean is calculated down the columns with a sliding window of 4000 with a shift of 400. The final number of rows is 1 + (200000 - 4000) / 400 = 491 (the same dimension as the rolling mean results).

# In[ ]:


# Get column ids for the negative id_measurement values
column_ids_0, metadata_0 = load_metadata_by_filter('train', 
                            filter_criteria={'id_measurement':negative_ids})
# Set window_size for rolling means and FFT preprocessing
window_size_means = 8000; window_size_fft = int(window_size_means/2)
# For the negative ids, get rolling means and FFT results
rolling_means_0 = compute_summary_statistics(column_ids_0,
    window_size_means, int(window_size_means/10), statistic='mean', dataset_type = 'train')
fft_results_0 = compute_fft_statistics(column_ids_0,
    window_size_fft, int(window_size_fft/10), dataset_type = 'train')


# In[ ]:


# Get column ids for the positive id_measurement values
column_ids_1, metadata_1 = load_metadata_by_filter('train',
                            filter_criteria={'id_measurement':positive_ids})
# Set window_size for rolling means and FFT preprocessing
window_size_means = 8000; window_size_fft = int(window_size_means/2)
# For the positive ids, get rolling means and FFT results
rolling_means_1 = compute_summary_statistics(column_ids_1,
    window_size_means, int(window_size_means/10), statistic='mean', dataset_type = 'train')
fft_results_1 = compute_fft_statistics(column_ids_1,
    window_size_fft, int(window_size_fft/10), dataset_type = 'train')


# ## *Generate plots of rolling means and FFT results for negative and positive examples*
# To visually compare rolling means and FFT results for negative and positive examples, generate plots of all preprocessed data. Ideally, if the data are useful for detecting faults in power lines, we would like to see some visually striking differences between the negative and positive examples. If we don't see this, we hope that machine learning models can effectively distinguish the groups based on non-obvious feature differences.

# ### First define the plotting routine to use for all data sets

# In[ ]:


# Function to generate subplots for rolling means and FFT results for negative and postive examples
def generate_subplots(data, metadata, ylim=[0,10]):
    # Get the number of plots to generate
    num_plots = data.shape[1]
    # Create the subplot object and get handles
    fig, axs = plt.subplots(int(num_plots/3), 3, figsize=(16, int(1.3*num_plots)))
    for idx in range(num_plots):
        # Get metadata for the current example
        signal_id, id_measurement, phase, target = metadata.iloc[idx,:]
        # Get the current data to plot
        current_data = data[str(signal_id)].values
        # Get the current ax handle
        ax = axs[int(idx/3), idx%3]
        # Set the title and turn on the grid for the current plot
        ax.set_title('sig id {0}; id meas {1}; phase {2}; target {3}'
                     .format(signal_id, id_measurement, phase, target))
        ax.grid(True)
        # Set the yrange
        ax.set_ylim(ylim)
        # Plot the data
        ax.plot(current_data)
    # Show the plots
    plt.show()


# ### Now plot rolling means and FFT results for negative and positive examples

# In[ ]:


# --- Plot rolling means for negative examples --- #
generate_subplots(rolling_means_0, metadata_0, ylim=[-25,25])


# In[ ]:


# --- Plot rolling means for positive examples --- #
generate_subplots(rolling_means_1, metadata_1, ylim=[-25,25])


# In[ ]:


# --- Plot FFT results for negative examples --- #
generate_subplots(fft_results_0, metadata_0, ylim=[5,8])


# In[ ]:


# --- Plot FFT results for positive examples --- #
generate_subplots(fft_results_1, metadata_1, ylim=[5, 8])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




