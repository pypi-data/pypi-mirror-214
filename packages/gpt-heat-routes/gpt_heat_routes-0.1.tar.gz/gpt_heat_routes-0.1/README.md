# Human Trafficking Route Visualizer

[![PyPI version]]()
[![License: MIT]]()

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

gpt_heat_routes is a Python library designed to assist researchers, analysts, and organizations in understanding and analyzing the routes taken by human traffickers. By providing a visual representation of trafficking routes and transportation hubs, this tool aims to enable stakeholders to develop more effective strategies and interventions to combat human trafficking.

This library leverages the power of geographic data and network analysis using libraries such as `networkx`, `osmnx`, `pandas`, `folium`, and `branca`. It enables users to create interactive maps with markers for transportation stations, clusters for sources, and visualizations of trafficking routes.

## Installation

Before installing, ensure you have Python 3.6 or later.

```sh
pip install gpt_heat_routes
```

## Usage

Below is a brief guide on how to use the Human Trafficking Route Visualizer. The library includes various functions that allow you to add transportation stations, source clusters, and custom colormaps to folium maps, as well as get and plot routes using network graphs.

```python
import human_trafficking_route_visualizer as htrv
import pandas as pd

# Load data (example DataFrame df with trafficking route data)
# ...

# Create a folium map object
M = ...

# Add transportation stations as markers on the folium map
M = htrv.add_tm_stations(M, df)

# Add source clusters to the folium map
M = htrv.add_source_clusters(M, df)

# Generate a route heatmap in one call
heatmap = htrv.get_route_heatmap(df, G, popup_vals="...")

# Display the map
heatmap
```

## Contributing
We encourage contributions to improve and extend the functionality of Human Trafficking Route Visualizer. If you are interested in contributing, please start by forking the repository, making changes, and submitting a pull request.


## License
LoveJustice international.

## Acknowledgments
This library was developed to provide support in the fight against human trafficking. We are grateful for the contributions and feedback from the community.
