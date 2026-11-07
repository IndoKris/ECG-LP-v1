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

for class_name, code in classes.items():
    count = 0
    count_any = 0
    for ecg_id, row in valid_df.iterrows():
        codes = row['scp_codes']
        if code in codes:
            count_any += 1
            if codes[code] >= 100.0:
                count += 1
    print(f'{class_name} ({code}): any presence = {count_any}, likelihood >= 100 = {count}')
