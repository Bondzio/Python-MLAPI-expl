import pandas as pd
import numpy as np
from kaggle.competitions import twosigmanews
env = twosigmanews.make_env()

(market_train_df, news_train_df) = env.get_training_data()
# market_train_df is the training marketdata (roughly 2007 to 2017)
# news_train_df is the training news data (roughly 2007 to 2017)

for (market_obs_df, news_obs_df, predictions_template_df) in env.get_prediction_days(): # Looping over days from start of 2017 to 2019-07-15
  # market_obs_df always have time values of 22:00 UTC. This is a snapshot of the trading day.
  # news_obs_df contains news from the previous market day up until the current day 22:00 UTC.
  
  current_time = market_obs_df.time.iloc[0] # You are here in time
  print(current_time)
  
  predictions_template_df['confidenceValue'] = 2.0 * np.random.rand(len(predictions_template_df)) - 1.0 # TODO: prove markets not efficient?
  env.predict(predictions_template_df) # Saves your predictions for the day

env.write_submission_file() # Writes your submission file