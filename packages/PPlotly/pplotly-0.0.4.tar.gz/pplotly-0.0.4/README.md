## PPlotly.py

It is a wrapper around `plotly.py`. Graph styles and functionalities are added to get scientific plots. 

### Quickstart

`pip install pplotly`

```python
import pplotly as pp
fig = pp.Figure()
fig = fig.add_trace(pp.Scatter(x=["a", "b", "c"], y=[1, 3, 2]))
fig.show()
```
All the `plotly` functionalities are available to use under `pplotly.plotly`

### Examples

#### Error plot
```python
import pplotly as pp
import numpy as np

fig = pp.make_errorplot(
    xaxis_title="X-Title",
    yaxis1_title="Y-Title [Unit]",
    yaxis2_title="Error [Unit]"
)

x_data = [1, 2, 3]
y1_data = [2.1, 2.2, 3.1]
y2_data = [2.15, 2.21, 3.05]

fig.add_trace(
    pp.Scatter(x=x_data, y=y1_data, name="Plot 1")
)

fig.add_trace(
    pp.Scatter(x=x_data, y=y2_data, name="Plot 2")
)

error = [abs(p2-p1) for p1, p2 in zip(y1_data, y2_data)]
rmse = np.sqrt(np.mean(np.array(error)**2))
fig.add_trace(pp.Scatter(x=x_data, y=error, name=f"Abs Error: RMSE = {round(rmse, 3)}"), row=2, col=1)
fig.show()
```

## Developer options

```bash
git clone 
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
```
