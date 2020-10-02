#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from plotly import tools, subplots
import plotly.offline as py
py.init_notebook_mode(connected = True)
import plotly.graph_objs as go
import plotly.express as px
pd.set_option('max_columns', 1000)
from bokeh.models import Panel, Tabs
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
import lightgbm as lgb
import plotly.figure_factory as ff
import gc
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder


# # Target Variable
# 
# The outcomes in this competition are grouped into 4 groups (labeled accuracy_group in the data):
# 
# * 3: the assessment was solved on the first attempt
# * 2: the assessment was solved on the second attempt
# * 1: the assessment was solved after 3 or more attempts
# * 0: the assessment was never solved
# 
# We have a multiclass problem. Let's check the main files

# # Files
# 
# # Train and test
# 
# These are the main data files which contain the gameplay events.
# 
# * event_id - Randomly generated unique identifier for the event type. Maps to event_id column in specs table.
# * game_session - Randomly generated unique identifier grouping events within a single game or video play session.
# * timestamp - Client-generated datetime
# * event_data - Semi-structured JSON formatted string containing the events parameters. Default fields are: event_count, event_code, and game_time; otherwise fields are determined by the event type.
# * installation_id - Randomly generated unique identifier grouping game sessions within a single installed application instance.
# * event_count - Incremental counter of events within a game session (offset at 1). Extracted from event_data.
# * event_code - Identifier of the event 'class'. Unique per game, but may be duplicated across games. E.g. event code '2000' always identifies the 'Start Game' event for all games. Extracted from event_data.
# * game_time - Time in milliseconds since the start of the game session. Extracted from event_data.
# * title - Title of the game or video.
# * type - Media type of the game or video. Possible values are: 'Game', 'Assessment', 'Activity', 'Clip'.
# * world - The section of the application the game or video belongs to. Helpful to identify the educational curriculum goals of the media. Possible values are: 'NONE' (at the app's start screen), TREETOPCITY' (Length/Height), 'MAGMAPEAK' (Capacity/Displacement), 'CRYSTALCAVES' (Weight).
# 
# # Specs
# 
# This file gives the specification of the various event types.
# 
# * event_id - Global unique identifier for the event type. Joins to event_id column in events table.
# * info - Description of the event.
# * args - JSON formatted string of event arguments. Each argument contains:
# * name - Argument name.
# * type - Type of the argument (string, int, number, object, array).
# * info - Description of the argument.
# 
# 
# # Train_labels
# * This file demonstrates how to compute the ground truth for the assessments in the training set.
# 
# # Sample_submission
# * A sample submission in the correct format.
# 
# So we have 2 files that have a lot of information that can be helpfull for predicting accuracy_group. Let's start with the train and test files.

# # Reading Files

# In[ ]:


get_ipython().run_cell_magic('time', '', "print('Reading train.csv file....')\ntrain = pd.read_csv('/kaggle/input/data-science-bowl-2019/train.csv')\nprint('Training.csv file have {} rows and {} columns'.format(train.shape[0], train.shape[1]))\n\nprint('Reading test.csv file....')\ntest = pd.read_csv('/kaggle/input/data-science-bowl-2019/test.csv')\nprint('Test.csv file have {} rows and {} columns'.format(test.shape[0], test.shape[1]))\n\nprint('Reading train_labels.csv file....')\ntrain_labels = pd.read_csv('/kaggle/input/data-science-bowl-2019/train_labels.csv')\nprint('Train_labels.csv file have {} rows and {} columns'.format(train_labels.shape[0], train_labels.shape[1]))\n\nprint('Reading specs.csv file....')\nspecs = pd.read_csv('/kaggle/input/data-science-bowl-2019/specs.csv')\nprint('Specs.csv file have {} rows and {} columns'.format(specs.shape[0], specs.shape[1]))\n\nprint('Reading sample_submission.csv file....')\nsample_submission = pd.read_csv('/kaggle/input/data-science-bowl-2019/sample_submission.csv')\nprint('Sample_submission.csv file have {} rows and {} columns'.format(sample_submission.shape[0], sample_submission.shape[1]))")


# Wow the dataset is huge, for exploration purpose let's extract a random sample

