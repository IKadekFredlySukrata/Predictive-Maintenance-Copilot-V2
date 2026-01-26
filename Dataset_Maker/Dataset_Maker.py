import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples to generate
n_samples = 432000

# Statistics from your image (excluding Tool wear - we'll handle it separately)
stats = {
    'Air temperature': {'mean': 300.031567, 'std': 2.016278},
    'Process temperature': {'mean': 310.021367, 'std': 1.497908},
    'Rotational speed': {'mean': 1537.640667, 'std': 178.949751},
    'Torque': {'mean': 40.011500, 'std': 9.986487}
}

# Generate synthetic data using normal distribution
synthetic_data = {}

for feature, params in stats.items():
    synthetic_data[feature] = np.random.normal(
        loc=params['mean'],
        scale=params['std'],
        size=n_samples
    )

# Generate Tool wear - sequential from 0 to 240, then reset
tool_wear = []
current_wear = 0
for i in range(n_samples):
    tool_wear.append(current_wear)
    current_wear += 1
    if current_wear > 240:
        current_wear = 0

synthetic_data['Tool wear'] = tool_wear

# Add Type column (all 'M' based on your data)
synthetic_data['Type'] = ['M'] * n_samples

# Create DataFrame
df = pd.DataFrame(synthetic_data)

# Reorder columns to match your original dataset
df = df[['Type', 'Air temperature', 'Process temperature', 
         'Rotational speed', 'Torque', 'Tool wear']]

# Apply constraints based on min/max from your data (except Tool wear)
df['Air temperature'] = df['Air temperature'].clip(295.3, 304.4)
df['Process temperature'] = df['Process temperature'].clip(305.7, 313.8)
df['Rotational speed'] = df['Rotational speed'].clip(1168.0, 2710.0)
df['Torque'] = df['Torque'].clip(9.7, 76.2)

# Round to appropriate decimal places
df['Air temperature'] = df['Air temperature'].round(6)
df['Process temperature'] = df['Process temperature'].round(6)
df['Rotational speed'] = df['Rotational speed'].round(6)
df['Torque'] = df['Torque'].round(6)
# Tool wear is already integer, no need to round

# Display first few rows and around the reset point
print("First 10 rows:")
print(df.head(10))
print("\nRows around first reset (235-245):")
print(df.iloc[235:246])
print("\nRows around second reset (476-486):")
print(df.iloc[476:486])

print(f"\nDataset shape: {df.shape}")
print(f"\nStatistics of generated data:")
print(df.describe())

# Save to CSV
df.to_csv('synthetic_dataset.csv', index=False)
print("\nDataset saved to 'synthetic_dataset.csv'")