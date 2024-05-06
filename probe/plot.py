# %% Imports

import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% Load poas data

poas = pd.read_csv("data/poas.csv")
N = len(poas[poas["partition"] != "test"])

# %% Load data

data = pd.read_csv("probe/results.csv")
data["log10_data_size"] = np.log10(data["data_size"])
data["actual_size"] = (data["data_size"] * N).round()
data["chain"] = data["chain"].str[3:].str.title()

# %% Compute best subtable

# Source: https://stackoverflow.com/a/54471056
best = data.loc[
    data.groupby(
        ["chain", "data_size"],
    )["avg_wd"].idxmin()
].reset_index(drop=True)

# %% Best wd vs. size


def g(legend):
    col = color = alt.Color("chain", title="Antibody chain")
    if not legend:
        col = col.legend(None)

    return alt.Chart(best).encode(
        x=alt.X(
            "actual_size",
            scale=alt.Scale(
                type="log",
                domain=[100, 2000000],
            ),
            title="Dataset size",
            axis=alt.Axis(
                grid=False,
                values=[10**i for i in range(2, 7)],
            ),
        ),
        y=alt.Y(
            "avg_wd",
            title="Antibody likeness (lower is better)",
            scale=alt.Scale(domain=[0, 0.3]),
        ),
        color=col,
        tooltip=["chain", "data_size", "actual_size", "sigma", "avg_wd"],
    )


c = (
    alt.layer(
        g(False).mark_line(),
        g(True).mark_circle(size=60, opacity=1),
        alt.Chart(
            pd.DataFrame(
                {
                    "val": [0.065, 0.062],
                    "chain": ["dWJS", "SeqVDM (SOTA)"],
                }
            )
        )
        .mark_rule()
        .encode(
            y=alt.Y("val"),
            color=alt.Color(
                "chain",
                scale=alt.Scale(range=["red", "indigo"]),
                title="Reported values",
            ),
            size=alt.value(2),
        ),
    )
    .resolve_scale(color="independent")
    .properties(
        width=600,
        height=300,
    )
    .configure_view(stroke=None)
    .interactive()
)


c.save("probe/plots/wd_vs_size.html")
c.save("probe/plots/wd_vs_size.png", ppi=300)


# %% Best wd vs. sigma


def g(chain, legend):
    col = alt.Color(
        "actual_size",
        title="Dataset size",
        scale=alt.Scale(
            type="log",
            scheme="blues" if chain == "Heavy" else "oranges",
            domain=[1e2, 1e6],
        ),
    )
    if not legend:
        col = col.legend(None)

    return alt.Chart(data[data["chain"] == chain]).encode(
        x=alt.X(
            "sigma",
            title="σ (noise level)",
            scale=alt.Scale(domain=[0.05, 0.95]),
            axis=alt.Axis(
                values=[0.1, 0.3, 0.5, 0.7, 0.9],
                grid=False,
            ),
        ),
        y=alt.Y(
            "avg_wd",
            title="Antibody likeness (lower is better)",
            scale=alt.Scale(domain=[0, 0.3]),
        ),
        color=col,
        tooltip=["chain", "data_size", "actual_size", "sigma", "avg_wd"],
    )


for chain in ["Heavy", "Light"]:
    c = (
        alt.layer(
            g(chain, False).mark_point(filled=True, size=60, opacity=1),
            g(chain, True).mark_line(),
        )
        .resolve_scale(color="independent")
        .properties(
            width=600,
            height=300,
        )
        .configure_view(stroke=None)
        .interactive()
    )

    c.save(f"probe/plots/wd_vs_sigma_{chain}.html")
    c.save(f"probe/plots/wd_vs_sigma_{chain}.png", ppi=300)

# %% sigma vs. size


c = alt.Chart(best).encode(
    x=alt.X(
        "actual_size",
        scale=alt.Scale(
            type="log",
            domain=[100, 2000000],
        ),
        title="Dataset size",
        axis=alt.Axis(
            grid=False,
            values=[10**i for i in range(2, 7)],
        ),
    ),
    y=alt.Y(
        "sigma",
        title="σ (noise level)",
        scale=alt.Scale(domain=[0.05, 0.95]),
        axis=alt.Axis(
            values=[0.1, 0.3, 0.5, 0.7, 0.9],
        ),
    ),
    color=alt.Color("chain", title="Antibody chain"),
    tooltip=["chain", "data_size", "actual_size", "sigma", "avg_wd"],
)

c = (
    alt.layer(
        c.mark_line(),
        c.mark_point(filled=True, opacity=1, size=60),
    )
    .properties(
        width=600,
        height=300,
    )
    .configure_view(stroke=None)
    .interactive()
)


c.save("probe/plots/sigma_vs_size.html")
c.save("probe/plots/sigma_vs_size.png", ppi=300)
