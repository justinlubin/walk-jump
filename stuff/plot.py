# %% Imports

import pandas as pd
import altair as alt

# %% Load data

data = pd.read_csv("stuff/results.csv")

# %% Plot

c = (
    alt.Chart(data)
    .mark_point()
    .encode(
        x="data_size",
        y="avg_wd",
        color="sigma",
    )
    .interactive()
)


c.save("plots.html")
