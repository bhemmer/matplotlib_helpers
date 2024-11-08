import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_lineset(x_list, y_list, parameter, ax=None, colormap="viridis", **kwargs):
    """plot a set of parameterized lines

    Args:
        x_list (np.array or list): single (if same for all y) or set of x values
        y_list (np.array or list): set of y values
        parameter (np.array or list):

    Returns:
        - ax
        - colorbar
    """
    if not ax:
        ax = plt.gca()

    if np.shape(x_list) == np.shape(y_list):
        pass
    elif len(np.shape(x_list)) == len(np.shape(y_list)) - 1:
        x_list = [x_list for y in y_list]
    else:
        raise ValueError(
            f"shape of x_list {np.shape(x_list)} does not match \
                shape of y_list {np.shape(y_list)}"
        )

    if len(parameter) != len(y_list):
        raise ValueError(
            f"len(parameter) {len(parameter)} does not match len(y_list) {len(y_list)}"
        )

    norm = matplotlib.colors.Normalize(vmin=np.min(parameter), vmax=np.max(parameter))
    cm = matplotlib.cm.get_cmap(colormap)
    sm = matplotlib.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])

    for x, y, p in zip(x_list, y_list, parameter):
        ax.plot(x, y, color=sm.to_rgba(p), **kwargs)

    colorbar = plt.colorbar(sm, ax=ax)

    return ax, colorbar
