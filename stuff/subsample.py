# %% Import

import pandas as pd

# %% Load data

data = pd.read_csv("data/poas.csv")

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
    subsampled_datas.append(
        pd.concat(
            [
                subsample(test, p),
                subsample(val, p),
                subsample(train, p),
            ]
        ).reset_index(drop=True)
    )

for df in subsampled_datas:
    df.to_csv


# test_data = (
#    data[data["partition"] != "test"]
#    .reset_index(
#        drop=True,
#    )
# )

# %% Run

FEATURES = LargeMoleculeDescriptors.descriptor_names()


def aho_to_descriptor_dict(seq_aho, *, prefix):
    seq = seq_aho.replace("-", "")
    lmd = LargeMoleculeDescriptors.from_sequence(seq)
    d = lmd.asdict()
    return {f"{prefix}{k}": v for k, v in d.items() if k in FEATURES}


def samples_to_descriptors(samples, show_progress=None):
    descriptors = []
    for i, row in samples.iterrows():
        heavy = aho_to_descriptor_dict(row["fv_heavy_aho"], prefix="fv_heavy_")
        light = aho_to_descriptor_dict(row["fv_light_aho"], prefix="fv_light_")
        descriptors.append(heavy | light | dict(row))
        if show_progress and i % show_progress == 0:
            print(i / len(samples))
    return pd.DataFrame(descriptors)


a = samples_to_descriptors(test_data.iloc[0:5000])
b = samples_to_descriptors(test_data.iloc[5001:10000])

per_column_wd, avg_wd, total_wd, _ = get_batch_descriptors(
    b,
    ref_feats=a,
    chain="fv_heavy",
)