# # Train and Test exploration

# In[ ]:


train_sample = train.sample(1000000)
train_sample.head()


# * The first thing i notice is that we have 17k labels for 11M data points (train data). For the model we should aggregate by installation id and get agg stats.
# * It's going to be very important to engineer good features for the agg stats part.

# In[ ]:


train_labels.head()


# Let's explore the distribution of our target variable

# In[ ]:


cnt_srs = train_labels['accuracy_group'].value_counts(normalize = True).sort_index()
cnt_srs.index = ['Never Solved', '3 or More Attempts', 'Second Attempt', 'First Attempt']
trace = go.Bar(
    x = cnt_srs.index,
    y = cnt_srs.values,
    marker = dict(
        color = '#1E90FF',
    ),
)

layout = go.Layout(
    title = go.layout.Title(
        text = 'Distribution of Accuracy Group',
        x = 0.5
    ),
    font = dict(size = 14),
    width = 800,
    height = 500,
)

data = [trace]
fig = go.Figure(data = data, layout = layout)
py.iplot(fig, filename = 'accuracy_group')


# * The two most common classes are fist attempt and never solved.
# * The majority class have a 50% of the observations
# * The columns num_correct, num_incorrect and accuracy are used to calculate the accuracy_group columns. 

# In[ ]:


def bar_plot(df, column, title, width, height, n):
    print('We have {} unique values'.format(df[column].nunique()))
    cnt_srs = df[column].value_counts(normalize = True)[:n]
    trace = go.Bar(
        x = cnt_srs.index,
        y = cnt_srs.values,
        marker = dict(
            color = '#1E90FF',
        ),
    )

    layout = go.Layout(
        title = go.layout.Title(
            text = title,
            x = 0.5
        ),
        font = dict(size = 14),
        width = width,
        height = height,
    )

    data = [trace]
    fig = go.Figure(data = data, layout = layout)
    py.iplot(fig, filename = 'bar_plot')
bar_plot(train_labels, 'title', 'Assessment Title', 800, 500, 10)


# 1. * Let's explore the timestamp column

# In[ ]:


def get_time(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['month'] = df['timestamp'].dt.month
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek
    return df
    
train_sample = get_time(train_sample)
test = get_time(test)


# In[ ]:


output_notebook()
def scatter_plot(cnt_srs, color):
    trace = go.Scatter(
        x = cnt_srs.index,
        y = cnt_srs.values,
        showlegend = False,
        marker = dict(
            color = color,
        )
    )
    return trace


def get_time_plots(df):
    print('The dataset start on {} and ends on {}'.format(df['date'].min(), df['date'].max()))
    cnt_srs = df['date'].value_counts().sort_index()
    trace1 = scatter_plot(cnt_srs, 'red')
    cnt_srs = df['month'].value_counts().sort_index()
    trace2 = scatter_plot(cnt_srs, 'blue')
    cnt_srs = df['hour'].value_counts().sort_index()
    trace3 = scatter_plot(cnt_srs, 'green')
    cnt_srs = df['dayofweek'].value_counts().sort_index()
    trace4 = scatter_plot(cnt_srs, 'orange')
    
    subtitles = ['Date Frequency', 'Month Frequency', 'Hour Frequency', 'Day of Week Frequency']
    
    fig = subplots.make_subplots(rows = 4, cols = 1, vertical_spacing = 0.08, subplot_titles = subtitles)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 3, 1)
    fig.append_trace(trace4, 4, 1)
    fig['layout'].update(height = 1200, width = 1000, paper_bgcolor = 'rgb(233, 233, 233)')
    py.iplot(fig, filename = 'time_plots')
get_time_plots(train_sample)


# * Date frequency increase with time
# * Hour frequency is greater between 13 and 0
# * We have a greater frequency in Thursday and Friday

# In[ ]:


get_time_plots(test)


# * Date frequency have down and upper peaks but stay in the same line.
# * Month frequency behave similar to the train set (More observarions on August and September)
# * Hour frequency behave similar to the train set
# * Wednesday, Thursday, Friday and Sunday have hight frequencies.

# Let's check installation id distribution

# In[ ]:


