# %% Import

import glob

import pandas as pd
from walkjump.metrics import LargeMoleculeDescriptors
from walkjump.metrics import get_batch_descriptors

# %% Helper functions

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


# %% Load test data

test_data = pd.read_csv("data/poas.csv")

test_data = (
    test_data[test_data["partition"] == "test"]
    .drop(columns={"partition"})
    .reset_index(
        drop=True,
    )
)

ref_feats = samples_to_descriptors(test_data)

# %% Load samples and evaluate them

PREFIX = "stuff/samples/data-"

chains = []
data_sizes = []
sigmas = []
avg_wds = []
prop_valids = []

for chain in ["fv_heavy", "fv_light"]:
    for filename in glob.glob(f"{PREFIX}*.csv"):
        data_size, _, sigma = filename[len(PREFIX) : -4].split("-")

        data_size = float(data_size.replace("_", "."))
        sigma = float(sigma.replace("_", "."))

        feats = samples_to_descriptors(pd.read_csv(filename))

        _per_column_wd, avg_wd, _total_wd, prop_valid = get_batch_descriptors(
            feats,
            ref_feats=ref_feats,
            chain=chain,
        )

        chains.append(chain)
        data_sizes.append(data_size)
        sigmas.append(sigma)
        avg_wds.append(avg_wd)
        prop_valids.append(prop_valid)

results = pd.DataFrame(
    data={
        "chain": chains,
        "data_size": data_sizes,
        "sigma": sigmas,
        "avg_wd": avg_wds,
        "prop_valid": prop_valids,
    }
)

results.to_csv("stuff/results.csv", index=False)
