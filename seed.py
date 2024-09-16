import pandas as pd
import glob
from hmmlearn import hmm
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from scipy.stats import multivariate_normal

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
combined_df.to_csv('combined_data.csv', index=False)

# Remove unnecessary columns
combined_df = combined_df.drop(columns=['Suddeness', 'TimeStamp', 'Average Speed', 'Driver Behavior', 'Reason for lane change', 'Remarks'])

# Map passenger load to numerical values
load_map = {'Low (0 - 33 %)': 0, 'Moderate (34 - 80 %)': 1, 'Full (81 - 100%)': 2}
combined_df['Passenger Load'] = combined_df['Passenger Load'].map(load_map)

# Convert observed and hidden states to numerical values
hidden_states = combined_df['Hidden State'].unique()
observed_states = combined_df['Observed State'].unique()

hidden_state_map = {'Vehicle': 0, 'Passenger': 1, 'Stoplight': 2}
observed_state_map = {'Go': 0, '1 Lane Right': 1, 'Load': 2, 'Stop': 3, '1 Lane Left': 4, 'Unload': 5, 'Wait': 6, '2 Lane Left': 7, '2 Lane Right': 8}

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
X_train_combined = np.concatenate(X_train)
lengths_train = [len(x) for x in X_train]

# Function to evaluate emission probabilities
def evaluate_emission_probabilities(model):
    emission_probs = {i: [] for i in range(len(hidden_states))}
    for i in range(len(hidden_states)):
        for j, obs_state in enumerate(observed_states):
            mean = model.means_[i]
            covar = np.diag(model.covars_[i])
            prob = multivariate_normal.pdf([observed_state_map[obs_state]], mean=mean, cov=covar)
            emission_probs[i].append(prob)
    return emission_probs

# Try different random states to find a good one
best_random_state = None

for random_state in range(840, 10000000):  # Adjust range as needed
    print(random_state)
    model = hmm.GaussianHMM(n_components=len(hidden_states), covariance_type="diag", n_iter=1000, random_state=random_state)
    model.fit(X_train_combined, lengths_train)
    
    # Evaluate emission probabilities
    emission_probs = evaluate_emission_probabilities(model)
    
    # Check if this model meets the desired properties
    state_0_valid = True
    #state_0_valid = all(prob > 0.00 for prob in emission_probs[0])  # Hidden state 0 should have non-zero values for at least some observed states
    state_1_valid = (emission_probs[1][observed_state_map['Load']] > 0.00 and
                     emission_probs[1][observed_state_map['Unload']] > 0.00)  # Hidden state 1 should have non-zero values for 'Load' and 'Unload'
    state_2_valid = (emission_probs[2][observed_state_map['Stop']] > 0.00 and
                     all(emission_probs[2][j] == 0.00 for j, obs_state in enumerate(observed_states) if obs_state != 'Stop'))  # Hidden state 2 should only have non-zero value for 'Stop'

    if state_0_valid and state_1_valid and state_2_valid:
        best_random_state = random_state
        break

print(f"Best random state found: {best_random_state}")

# Train final model with the best random state
model = hmm.GaussianHMM(n_components=len(hidden_states), covariance_type="diag", n_iter=1000, random_state=best_random_state)
model.fit(X_train_combined, lengths_train)

# Save the trained model
joblib.dump(model, 'trained_hmm_model_best.pkl')
