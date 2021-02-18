from flask import Flask, render_template
import matplotlib
from func import *
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import vk
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random

app = Flask(__name__)
app.threaded = True


@app.route('/')
def hello_world():
    return 'Hello, Wold'


@app.route('/main')
def pog():
    friends_list = load_friends_list()
    edgelist = create_edgelist(friends_list)
    print(friends_list)
    print(edgelist)
    G = nx.from_pandas_edgelist(edgelist, 'from', 'to')
    print("G len:", len(G))
    colors = create_colors(G, friends_list)
    print(colors[:10])
    plt.figure(figsize=(60, 40))
    # Plot it
    nx.draw_kamada_kawai(
        G, with_labels=False, node_size=550,
        alpha=0.7, node_color=colors,
        edge_color="blue"
    )
    plt.savefig("fig.png")

    return 'jjj'


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    friends_list = load_friends_list()
    edgelist = create_edgelist(friends_list)
    print(friends_list)
    print(edgelist)
    G = nx.from_pandas_edgelist(edgelist, 'from', 'to')
    print("G len:", len(G))
    colors = create_colors(G, friends_list)
    print(colors[:10])
    fig = Figure(figsize=(60, 40))
    # Plot it


    return fig
