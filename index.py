import numpy as np
import json
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import pyswarms as ps
import matplotlib.pyplot as plt

# Step 1: Load the data from the JSON file
with open('assets/data.json', 'r') as f:
    data = json.load(f)

# Step 2: Extract the data into numpy arrays and combine Station 1 and Station 2 features
X_station1 = np.array([entry['s1'] for entry in data])
X_station2 = np.array([entry['s2'] for entry in data])
X_combined = np.hstack((X_station1, X_station2))  # Combine features from both stations
y = np.array([entry['output'] for entry in data])

# Step 3: Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

kf = KFold(n_splits=10, shuffle=True)

X_data = X_scaled

def fitness_function(params):
    n_particles = params.shape[0]
    scores = np.zeros(n_particles)
    
    for i in range(n_particles):
        C, epsilon, gamma = params[i]
        svr = SVR(kernel='rbf', C=C, epsilon=epsilon, gamma=gamma)
        mse_scores = cross_val_score(svr, X_data, y, cv=kf, scoring='neg_mean_squared_error')
        rmse_scores = np.sqrt(-mse_scores)
        scores[i] = np.mean(rmse_scores)

    return scores

bounds = (np.array([0.1, 0.001, 0.001]),  # Lower bounds for C, epsilon, gamma
        np.array([5000, 3, 4]))          # Upper bounds for C, epsilon, gamma

# Increase the number of particles and iterations
options = {'c1': 0.7, 'c2': 0.5, 'w': 0.5}
optimizer = ps.single.GlobalBestPSO(n_particles=20, dimensions=3, options=options, bounds=bounds)

#Best-One
C = 2.60222552e+03
epsilon = 1.39305580e-01
gamma = 1.76320481e+00

best_cost, best_params = optimizer.optimize(fitness_function, iters=3)
print("Best Parameters from PSO:", best_params)
C, epsilon, gamma = best_params

# Initialize lists to store performance metrics across all folds
rmse_list = []
mae_list = []
r2_list = []

for train_index, test_index in kf.split(X_data):
    X_train, X_test = X_data[train_index], X_data[test_index]
    y_train, y_test = y[train_index], y[test_index]

    svr = SVR(kernel='rbf', C=C, epsilon=epsilon, gamma=gamma)
    svr.fit(X_train, y_train)

    y_pred = svr.predict(X_test)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Store metrics for later reporting
    rmse_list.append(rmse)
    mae_list.append(mae)
    r2_list.append(r2)
    
    # Print individual fold metrics
    print(f"Fold RMSE: {rmse}")
    print(f"Fold MAE: {mae}")
    print(f"Fold R² Score: {r2}")

# Summarize performance across all folds
mean_rmse = np.mean(rmse_list)
mean_mae = np.mean(mae_list)
mean_r2 = np.mean(r2_list)

print("\nSummary of Performance Across All Folds:")
print(f"Average RMSE: {mean_rmse}")
print(f"Average MAE: {mean_mae}")
print(f"Average R² Score: {mean_r2}")

# Plotting the RMSE values as a bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(range(1, len(rmse_list) + 1), rmse_list, color='blue')

# Adding titles and labels
plt.title('RMSE of Each Cross-Validation Fold')
plt.xlabel('Fold Index')
plt.ylabel('RMSE')
plt.xticks(range(1, len(rmse_list) + 1))  # Set x-ticks to match fold indices
plt.grid(axis='y')

# Adding RMSE values on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom')

# Display the plot
plt.show()