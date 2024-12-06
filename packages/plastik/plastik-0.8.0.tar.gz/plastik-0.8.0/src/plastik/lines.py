"""Module that stores nice-to-have objects related to plotted lines."""

import itertools


def get_linestyle_dict() -> dict[str, str | tuple]:
    """Get back a dictionary of dense but non-solid line styles.

    Returns
    -------
    dict[str, str | tuple]
        Dictionary with a descriptive name and value of some nice and dense matplotlib
        line styles.

    Notes
    -----
    See <https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html>.
    """
    return {
        "dotted": ":",
        "dashed": "--",
        "dashdot": "-.",
        "long dash with offset": (5, (10, 3)),
        "densely dashed": (0, (5, 1)),
        "densely dashdotted": (0, (3, 1, 1, 1)),
        "densely dashdotdotted": (0, (3, 1, 1, 1, 1, 1)),
    }


def get_linestyle_cycle() -> itertools.cycle:
    """Get back an object cycling some dense but non-solid line styles.

    Returns
    -------
    itertools.cycle
        An object that will cycle matplotlib line styles.

    Examples
    --------
    >>> ls = get_linestyle_cycle()
    >>> next(ls)
    :

    >>> next(ls)
    --
    """
    return itertools.cycle(list(get_linestyle_dict().values()))
