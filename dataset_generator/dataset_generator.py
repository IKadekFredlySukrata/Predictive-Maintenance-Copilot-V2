import numpy as np
import pandas as pd
import shutil

def dataset_maker(machine_type: str):
    np.random.seed(42)

    n_samples = {
        'L': 12960000,
        'M': 6480000,
        'H': 2160000
    }

    stats = {
        'L': {
            'Air temperature': {'mean': 300.0, 'std': 2.0},
            'Process temperature': {'mean': 310.0, 'std': 1.5},
            'Rotational speed': {'mean': 1540.0, 'std': 180.5},
            'Torque': {'mean': 40.0, 'std': 10.0}
        },
        'M': {
            'Air temperature': {'mean': 300.0, 'std': 2.0},
            'Process temperature': {'mean': 310.0, 'std': 1.5},
            'Rotational speed': {'mean': 1538.0, 'std': 179.0},
            'Torque': {'mean': 40.0, 'std': 10.0}
        },
        'H': {
            'Air temperature': {'mean': 300.0, 'std': 2.0},
            'Process temperature': {'mean': 310.0, 'std': 1.5},
            'Rotational speed': {'mean': 1538.0, 'std': 173.0},
            'Torque': {'mean': 40.0, 'std': 10.0}
        }
    }

    synthetic_data = {}

    for type, features in stats.items():
        if type == machine_type:
            for feature_name, feature_params in features.items():
                synthetic_data[feature_name] = np.random.normal(
                    loc=feature_params['mean'],
                    scale=feature_params['std'],
                    size=n_samples[machine_type]
                )

    tool_wear = []
    current_wear = 0
    for i in range(n_samples[machine_type]):
        tool_wear.append(current_wear)
        current_wear += 1
        if current_wear > 240:
            current_wear = 0

    synthetic_data['Tool wear'] = tool_wear

    synthetic_data['Type'] = [machine_type] * n_samples[machine_type]

    df = pd.DataFrame(synthetic_data)
    df = df[['Type', 'Air temperature', 'Process temperature', 
             'Rotational speed', 'Torque', 'Tool wear']]
    
    threshold = {
        'L': {
            'Air temperature': {'min': 295.3, 'max': 304.5},
            'Process temperature': {'min': 305.7, 'max': 313.8},
            'Rotational speed': {'min': 1181.0, 'max': 2886.0},
            'Torque': {'min': 3.0, 'max': 76.6}
        },
        'M': {
            'Air temperature': {'min': 295.3, 'max': 304.4},
            'Process temperature': {'min': 305.7, 'max': 313.8},
            'Rotational speed': {'min': 1168.0, 'max': 2710.0},
            'Torque': {'min': 9.7, 'max': 76.2}
        },
        'H': {
            'Air temperature': {'min': 295.5, 'max': 304.2},
            'Process temperature': {'min': 305.9, 'max': 313.5},
            'Rotational speed': {'min': 1212.0, 'max': 2636.0},
            'Torque': {'min': 12.8, 'max': 72.8}
        }
    }

    df['Air temperature'] = df['Air temperature'].clip(threshold[machine_type]['Air temperature']['min'], 
                                                       threshold[machine_type]['Air temperature']['max'])
    df['Process temperature'] = df['Process temperature'].clip(threshold[machine_type]['Process temperature']['min'], 
                                                       threshold[machine_type]['Process temperature']['max'])
    df['Rotational speed'] = df['Rotational speed'].clip(threshold[machine_type]['Rotational speed']['min'],
                                                       threshold[machine_type]['Rotational speed']['max'])
    df['Torque'] = df['Torque'].clip(threshold[machine_type]['Torque']['min'],
                                                       threshold[machine_type]['Torque']['max'])
    
    df.to_csv(f'generated_dataset/synthetic_dataset_{machine_type.lower()}_machine.csv', index=False)
    #shutil.move(f"../synthetic_dataset_{machine_type.lower()}_machine.csv", "generated_dataset")

machine_types = {'L', 'M', 'H'}
for machine_type in machine_types:
    print(f"Generating dataset {machine_type}")
    dataset_maker(machine_type)
    print(f"Dataset {machine_type} is generated")