bar_plot(train_labels, 'installation_id', 'Installation Id Distribution', 1000, 800, 100)


# * Left skewed
# * We have 3614 different installation ids (remeber it's a sample, all the train data have 17K)
# * Id 08987c08 have 0.88% of the observarions

# Let's check the event count distribution.

# In[ ]:


bar_plot(train_sample, 'event_count', 'Event Count Distribution', 1000, 800, 100)


# * We have 2205 unique values
# * Left skewed
# * Most common value is 1 with 2.66% of the observarions

# In[ ]:


def plot_hist(df, column, title, log = True):
    df = df[[column]]
    if log == True:
        df[column] = np.log1p(df[column])
    plt.figure(figsize = (10,8))
    sns.distplot(df[column])
    plt.title('{}'.format(title))
plot_hist(train_sample, 'game_time', 'Game Time Distribution', log = True)


# * Left skewd (log x + 1 to visualize better)

# In[ ]:


# title
bar_plot(train_sample, 'title', 'Title Distribution', 1000, 800, 100)


# * The most common tittle is Chow Time followed by Sandcastle Builder (Activity)
# * Left skewd
# 
# Let's check type column

# In[ ]:


bar_plot(train_sample, 'type', 'Type Distribution', 800, 500, 100)


# * Game is the most common type followed by Activity
# * Clip is only 1.6% of the observations
# 
# Let's check out world

# In[ ]:


bar_plot(train_sample, 'world', 'World Distribution', 800, 500, 100)


# * MAGMAPEAK have 44.3% of the observarions
# * NONE have almost 0% observations

# # Model
# 
# Let's try to build a baseline model. 

# In[ ]:


# funtions to get agg stadistics and merge with test and train
def get_object_columns(df, columns):
    df = df.groupby(['installation_id', columns])['event_id'].count().reset_index()
    df = df.pivot_table(index = 'installation_id', columns = [columns], values = 'event_id')
    df.columns = list(df.columns)
    df.fillna(0, inplace = True)
    return df

def get_numeric_columns(df, column):
    df = df.groupby('installation_id').agg({f'{column}': ['mean', 'sum', 'std']})
    df.fillna(0, inplace = True)
    df.columns = [f'{column}_mean', f'{column}_sum', f'{column}_std']
    return df

def get_numeric_columns_2(df, agg_column, column):
    df = df.groupby(['installation_id', agg_column]).agg({f'{column}': ['mean', 'sum', 'std']}).reset_index()
    df = df.pivot_table(index = 'installation_id', columns = [agg_column], values = [col for col in df.columns if col not in ['installation_id', 'type']])
    df.fillna(0, inplace = True)
    df.columns = list(df.columns)
    return df

numerical_columns = ['game_time']
categorical_columns = ['type', 'world']

reduce_train = pd.DataFrame({'installation_id': train['installation_id'].unique()})
reduce_train.set_index('installation_id', inplace = True)
reduce_test = pd.DataFrame({'installation_id': test['installation_id'].unique()})
reduce_test.set_index('installation_id', inplace = True)

train = get_time(train)

for i in numerical_columns:
    reduce_train = reduce_train.merge(get_numeric_columns(train, i), left_index = True, right_index = True)
    reduce_test = reduce_test.merge(get_numeric_columns(test, i), left_index = True, right_index = True)
    
for i in categorical_columns:
    reduce_train = reduce_train.merge(get_object_columns(train, i), left_index = True, right_index = True)
    reduce_test = reduce_test.merge(get_object_columns(test, i), left_index = True, right_index = True)
    
for i in categorical_columns:
    for j in numerical_columns:
        reduce_train = reduce_train.merge(get_numeric_columns_2(train, i, j), left_index = True, right_index = True)
        reduce_test = reduce_test.merge(get_numeric_columns_2(test, i, j), left_index = True, right_index = True)
    
    
reduce_train.reset_index(inplace = True)
reduce_test.reset_index(inplace = True)
    
print('Our training set have {} rows and {} columns'.format(reduce_train.shape[0], reduce_train.shape[1]))
    
