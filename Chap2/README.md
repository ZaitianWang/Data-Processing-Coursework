# Chapter 2 Homework

## Purpose

Anomaly detection

## Algorithms

- K-Means
- DTI
- Distance-Based

## Optimal Parameters/Trained Model
- K-Means
  - k = 5
  - threshold = 0.01
- DTI
  - DT_leaves = `[[False, False, True], True, [False, True, True]]`
- Distance Based
  - r = 0.075
  - pi = 0.003

## Performance Evaluation

|                | precision | recall |
| :------------- | --------- | ------ |
| K-Means        | 0.4       | 1.0    |
| DTI            | 0.375     | 0.75   |
| Distance Based | 0.5       | 1.0    |
