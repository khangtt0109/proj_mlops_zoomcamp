import pandas as pd
from datetime import datetime
import sys
import os

# Add the parent directory to the path so we can import batch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    # Test data
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
    df = pd.DataFrame(data, columns=columns)

    categorical = ["PULocationID", "DOLocationID"]

    # Apply the transformation
    result = prepare_data(df, categorical)

    # Expected output - only 2 rows should remain after filtering
    expected_data = [
        (
            -1,
            -1,
            dt(1, 1),
            dt(1, 10),
            9.0,
        ),  # Row 0: duration = 9 minutes, None values become -1
        (1, 1, dt(1, 2), dt(1, 10), 8.0),  # Row 1: duration = 8 minutes
    ]

    expected_columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "duration",
    ]
    expected_df = pd.DataFrame(expected_data, columns=expected_columns)

    # Convert categorical columns to string type (as done in prepare_data)
    expected_df[categorical] = expected_df[categorical].astype("str")

    # Assert that the result matches expected
    pd.testing.assert_frame_equal(result, expected_df, check_dtype=False)

    # Also check the number of rows
    assert len(result) == 2, f"Expected 2 rows, got {len(result)} rows"
