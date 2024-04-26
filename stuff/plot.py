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

# %% Compute mins

# Source: https://stackoverflow.com/a/54471056
mins = data.loc[data.groupby(["chain", "data_size"])["avg_wd"].idxmin()].reset_index(drop=True)


# %% wd vs. size


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
    y=alt.Y("avg_wd"),
    color="chain",
    tooltip=["chain", "data_size", "actual_size", "sigma", "avg_wd"],
)

c = (
    alt.layer(
        c.mark_line(),
        c.mark_point(),
    )
    .properties(
        width=800,
        height=500,
    )
    .interactive()
)


c.save("stuff/plots/wd_vs_size.html")

# %% wd vs. sigma

c = alt.Chart(data).encode(
    x=alt.X("sigma"),
    y=alt.Y("avg_wd"),
    color=alt.Color(
        "data_size",
        scale=alt.Scale(
            type="log",
            scheme="blues",
        ),
        type="ordinal",
    ),
    tooltip=["chain", "data_size", "actual_size", "sigma", "avg_wd"],
)

c = (
    alt.layer(
        c.mark_line(),
        c.mark_point(),
    )
    .properties(
        width=800,
        height=500,
    )
    .facet(
        column="chain",
    )
    .interactive()
)


c.save("stuff/plots/wd_vs_sigma.html")

# %% sigma vs. size


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
    y=alt.Y("sigma", scale=alt.Scale(domain=[0, 1])),
    color="chain",
    tooltip=["chain", "data_size", "actual_size", "sigma", "avg_wd"],
)

c = (
    alt.layer(
        c.mark_line(),
        c.mark_point(),
    )
    .properties(
        width=800,
        height=500,
    )
    .interactive()
)


c.save("stuff/plots/sigma_vs_size.html")
