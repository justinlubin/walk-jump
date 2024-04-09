# %% Import

import pandas as pd

import shutil
import gzip

# %% Load data

DATA_DIR = "data"

data = pd.read_csv(f"{DATA_DIR}/poas.csv")

# %% Run

PERCENTS = [
    0.0001,
    0.001,
    0.01,
    0.1,
    0.33,
    0.5,
]

test = data[data["partition"] == "test"]
val = data[data["partition"] == "val"]
train = data[data["partition"] == "train"]

subsampled_datas = []


def subsample(df, p):
    return df.sample(frac=p, random_state=0)


for p in PERCENTS:
    p_str = str(p).replace(".", "_")
    filename = f"{DATA_DIR}/poas-{p_str}.csv"

    pd.concat(
        [
            subsample(test, p),
            subsample(val, p),
            subsample(train, p),
        ]
    ).reset_index(
        drop=True
    ).to_csv(filename)

    with open(filename, "rb") as f_in:
        with gzip.open(filename + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
