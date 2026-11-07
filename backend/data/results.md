# Results: AI Vision Model ECG Evaluation

## Summary Metrics
- **Overall Accuracy (Top-1):** 81.25%
- **Top-3 Accuracy:** 87.50%
- **Total Evaluated Cases:** 48

## Per-Class Breakdown
```
                                precision    recall  f1-score   support

           Atrial fibrillation       0.88      0.88      0.88         8
         First-degree AV block       1.00      1.00      1.00         8
Inferior myocardial infarction       0.78      0.88      0.82         8
      Left bundle branch block       0.83      0.62      0.71         8
                        Normal       0.62      0.62      0.62         8
     Right bundle branch block       0.78      0.88      0.82         8

                      accuracy                           0.81        48
                     macro avg       0.81      0.81      0.81        48
                  weighted avg       0.81      0.81      0.81        48

```

## Notes on Wrong Cases
- Misclassifications primarily occurred between morphologically similar conduction delays and infarct patterns (e.g., bundle branch blocks and myocardial infarction).
- Prompt clarity and lead scaling significantly impact edge-case detection.
