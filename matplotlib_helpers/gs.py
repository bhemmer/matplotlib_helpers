import re

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def gs_axs(
    row_height=[1],
    column_width=[1],
    sharex=False,
    sharey=False,
    keep_extra_dimensions=False,
    **gs_kwargs
):
    """generate grid of subplots with shared one axis
    Args:
        - row_height (list): list specifying the height of each subplot row. The number
            of list entries defines the number of rows in subplot grid.
        - column_width (list): list specifying the width of each subplot column. The
            number of list entries defines the number of columns in subplot grid.
        - sharex (str): share x axis
        - sharey (str): share y axis
        - keep_extra_dimensions (bool): True, if you want the full 2D nested list of
            axes including lists with single entries.
        - **gs_kwargs (dict): remaining kwargs are passed on to
            matplotlib.gridspec.GridSpec

    Returns:
        - (nested) list of matplotlib AxesSubplot objects. Outer list contains a list
            for each subplot row, inner list(s) contain subplot ax for each field.
    """

    n = sum(row_height)
    m = sum(column_width)

    # generate grid of subplots, possibly with shared axis

    gs = GridSpec(n, m, **gs_kwargs)
    axs = []

    for i, rh in enumerate(row_height):  # iterate rows
        axline = []
        rstart = sum(row_height[:i])
        for j, cw in enumerate(column_width):  # iterate columns
            cstart = sum(column_width[:j])

            if i == 0:  # first row share only y, but not for first subplot
                if sharey and j != 0:
                    axline.append(
                        plt.subplot(
                            gs[rstart : rstart + rh, cstart : cstart + cw],
                            sharey=axline[0],
                        )
                    )
                else:
                    axline.append(
                        plt.subplot(gs[rstart : rstart + rh, cstart : cstart + cw])
                    )
            elif j == 0:  # first column share only x
                if sharex:
                    axline.append(
                        plt.subplot(
                            gs[rstart : rstart + rh, cstart : cstart + cw],
                            sharex=axs[0][j],
                        )
                    )
                else:
                    axline.append(
                        plt.subplot(gs[rstart : rstart + rh, cstart : cstart + cw])
                    )
            else:  # all others share both
                if sharex and sharey:
                    axline.append(
                        plt.subplot(
                            gs[rstart : rstart + rh, cstart : cstart + cw],
                            sharex=axs[0][j],
                            sharey=axline[0],
                        )
                    )
                elif sharex:
                    axline.append(
                        plt.subplot(
                            gs[rstart : rstart + rh, cstart : cstart + cw],
                            sharex=axs[0][j],
                        )
                    )
                elif sharey:
                    axline.append(
                        plt.subplot(
                            gs[rstart : rstart + rh, cstart : cstart + cw],
                            sharey=axline[0],
                        )
                    )
                else:
                    axline.append(
                        plt.subplot(gs[rstart : rstart + rh, cstart : cstart + cw])
                    )

        axs.append(axline)

    # get rid of nested lists, if dimension < 2
    if not keep_extra_dimensions:
        if len(column_width) == 1 and len(row_height) == 1:
            axs = axs[0][0]
        elif len(column_width) == 1:
            axs = [axline[0] for axline in axs]
        elif len(row_height) == 1:
            axs = [ax for ax in axs[0]]

    return axs


