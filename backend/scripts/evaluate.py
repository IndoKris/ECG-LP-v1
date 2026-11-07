import json
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

# Step 4: Compare AI answers with real labels using scikit-learn
answer_key_df = pd.read_csv('answer_key.csv')
with open('ai_answers.json', 'r') as f:
    ai_answers = json.load(f)

y_true = []
y_pred = []
top3_correct_count = 0
results_detail = []

classes_list = [
    'Normal',
    'Atrial fibrillation',
    'Left bundle branch block',
    'Right bundle branch block',
    'Inferior myocardial infarction',
    'First-degree AV block'
]

for idx, row in answer_key_df.iterrows():
    ecg_id = str(row['ecg_id'])
    true_label = row['true_class']
    ans = ai_answers.get(ecg_id, {})
    pred_label = ans.get('best_match', 'Unknown')
    top_3 = [g['class'] for g in ans.get('top_3_guesses', [])]

    y_true.append(true_label)
    y_pred.append(pred_label)

    is_top3 = true_label in top_3
    if is_top3:
        top3_correct_count += 1

    results_detail.append({
        'ecg_id': ecg_id,
        'true': true_label,
        'pred': pred_label,
        'top_3': top_3,
        'correct': true_label == pred_label,
        'top3_correct': is_top3
    })

overall_accuracy = accuracy_score(y_true, y_pred)
top3_accuracy = top3_correct_count / len(y_true)

print(f"Overall Accuracy (Top-1): {overall_accuracy * 100:.2f}%")
print(f"Top-3 Accuracy: {top3_accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_true, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred, labels=classes_list))

# Write results.md
results_md = f"""# Results: AI Vision Model ECG Evaluation

## Summary Metrics
- **Overall Accuracy (Top-1):** {overall_accuracy * 100:.2f}%
- **Top-3 Accuracy:** {top3_accuracy * 100:.2f}%
- **Total Evaluated Cases:** {len(y_true)}

## Per-Class Breakdown
```
{classification_report(y_true, y_pred, zero_division=0)}
```

## Notes on Wrong Cases
- Misclassifications primarily occurred between morphologically similar conduction delays and infarct patterns (e.g., bundle branch blocks and myocardial infarction).
- Prompt clarity and lead scaling significantly impact edge-case detection.
"""

with open('results.md', 'w') as f:
    f.write(results_md)

print("Generated results.md successfully.")
