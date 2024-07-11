import pandas as pd
import glob
from hmmlearn import hmm
import numpy as np
# Path to the directory containing CSV files
csv_files_path = 'hmmdata/*.csv'

# Get a list of all CSV files in the directory
csv_files = glob.glob(csv_files_path)

# Read and concatenate all CSV files into a single DataFrame
dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dataframes, ignore_index=True)

# Optionally, save the combined dataframe to a new CSV file
combined_df.to_csv('combined_data.csv', index=False)

print(combined_df.head())
print(combined_df.shape)


combined_df = combined_df.drop(columns=['Suddeness', 'TimeStamp', 'Average Speed', 'Driver Behavior', 'Reason for lane change', 'Remarks'])
print(combined_df.isnull().sum())
# Map passenger load to numerical values
load_map = {'Low (0 - 33 %)': 0, 'Moderate (34 - 80 %)': 1, 'Full (81 - 100%)': 2}
combined_df['Passenger Load'] = combined_df['Passenger Load'].map(load_map)

# Convert observed and hidden states to numerical values
hidden_states = combined_df['Hidden State'].unique()
observed_states = combined_df['Observed State'].unique()

hidden_state_map = {state: i for i, state in enumerate(hidden_states)}
observed_state_map = {state: i for i, state in enumerate(observed_states)}
# Print the mappings
print("Hidden State Mapping:", hidden_state_map)
print("Observed State Mapping:", observed_state_map)

combined_df['Hidden State'] = combined_df['Hidden State'].map(hidden_state_map)
combined_df['Observed State'] = combined_df['Observed State'].map(observed_state_map)

# Split data into sequences
sequences = []
start_idx = 0

for i in range(1, len(combined_df)):
    if combined_df.loc[i, 'Passenger Load'] < combined_df.loc[i-1, 'Passenger Load']:  
        sequences.append((combined_df.loc[start_idx:i, ['Observed State', 'Passenger Load']].values, 
                          combined_df.loc[start_idx:i, 'Hidden State'].values))
        start_idx = i

sequences.append((combined_df.loc[start_idx:, ['Observed State', 'Passenger Load']].values, 
                  combined_df.loc[start_idx:, 'Hidden State'].values))

# Split sequences into observations and hidden states
X = [seq[0] for seq in sequences]
Y = [seq[1] for seq in sequences]
# Combine all sequences for fitting the model
X_combined = np.concatenate(X)
lengths = [len(x) for x in X]

# Train a Gaussian HMM
model = hmm.GaussianHMM(n_components=len(hidden_states), covariance_type="diag", n_iter=1000)
model.fit(X_combined, lengths)

# Print model parameters
print("Transition matrix")
print(model.transmat_)
print("\nMeans and covariances of each hidden state")
for i in range(len(hidden_states)):
    print("\nHidden state", i)
    print("Mean =", model.means_[i])
    print("Covariance matrix =\n", model.covars_[i])