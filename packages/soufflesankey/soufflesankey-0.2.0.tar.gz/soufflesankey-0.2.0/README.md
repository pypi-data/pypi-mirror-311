# SouffleSankey

A Python package for creating Sankey diagrams with a focus on mobile app analytics visualization.

## Installation

```bash
pip install soufflesankey
```

## Quick Start

```python
from soufflesankey import SouffleSankey

# Create a new Sankey diagram
sankey = SouffleSankey()

# Add flows
sankey.add_flow('Start', 'End', 100)

# Create and show the plot
fig = sankey.plot()
fig.show()
```

## Features
- Easy-to-use API for creating Sankey diagrams
- Support for custom colors and styling
- Built-in support for funnel analysis
- Integration with Plotly for interactive visualizations

## License
MIT License
