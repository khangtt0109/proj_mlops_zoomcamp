# MLOps Zoomcamp Homework

This repository contains solutions and code for the MLOps Zoomcamp course homework assignments.

## Project Structure

- `data/` - Contains datasets used for the homework assignments.
- `output/` - Contains processed data and model outputs.
- `artifacts/` - Stores MLflow artifacts (models, plots, etc.).
- `mlflow.db` - SQLite database for MLflow tracking.
- `homework_1.ipynb` - Jupyter notebook for Homework 1.
- `homework_2.ipynb` - Jupyter notebook for Homework 2.
- `preprocess_data.py` - Script for data preprocessing.
- `train.py` - Script for training a RandomForestRegressor and logging with MLflow.
- `hpo.py` - Script for hyperparameter optimization using Hyperopt and MLflow.
- `register_model.py` - Script for evaluating and registering the best model in the MLflow Model Registry.

## ML Lifecycle with MLflow

### 1. Start the MLflow Tracking Server

```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./artifacts \
  --host 127.0.0.1 \
  --port 5001
```

### 2. Preprocess the Data

```bash
python preprocess_data.py --raw_data_path ./data/homework_2 --dest_path ./output
```

### 3. Train a Baseline Model

```bash
python train.py --data_path ./output
```

### 4. Hyperparameter Optimization

Run hyperparameter search and log results to MLflow:

```bash
python hpo.py
```

### 5. Register the Best Model

Evaluate the top models on the test set and register the best one:

```bash
python register_model.py --data_path ./output --top_n 5
```

### 6. Explore Results

Open the MLflow UI in your browser:

## Getting Started

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   ```
2. Install dependencies (see the notebook for required Python packages).
3. Download the required data into the `data/` directory.
4. Open and run the Jupyter notebook:
   ```bash
   jupyter notebook homework_1.ipynb
   ```

## Homework 1 Overview

- Reads NYC Yellow Taxi trip data for January and February 2023.
- Computes trip durations, filters outliers, and applies one-hot encoding to categorical features.
- Trains a linear regression model to predict trip duration.
- Evaluates model performance using RMSE.

## License

This project is for educational purposes as part of the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course.
