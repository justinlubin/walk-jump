# %% Imports

import altair as alt
import numpy as np
import pandas as pd

# %% Load poas data

poas = pd.read_csv("data/poas.csv")
N = len(poas[poas["partition"] != "test"])

# %% Load data

data = pd.read_csv("stuff/results.csv")
data["log10_data_size"] = np.log10(data["data_size"])
data["actual_size"] = (data["data_size"] * N).round()

data = (
    data.groupby(
        ["chain", "data_size", "sigma"],
    )
    .mean()
    .reset_index()
)


# %% Plot

mins = data.loc[data.groupby(["chain", "data_size"])["avg_wd"].idxmin()].reset_index()

c = alt.Chart(mins).encode(
    x=alt.X(
        "data_size",
        scale=alt.Scale(
            type="log",
            domain=[
                data["data_size"].min() / 2,
                data["data_size"].max() * 2,
            ],
        ),
    ),
    y=alt.Y("avg_wd:Q"),
    color="chain",
    tooltip=["chain", "data_size", "actual_size", "sigma", "avg_wd"],
)
c = alt.layer(c.mark_line(), c.mark_point()).properties(width=800, height=500).interactive()


c.save("stuff/plots/wd_vs_size.html")
