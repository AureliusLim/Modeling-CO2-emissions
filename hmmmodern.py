import pandas as pd
import glob
from hmmlearn import hmm
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from scipy.stats import multivariate_normal
# Path to the directory containing CSV files
csv_files_path = 'hmmdatamodern/*.csv'

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
combined_df.to_csv('combined_data_modern.csv', index=False)

print(combined_df.head())
print(combined_df.shape)

combined_df = combined_df.drop(columns=['Suddeness', 'TimeStamp', 'Driver Behavior', 'Reason for lane change', 'Remarks'])
print(combined_df.isnull().sum())

# Map passenger load to numerical values
load_map = {'Low (0 - 33 %)': 0, 'Moderate (34 - 80 %)': 1, 'Full (81 - 100%)': 2}
combined_df['Passenger Load'] = combined_df['Passenger Load'].map(load_map)

# Convert observed and hidden states to numerical values
hidden_states = combined_df['Hidden State'].unique()
observed_states = combined_df['Observed State'].unique()

hidden_state_map = {'Vehicle': 0, 'Passenger': 1, 'Stoplight': 2}
observed_state_map = {'Go': 0, '1 Lane Right': 1, 'Load': 2, 'Stop': 3, '1 Lane Left': 4, 'Unload': 5, 'Wait': 6, '2 Lane Left': 7, '2 Lane Right': 8}

# Print the mappings
print("Hidden State Mapping:", hidden_state_map)
print("Observed State Mapping:", observed_state_map)

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
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

# Combine all sequences for fitting the model
X_train_combined = np.concatenate(X_train)
lengths_train = [len(x) for x in X_train]

# Train a Gaussian HMM
model = hmm.GaussianHMM(n_components=len(hidden_states), covariance_type="diag", n_iter=1000, random_state=49)
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

print("\nEmission probabilities (probability of observing each state given each hidden state):")
for i in range(len(hidden_states)):
    print(f"\nHidden state {i}:")
    for j, obs_state in enumerate(observed_states):
        mean = model.means_[i]
        covar = np.diag(model.covars_[i])  # Use diagonal covariance
        prob = multivariate_normal.pdf([observed_state_map[obs_state]], mean=mean, cov=covar)
        print(f"Probability of observing '{obs_state}' = {prob:.2e}")

# Save the trained model
joblib.dump(model, 'trained_hmm_model_modern.pkl')
