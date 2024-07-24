from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import pandas as pd

# Load your data
train_df = pd.read_excel('../../data/Social_esg_tone.xlsx')
train_df['Social_Score'] = train_df['Social_Score'].astype(int)  # Ensure target variable is integer
train_df.drop(columns =["company"])

target = 'Social_Score'

# Split data into training and validation sets
train_data, val_data = train_test_split(train_df, test_size=0.2, random_state=42)

train_data = TabularDataset(train_df)
val_data = TabularDataset(val_data)

# Create a TabularPredictor object
quality = 'medium_quality'
predictor = TabularPredictor(label=target).fit(train_data,presets=quality)

# Make predictions on the validation set (excluding target variable)
y_pred = predictor.predict(val_data.drop(columns=['Social_Score']))

# Evaluate model performance on validation set
predictor.evaluate(val_data, silent=True)
# View the leaderboard (models explored during training)
print(predictor.leaderboard(val_data))