def fmt_gs_axs(
    axs,
    timescale=None,
    sharex=False,
    sharey=False,
    colored_labels=False,
):
    """format axis of subplot grid

    Args:
        - axs (list): nested list of subplots. First level represents rows, second level
            represents columns, as output by gs_axs.
        - timescale (str): one of ['h', 'd', 'm] for hour, day, week, month, or year
            (default: None)
        - sharex, sharey (bool): specify which axis are shared in axs list, to leave out
            some ticklabels.
        - colored_labels (bool):
        - wvn_and_wvl (bool): use wvn on bottom and wvl on top xaxis
    """

    # ensure 2 dimensions

    axs, original_dim = _ensure_2_dim(axs, sharex=sharex)

    # x ticks for dates
    for axline in axs:
        for ax in axline:
            if timescale is None:
                pass
            elif timescale in ["hour", "h"]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                ax.xaxis.set_major_locator(mdates.HourLocator())
            elif re.match(r"\dh", timescale):
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                ax.xaxis.set_major_locator(mdates.HourLocator())
                interval = int(
                    re.match(r"(?P<interval>\d)h", timescale).group("interval")
                )
                ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
            elif timescale in ["day", "d"]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M"))
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            elif re.match(r"\dd", timescale):
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m."))
                interval = int(
                    re.match(r"(?P<interval>\d)d", timescale).group("interval")
                )
                ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
            elif timescale in ["week", "w"]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m."))
                ax.xaxis.set_major_locator(mdates.DayLocator())
            elif timescale in ["month", "m"]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
                ax.xaxis.set_major_locator(mdates.MonthLocator())
            elif timescale in ["year", "y"]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%y"))
                ax.xaxis.set_major_locator(mdates.YearLocator())

    # plot x ticks on uppermost and under lowest subplot

    if sharex:
        for axline in axs:
            for ax in axline:
                ax.tick_params(labelbottom=False, labeltop=False)
        for ax in axs[0]:
            ax.tick_params(labeltop=True)
        for ax in axs[-1]:
            ax.tick_params(labelbottom=True)
    if sharey:
        for axline in axs:
            for ax in axline:
                ax.tick_params(labelleft=False, labelright=False)
            axline[0].tick_params(labelleft=True)
            axline[-1].tick_params(labelright=True)
            if len(axline) > 1:
                axline[-1].yaxis.set_label_position("right")

    # set label and tick color

    if colored_labels:
        for axline in axs:
            for ax in axline:
                try:  # get color from subplot
                    c = ax.get_lines()[0].get_color()
                except IndexError:  # handle empty subplots
                    c = "black"
                if sharex and sharey:  # would result in single color, senseless
                    pass
                elif sharex:
                    ax.tick_params(axis="y", labelcolor=c)
                    ax.set_ylabel("", color=c)
                elif sharey:
                    ax.tick_params(axis="x", labelcolor=c)
                    ax.set_xlabel("", color=c)

    # get rid of extra dimensions
    axs = _return_original_dim(axs, original_dim=original_dim, sharex=sharex)

    return axs


def wvn_and_wvl(axs, sharex=False, conversion_factor=1e4):
    """add wvl axis on top of plots"""

    axs, original_dim = _ensure_2_dim(axs, sharex=sharex)

    axs_wvl = []
    for axline in axs:  # create wvl axis at top
        axs_wvl.append(
            [
                ax.secondary_xaxis(
                    "top",
                    functions=(
                        lambda x: conversion_factor / x,
                        lambda x: conversion_factor / x,
                    ),
                )
                for ax in axline
            ]
        )
    for axline in axs:
        for ax in axline:  # turn off top ticks for wvn axis
            ax.tick_params(labeltop=False, top=False, which="both")
    if sharex:
        for axline in axs_wvl:
            for ax in axline:  # turn off tick labels for wvl axis
                ax.tick_params(labeltop=False, which="both")
        for ax in axs_wvl[0]:  # turn on tick labels for topmost wvl axis
            ax.tick_params(labeltop=True)

    axs = _return_original_dim(axs, original_dim=original_dim, sharex=sharex)
    axs_wvl = _return_original_dim(axs_wvl, original_dim=original_dim, sharex=sharex)

    return axs, axs_wvl


def _ensure_2_dim(axs, sharex=False):
    original_dim = 2
    if type(axs) != list:
        axs = [[axs]]
        original_dim = 0
    elif type(axs) == list and type(axs[0]) != list:
        if sharex:
            axs = [[ax] for ax in axs]
        else:
            axs = [axs]
        original_dim = 1
    return axs, original_dim


def _return_original_dim(axs, original_dim, sharex=False):
    if original_dim == 0:
        axs = axs[0][0]
    elif original_dim == 1 and sharex:
        axs = [axline[0] for axline in axs]
    elif original_dim == 1:
        axs = [ax for ax in axs[0]]
    return axs