# get the mode of the title
labels_map = dict(train_labels.groupby('title')['accuracy_group'].agg(lambda x:x.value_counts().index[0]))
# merge target
labels = train_labels[['installation_id', 'title', 'accuracy_group']]
# replace title with the mode
labels['title'] = labels['title'].map(labels_map)
# get title from the test set
reduce_test['title'] = test.groupby('installation_id').last()['title'].map(labels_map).reset_index(drop = True)
# join train with labels
reduce_train = labels.merge(reduce_train, on = 'installation_id', how = 'left')
print('We have {} training rows'.format(reduce_train.shape[0]))


# Now, lets alaign our train and test set

# In[ ]:


categoricals = ['title']
reduce_train = reduce_train[['installation_id', 'game_time_mean', 'game_time_sum', 'game_time_std', 'Activity', 'Assessment', 
                             'Clip', 'Game', 'CRYSTALCAVES', 'MAGMAPEAK', 'NONE', 'TREETOPCITY', ('game_time', 'mean', 'Activity'),
                             ('game_time', 'mean', 'Assessment'), ('game_time', 'mean', 'Clip'), ('game_time', 'mean', 'Game'), 
                             ('game_time', 'std', 'Activity'), ('game_time', 'std', 'Assessment'), ('game_time', 'std', 'Clip'), 
                             ('game_time', 'std', 'Game'), ('game_time', 'sum', 'Activity'), ('game_time', 'sum', 'Assessment'), 
                             ('game_time', 'sum', 'Clip'), ('game_time', 'sum', 'Game'), ('game_time', 'mean', 'CRYSTALCAVES'), 
                             ('game_time', 'mean', 'MAGMAPEAK'), ('game_time', 'mean', 'NONE'), ('game_time', 'mean', 'TREETOPCITY'), 
                             ('game_time', 'std', 'CRYSTALCAVES'), ('game_time', 'std', 'MAGMAPEAK'), ('game_time', 'std', 'NONE'), 
                             ('game_time', 'std', 'TREETOPCITY'), ('game_time', 'sum', 'CRYSTALCAVES'), 
                             ('game_time', 'sum', 'MAGMAPEAK'), ('game_time', 'sum', 'NONE'), ('game_time', 'sum', 'TREETOPCITY'), 
                             'title', 'accuracy_group']]


# In[ ]:


def run_lgb(reduce_train, reduce_test):
    kf = KFold(n_splits=10)
    features = [i for i in reduce_train.columns if i not in ['accuracy_group', 'installation_id']]
    target = 'accuracy_group'
    oof_pred = np.zeros((len(reduce_train), 4))
    y_pred = np.zeros((len(reduce_test), 4))
    for fold, (tr_ind, val_ind) in enumerate(kf.split(reduce_train)):
        print('Fold {}'.format(fold + 1))
        x_train, x_val = reduce_train[features].iloc[tr_ind], reduce_train[features].iloc[val_ind]
        y_train, y_val = reduce_train[target][tr_ind], reduce_train[target][val_ind]
        train_set = lgb.Dataset(x_train, y_train, categorical_feature=categoricals)
        val_set = lgb.Dataset(x_val, y_val, categorical_feature=categoricals)

        params = {
            'learning_rate': 0.01,
            'metric': 'multiclass',
            'objective': 'multiclass',
            'num_classes': 4,
            'feature_fraction': 0.75,
            'subsample': 0.75
        }

        model = lgb.train(params, train_set, num_boost_round = 100000, early_stopping_rounds = 100, 
                          valid_sets=[train_set, val_set], verbose_eval = 100)
        oof_pred[val_ind] = model.predict(x_val)
        y_pred += model.predict(reduce_test[features]) / 10
    return y_pred
y_pred = run_lgb(reduce_train, reduce_test)


# In[ ]:


reduce_test = reduce_test.reset_index()
reduce_test = reduce_test[['installation_id']]
reduce_test['accuracy_group'] = y_pred.argmax(axis = 1)
sample_submission.drop('accuracy_group', inplace = True, axis = 1)
sample_submission = sample_submission.merge(reduce_test, on = 'installation_id')
sample_submission.to_csv('submission.csv', index = False)


# In[ ]:


sample_submission['accuracy_group'].value_counts(normalize = True)

