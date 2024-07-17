import pandas as pd
import glob
from hmmlearn import hmm
import numpy as np
import joblib
from sklearn.model_selection import train_test_split

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

# Remove unnecessary columns
combined_df = combined_df.drop(columns=['Suddeness', 'TimeStamp', 'Average Speed', 'Driver Behavior', 'Reason for lane change', 'Remarks'])

# Map passenger load to numerical values
load_map = {'Low (0 - 33 %)': 0, 'Moderate (34 - 80 %)': 1, 'Full (81 - 100%)': 2}
combined_df['Passenger Load'] = combined_df['Passenger Load'].map(load_map)

# Convert observed and hidden states to numerical values
hidden_states = combined_df['Hidden State'].unique()
observed_states = combined_df['Observed State'].unique()

hidden_state_map = {state: i for i, state in enumerate(hidden_states)}
observed_state_map = {state: i for i, state in enumerate(observed_states)}

combined_df['Hidden State'] = combined_df['Hidden State'].map(hidden_state_map)
combined_df['Observed State'] = combined_df['Observed State'].map(observed_state_map)

# Split data into sequences based on passenger load changes
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

# Perform train-test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Combine all sequences for fitting the model
X_train_combined = np.concatenate(X_train)
lengths_train = [len(x) for x in X_train]

# Train a Gaussian HMM
model = hmm.GaussianHMM(n_components=len(hidden_states), covariance_type="diag", n_iter=1000)
model.fit(X_train_combined, lengths_train)

# Print model parameters
print("Transition matrix")
print(model.transmat_)
print(model.score(X_train_combined))
print("\nMeans and covariances of each hidden state")
for i in range(len(hidden_states)):
    print("\nHidden state", i)
    print("Mean =", model.means_[i])
    print("Covariance matrix =\n", model.covars_[i])

# Evaluate on test set
X_test_combined = np.concatenate(X_test)
lengths_test = [len(x) for x in X_test]
print("\nTest set score:", model.score(X_test_combined, lengths_test))

# Save the trained model
joblib.dump(model, 'trained_hmm_model.pkl')
