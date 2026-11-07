import pandas as pd
import ast

df = pd.read_csv('ptbxl_database.csv', index_col='ecg_id')
df['validated_by_human'] = df['validated_by_human'].fillna(False)
valid_df = df[df['validated_by_human'] == True].copy()
valid_df['scp_codes'] = valid_df['scp_codes'].apply(ast.literal_eval)

classes = {
    'Normal': 'NORM',
    'Atrial fibrillation': 'AFIB',
    'Left bundle branch block': 'CLBBB',
    'Right bundle branch block': 'CRBBB',
    'Inferior myocardial infarction': 'IMI',
    'First-degree AV block': '1AVB'
}

selected_records = []
seen_patients = set()

for class_name, code in classes.items():
    matched = []
    for ecg_id, row in valid_df.iterrows():
        codes = row['scp_codes']
        # Relax constraint: code in codes with >= 100 likelihood, patient not yet seen
        if code in codes and codes[code] >= 100.0:
            patient_id = row['patient_id']
            matched.append((ecg_id, row, patient_id))

    print(f'Class {class_name} ({code}): found {len(matched)} records with {code} >= 100.')

    class_picked = 0
    for ecg_id, row, patient_id in matched:
        if class_picked >= 8:
            break
        if patient_id not in seen_patients:
            seen_patients.add(patient_id)
            selected_records.append({
                'ecg_id': ecg_id,
                'patient_id': patient_id,
                'class': class_name,
                'code': code,
                'filename_lr': row['filename_lr'],
                'filename_hr': row['filename_hr']
            })
            class_picked += 1

    print(f'Picked {class_picked} for {class_name}')

selected_df = pd.DataFrame(selected_records)
print('\nTotal selected records:', len(selected_df))
print(selected_df['class'].value_counts())
selected_df.to_csv('selected.csv', index=False)
print('Saved selected.csv successfully.')
