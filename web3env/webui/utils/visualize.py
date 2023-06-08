import os
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm

DATA_PATH = os.environ.get('DATA_PATH')

def generate_plot():
    a2c_data = pd.read_csv(DATA_PATH + '/a2c.csv')
    # compare change of honest_proportion
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a2c_data.index, y=a2c_data["honest_proportion"], name="A2C"))

    fig.update_layout(title="Change of Honest Proportion",
                    xaxis_title="Epochs",
                    yaxis_title="Honest Proportion")
    fig.write_image(os.path.join(DATA_PATH, 'honest_proportion.png'))
    return 

