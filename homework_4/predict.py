import argparse
import pickle
import pandas as pd
import numpy as np


def read_data(filename):
    df = pd.read_parquet(filename)

    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df


def main(year: int, month: int):
    # Load the model from the Docker image
    with open("model.bin", "rb") as f_in:
        dv, model = pickle.load(f_in)

    # Read the data
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet"
    df = read_data(url)

    # Prepare features
    categorical = ["PULocationID", "DOLocationID"]
    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)

    # Make predictions
    y_pred = model.predict(X_val)

    # Print mean predicted duration
    print(f"Mean predicted duration: {np.mean(y_pred):.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, required=True)
    args = parser.parse_args()

    main(args.year, args.month)
