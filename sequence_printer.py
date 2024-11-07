import pandas as pd
import glob
import numpy as np
from hmmlearn import hmm
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
import joblib
def print_state_occurrences_by_load(sequences):
    load_groups = {0: 'Low (0 - 33%)', 1: 'Moderate (34 - 80%)', 2: 'Full (81 - 100%)'}
    for load, load_name in load_groups.items():
        observed_states = []
        hidden_states = []
        for seq in sequences:
            # Filter sequences by passenger load
            load_indices = np.where(seq[0][:, 1] == load)[0]
            if len(load_indices) > 0:
                observed_states.extend(seq[0][load_indices, 0])
                hidden_states.extend(seq[1][load_indices])
        
        # Print observed state occurrences
        print(f"\nOccurrences of observed states for Passenger Load '{load_name}':")
        print(pd.Series(observed_states).value_counts().sort_index())

        # Print hidden state occurrences
        print(f"Occurrences of hidden states for Passenger Load '{load_name}':")
        print(pd.Series(hidden_states).value_counts().sort_index())
csv_files_path = 'validation/simulation/modern/*.csv'

# Get a list of all CSV files in the directory
csv_files = glob.glob(csv_files_path)

# Read and concatenate all CSV files into a single DataFrame
dataframes = [pd.read_csv(file) for file in csv_files]
combined_df = pd.concat(dataframes, ignore_index=True)

# Data preprocessing
combined_df = combined_df.drop(columns=['Suddeness', 'TimeStamp', 'Driver Behavior', 'Reason for lane change', 'Remarks'])

# Mapping categorical values to numerical values
load_map = {'Low (0 - 33 %)': 0, 'Moderate (34 - 80 %)': 1, 'Full (81 - 100%)': 2}
combined_df['Passenger Load'] = combined_df['Passenger Load'].map(load_map)

hidden_state_map = {'Vehicle': 0, 'Passenger': 1, 'Stoplight': 2}
observed_state_map = {'Go': 0, '1 Lane Right': 1, 'Load': 2, 'Stop': 3, '1 Lane Left': 4, 'Unload': 5, 'Wait': 6, '2 Lane Left': 7, '2 Lane Right': 8}

combined_df['Hidden State'] = combined_df['Hidden State'].map(hidden_state_map)
combined_df['Observed State'] = combined_df['Observed State'].map(observed_state_map)

sequences = []
start_idx = 0

for i in range(1, len(combined_df)):
    if combined_df.loc[i, 'Passenger Load'] < combined_df.loc[i-1, 'Passenger Load']:
        sequences.append((combined_df.loc[start_idx:i, ['Observed State', 'Passenger Load']].values, 
                          combined_df.loc[start_idx:i, 'Hidden State'].values))
        start_idx = i

sequences.append((combined_df.loc[start_idx:, ['Observed State', 'Passenger Load']].values, 
                  combined_df.loc[start_idx:, 'Hidden State'].values))

# Flatten sequences for HMM input
def flatten_sequences(sequences):
    return [item for sublist in sequences for item in sublist]

# Debug: Print the distribution of observed and hidden states in sequences
observed_states_flat = flatten_sequences([seq[0][:, 0] for seq in sequences])
hidden_states_flat = flatten_sequences([seq[1] for seq in sequences])

print("\nDistribution of observed states in sequences:")
print(pd.Series(observed_states_flat).value_counts().sort_index())

print("\nDistribution of hidden states in sequences:")
print(pd.Series(hidden_states_flat).value_counts().sort_index())
print_state_occurrences_by_load(sequences)