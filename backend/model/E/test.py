import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import time

def load_data(file_path):
    data = pd.read_excel(file_path)
    # Handle missing values here (e.g., data.fillna(method='ffill', inplace=True))
    return data

def evaluate_model(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared: {r2:.2f}")
    return mse, rmse, mae, r2

# Load the saved model
predictor = TabularPredictor.load("AutogluonModels/ag-20240725_071820")

# Load data
data = load_data('../data/Environmental_esg_tone.xlsx')


# Separate features and target variable
new_features = data.drop('Environmental_Score', axis=1)
new_target = data['Environmental_Score']
print("DATA reading done")
print()
# Make predictions

print("STARTING prediction")
print()
start_time = time.time()
# predictor._learner.persist_trainer(low_memory=False)
new_predictions = predictor.predict(new_features)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Prediction time: {elapsed_time:.4f} seconds")
print()

# Evaluate model
mse, rmse, mae, r2 = evaluate_model(new_target, new_predictions)

# Combine predictions with original data
data['Predicted_Score'] = new_predictions
data['difference'] = data['Predicted_Score'] - data['Environmental_Score']

# Save results
# data.to_excel('../outcomes/E_Outcome.xlsx', index=False)

