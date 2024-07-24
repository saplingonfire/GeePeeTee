from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import pandas as pd

# Load your data
train_df = pd.read_excel('../../data/Environmental_esg_tone.xlsx')
train_df['Environmental_Score'] = train_df['Environmental_Score'].astype(int)  # Ensure target variable is integer
# train_df.drop(columns =["company"])

target = 'Environmental_Score'

# Split data into training and validation sets
train_data, val_data = train_test_split(train_df, test_size=0.2, random_state=42)

train_data = TabularDataset(train_df)
val_data = TabularDataset(val_data)


# Create a TabularPredictor object
quality = 'medium_quality'
predictor = TabularPredictor(label=target).fit(train_data,presets=quality)  # **Added fit method**

# Make predictions on the validation set (excluding target variable)
y_pred = predictor.predict(val_data.drop(columns=['Environmental_Score']))

# Evaluate model performance on validation set
predictor.evaluate(val_data, silent=True)
# View the leaderboard (models explored during training)
print(predictor.leaderboard(val_data))

# presets='best_quality'   : Maximize accuracy. Default time_limit=3600.
# presets='high_quality'   : Strong accuracy with fast inference speed. Default time_limit=3600.
# presets='good_quality'   : Good accuracy with very fast inference speed. Default time_limit=3600.
# presets='medium_quality'