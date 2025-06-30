# MLOps Zoomcamp Homeworks

This repository contains code and solutions for the MLOps Zoomcamp course homeworks, covering the full ML lifecycle: data processing, model training, hyperparameter optimization, experiment tracking, and model registration using MLflow.

---

## Project Structure

```
mlops_zoomcamps/
├── artifacts/                # MLflow artifacts (models, plots, etc.)
├── data/
│   ├── homework_1/           # Raw data for Homework 1
│   ├── homework_2/           # Raw data for Homework 2
│   └── homework_3/           # Raw data for Homework 3
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
├── README.md                 # This file
├── homework_4/               # Homework 4: Dockerized prediction
│   ├── predict.py            # Prediction script (CLI)
│   ├── Dockerfile            # Dockerfile for building the container
│   └── model.bin             # Pre-trained model and vectorizer (provided in base image)
```

---

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd mlops_zoomcamps
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

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

## Homework 3: Docker and MLflow Deployment

- **Goal:** Containerize the ML application and deploy MLflow tracking server using Docker.

### 1. Project Structure

```
mlops/
├── mlflow.dockerfile         # Dockerfile for MLflow server
├── docker-compose.yml        # Docker Compose configuration
├── mlflow_data/             # MLflow data storage
└── scripts/                 # Database initialization scripts
```

### 2. Start the Services

```bash
# Create necessary directories
mkdir -p mlflow_data
chmod 777 mlflow_data

# Start all services
docker-compose up --build
```

### 3. Access Services

- MLflow UI: http://localhost:5001
- Mage UI: http://localhost:6789

### 4. Features

- Containerized MLflow tracking server
- Persistent storage for MLflow data
- Integration with Mage platform
- PostgreSQL database with pgvector support
- Automatic service restart on failure

---

## Homework 4: Model Packaging and Docker

- **Goal:** Package the prediction script in a Docker container using a pre-built base image with the model and vectorizer.

### 1. Project Structure

```
homework_4/
├── predict.py      # CLI script for making predictions
├── Dockerfile      # Dockerfile for building the container
```

### 2. Build the Docker Image

Make sure you are in the `homework_4` directory:

```bash
cd homework_4

docker build -t taxi-prediction .
```

### 3. Run the Prediction Script in Docker

To predict the mean duration for a specific year and month (e.g., May 2023):

```bash
docker run -it taxi-prediction --year 2023 --month 5
```

- The script will output the mean predicted duration for the specified month.
- The model and vectorizer are already included in the base image (`agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim`).

---

## Homework 5: Monitoring and Data Quality

- **Goal:** Monitor data quality and model metrics for NYC Taxi trip duration prediction using Evidently, PostgreSQL, and Grafana.
- **Steps:**

  1. Download and prepare the March 2024 Green Taxi dataset.
  2. Expand data quality metrics using Evidently (e.g., add quantile and custom metrics).
  3. Store metrics in a PostgreSQL database for batch monitoring.
  4. Visualize metrics and data quality in Grafana dashboards.
  5. Save and manage dashboard configurations for reproducibility.

- **How to run:**

  - Open and run `homework_5.ipynb` in Jupyter Notebook.
  - Follow the notebook cells to process data, compute metrics, and interact with dashboards.

- **Main tools:**
  - Evidently (for data quality and drift metrics)
  - PostgreSQL (for metrics storage)
  - Grafana (for dashboard visualization)

---

## Homework 6: Testing, Integration, and S3 Mocking with Localstack

**Goal:** Refactor the batch inference code, add unit and integration tests, and mock S3 using Localstack for robust ML batch pipelines.

### 1. Refactor `batch.py`

- Move all logic into a `main(year, month)` function.
- Extract a `prepare_data(df, categorical)` function for data preprocessing.
- Remove all global variables; pass parameters explicitly.
- Add `get_input_path` and `get_output_path` functions to support environment-based input/output paths for both testing and production.

### 2. Unit Test for `prepare_data`

- Create a `homework_6/tests/` directory with a `test_batch.py` file.
- Write a test for `prepare_data` using a sample dataframe, checking that only valid rows are kept.
- Run the test:
  ```bash
  cd homework_6
  pytest tests/
  ```

### 3. Configure Localstack to Mock S3

- Create a `docker-compose.yaml` in `homework_6`:
  ```yaml
  services:
    localstack:
      image: localstack/localstack:latest
      ports:
        - "4566:4566"
      environment:
        - SERVICES=s3
        - DEBUG=1
        - DATA_DIR=/tmp/localstack/data
      volumes:
        - "/var/run/docker.sock:/var/run/docker.sock"
  ```
- Start Localstack:
  ```bash
  cd homework_6
  docker-compose up -d
  ```
- Create a mock S3 bucket:
  ```bash
  export AWS_ACCESS_KEY_ID=test
  export AWS_SECRET_ACCESS_KEY=test
  export AWS_DEFAULT_REGION=us-east-1
  aws s3 mb s3://nyc-duration --endpoint-url http://localhost:4566
  ```

### 4. Read/Write S3 via Localstack in `batch.py`

- Use the `S3_ENDPOINT_URL` environment variable and `storage_options` when reading/writing Parquet files with pandas.
- Add a `save_data(df, filename)` function to handle saving to S3 or local files.

### 5. Create Test Data and Run Integration Test

- Create `integration_test.py`:
  - Generate a test dataframe (same as the unit test).
  - Save it to the mock S3 bucket (Localstack).
  - Set environment variables for `batch.py`.
  - Call `batch.py` to process the batch.
  - Read the output file from S3 and compute the sum of predicted durations.
- Install the required package:
  ```bash
  pip install s3fs
  ```
- Run the integration test:
  ```bash
  python integration_test.py
  ```
- Expected output:
  ```
  Sum of predicted durations: 36.28
  ```

### 6. End-to-End Summary

- Refactor code, write unit tests, configure Localstack, and test the batch pipeline with mock S3 data.
- Ensure all steps are automated and easily repeatable.

---

**Quick Start for Homework 6:**

```bash
# Install required packages
pip install -r requirements.txt
pip install s3fs

# Start Localstack
cd homework_6
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
docker-compose up -d
aws s3 mb s3://nyc-duration --endpoint-url http://localhost:4566

# Run the integration test
python integration_test.py
```

**Expected final result:**

```
Sum of predicted durations: 36.28
```

---

## Requirements

All dependencies are listed in `requirements.txt`
