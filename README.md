# MLOps Zoomcamp Homeworks

This repository contains code and solutions for the MLOps Zoomcamp course homeworks, covering the full ML lifecycle: data processing, model training, hyperparameter optimization, experiment tracking, and model registration using MLflow.

---

## Project Structure

```
mlops_zoomcamps/
├── artifacts/                # MLflow artifacts (models, plots, etc.)
├── data/
│   ├── homework_1/           # Raw data for Homework 1
│   └── homework_2/           # Raw data for Homework 2
├── mlruns/                   # MLflow tracking directory
├── output/                   # Processed data and outputs
├── homework_1.ipynb          # Homework 1 notebook
├── homework_2.ipynb          # Homework 2 notebook
├── preprocess_data.py        # Data preprocessing script
├── train.py                  # Model training script
├── hpo.py                    # Hyperparameter optimization script
├── register_model.py         # Model registration script
├── mlflow.db                 # SQLite DB for MLflow tracking
├── requirements.txt          # Project dependencies
└── README.md                 # This file
```

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd mlops_zoomcamps
   ```

````

2. **Install dependencies:**
   ```bash
pip install -r requirements.txt
````

---

## Homework 1: NYC Taxi Trip Duration Prediction

- **Goal:** Predict taxi trip durations using linear regression.
- **Steps:**

  1. Load and clean the NYC Yellow Taxi trip data.
  2. Feature engineering and outlier removal.
  3. Train a linear regression model.
  4. Evaluate model performance using RMSE.

- **How to run:**
  - Open and run `homework_1.ipynb` in Jupyter Notebook.
  - Follow the notebook cells for data processing, feature engineering, model training, and evaluation.

---

## Homework 2: ML Lifecycle with MLflow

- **Goal:** Manage the full ML lifecycle for a RandomForestRegressor using MLflow, including hyperparameter optimization and model registration.

### 1. Preprocess the Data

```bash
python preprocess_data.py --raw_data_path ./data/homework_2 --dest_path ./output
```

### 2. Start the MLflow Tracking Server

```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./artifacts \
  --host 127.0.0.1 \
  --port 5001
```

### 3. Train a Baseline Model

```bash
python train.py --data_path ./output
```

### 4. Hyperparameter Optimization

```bash
python hpo.py
```

- This script uses Hyperopt to search for the best RandomForestRegressor hyperparameters.
- Each run logs the hyperparameters and validation RMSE to MLflow.

### 5. Register the Best Model

```bash
python register_model.py --data_path ./output --top_n 5
```

- This script selects the top 5 models from hyperopt, evaluates them on the test set, and registers the best one in the MLflow Model Registry.

### 6. Explore Results

Open the MLflow UI in your browser:

```
http://localhost:5001
```

- View experiments, runs, and the model registry.

---

## Requirements

All dependencies are listed in `requirements.txt`. Main packages:

- mlflow
- scikit-learn
- hyperopt
- click
- pandas
- numpy

---

## License

This project is for educational purposes as part of the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course.
