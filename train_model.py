import pandas as pd
from sklearn.neural_network import MLPRegressor
import pickle

# read data
data = pd.read_csv("projectile_data.csv")

# input X,Y → output theta,v0
X = data[["X", "Y"]].values
y = data[["theta_deg", "v0"]].values

# define model
model = MLPRegressor(hidden_layer_sizes=(64,64), max_iter=500, random_state=42)
model.fit(X, y)

# save model
with open("projectile_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as projectile_model.pkl")

