import gzip

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

from morphomnist import idx


def plot_digit(x, ax=None, title=None, **kwargs):
    if ax is None:
        ax = plt.gca()
    def_kwargs = dict(cmap='gray_r')
    def_kwargs.update(**kwargs)
    ax.imshow(x.squeeze(), **def_kwargs)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    if title is not None:
        ax.set_title(title)


def plot_ellipse(x, y, angle, major, minor, ax, **kwargs):
    if ax is None:
        ax = plt.gca()
    ax.add_patch(Ellipse(xy=(x, y), width=2 * major, height=2 * minor,
                         angle=np.rad2deg(angle), **kwargs))


def plot_parallelogram(top_left, top_right, bottom_right, bottom_left, scale=1., ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()
    corners = [top_left, top_right, bottom_right, bottom_left, top_left]
    ax.plot(*(scale * np.array(corners).T - .5), **kwargs)


def save(data, path):
    with gzip.open(path, 'wb') as f:
        idx.save_uint8(data, f)


def load(path):
    with gzip.open(path, 'rb') as f:
        data = idx.load_uint8(f)
    return data
