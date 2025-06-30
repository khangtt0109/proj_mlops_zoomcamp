#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime
import os


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def create_test_data():
    """Create and upload test data to S3"""
    # Test data from Q3
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]

    df_input = pd.DataFrame(data, columns=columns)

    # Set up S3 endpoint for Localstack
    s3_endpoint_url = "http://localhost:4566"
    options = {"client_kwargs": {"endpoint_url": s3_endpoint_url}}

    # Save to S3 as if it's January 2023 data
    input_file = "s3://nyc-duration/in/2023-01.parquet"

    df_input.to_parquet(
        input_file,
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=options,
    )

    print(f"Test data saved to {input_file}")


def run_integration_test():
    """Run the complete integration test"""
    # Set environment variables for batch.py
    os.environ["S3_ENDPOINT_URL"] = "http://localhost:4566"
    os.environ["INPUT_FILE_PATTERN"] = (
        "s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
    )
    os.environ["OUTPUT_FILE_PATTERN"] = (
        "s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
    )

    # Run batch.py for January 2023
    print("Running batch.py for January 2023...")
    result = os.system("python batch.py 2023 1")

    if result != 0:
        print("Error: batch.py failed to run")
        return

    # Read the output from S3
    options = {"client_kwargs": {"endpoint_url": "http://localhost:4566"}}
    output_file = "s3://nyc-duration/out/2023-01.parquet"

    try:
        df_result = pd.read_parquet(output_file, storage_options=options)
        sum_durations = round(df_result["predicted_duration"].sum(), 2)
        print(f"Sum of predicted durations: {sum_durations}")
        return sum_durations
    except Exception as e:
        print(f"Error reading output file: {e}")
        return None


if __name__ == "__main__":
    # Step 1: Create test data
    create_test_data()

    # Step 2: Run integration test
    run_integration_test()
