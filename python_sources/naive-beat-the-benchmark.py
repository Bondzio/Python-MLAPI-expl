import pandas as pd
sub = pd.read_csv('../input/sample_submission.csv')
sub['day'] = "5 4 3 2 1"
sub.to_csv('naive_submit.csv', index=False)