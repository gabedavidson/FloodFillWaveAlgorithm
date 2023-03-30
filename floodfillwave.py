from __future__ import annotations

import math as m


def ff_w(grid: list[list], start: tuple = (0, 0), strength: float = 1.0, strength_anchor: int = 1,
         stage_strength_params: tuple = (False, None, None), reach: int = -1,
         default_increase_ceil: bool = True, default_jump_ceil: bool = False, avoid: list = None,
         post_avoid_fill: bool = True, func=None, func_inplace: bool = False, override_func_nones: bool = False,
         catch_func_nones: bool = False, save_stages: bool = True, shape: str | list = 0, shpd_sep: chr = ','):
    """
    This function impacts a 2-D or 3-D grid given some function func(...) following the wave shape of some shape.
    The 'shape' must following this format: (shape)(dimension)_(shape coefficients)&(second level function)|     ->
    (second level function coefficients)|(second level function operation)&(third...)|(...)|(...)&....
    :param grid: The grid to impact with func(...).
    :param start: The coordinate [x, y] to begin wave at.
    :param strength: The strength of the increase in current reach of wave.
    :param strength_anchor: The anchor against which to compare strength parameter value.
    :param stage_strength_params: [0]: Should the increase in current reach of wave compound with that of the iteration before.
                                            [1]: The maximum strength of increase.
                                            [2]: The maximum incremental strength of increase as %.
    :param reach: The maximum amount of tiles this wave can advance along an axis. -1 for total fill.
    :param default_increase_ceil: Default True. ceil(i) or floor(i) real strength values.
    :param default_jump_ceil: Default False. Automatically adjust total real impact to ceil(i) or not.
    :param avoid: Tile coordinates ([[x, y], ...]) to not impact with func(...).
    :param post_avoid_fill: Default True. Impact tiles hidden behind obstacles.
    :param func: Defaults None. The function to apply to impacted tiles.
    :param func_inplace: Defaults False. This function impacts the tile in-place or not.
    :param override_func_nones: Defaults False. If the impact of func(...) is None, override change to previous value.
    :param catch_func_nones: Defaults False. If the impact of func(...) is None, throw an Exception.
    :param save_stages: Default True. Save the individual impact of each iteration in a list.
    :param shape: Default 0. Designated name or index of shape type. Possible types: ['rhombus2', 'circle2', 'rhombus3', 'circle3', 'wave']
    :param shpd_sep: Defaults ','. Designates the separator used in shape details.
    :return: None or list
    """

    # grid & allowable default parameter checks
    assert len(grid) > 0, "Grid cannot be one-dimensional."
    assert len(stage_strength_params) == 3
    assert stage_strength_params[1] is not None and stage_strength_params[2] is not None if \
        stage_strength_params[0] else True

    # preliminary shape type check
    shapes = ['rhombus2', 'circle2', 'rhombus3', 'circle3', 'wave']
    assert shape < len(shapes) if isinstance(shape, int) else all([s.startswith(shape) for s in shapes]) if isinstance(
        shape, str) else False

    # func(...) runtime exception and return value checks
    assert func is not None, "func parameter cannot be None."
    assert override_func_nones is not catch_func_nones if override_func_nones or catch_func_nones else True, "Cannot override func(...) None impact and catch func(..) None impact at the same time."
    try:
        if func_inplace:
            g_tmp = [r[:] for r in g]
            func(g, 0, 0)
            assert g_tmp[0][0] is not None
            del g_tmp
        else:
            assert func(g[0][0]) is not None
    except Exception as e:
        raise Exception(f"func(t) threw the following exception -> {e}")

    # determining shape details
    wavef = None

    if isinstance(shape, int):
        wavef = lambda x, y: abs(y) <= abs(x)
    elif isinstance(shape, str):
        sdetails = [[float(c) for c in shape.split('&')[0][shape.index('_') + 1:].split(shpd_sep)], [[_d.split(',') if i != 1 else [float(c) for c in d.split('|')[1].split(',')] for i, _d in enumerate(d.split('|'))] for d in shape.split('&')[1:]]]

        # determining wave function to use
        if shape.startswith('rhombus2'):
            if len(sdetails[0]) == 1:  # degree of interior side angles

                wavef = lambda x: m.sin(sdetails[0][0]*m.pi/180)  # returns area
                wavef = lambda x: False

                print(m.sin(sdetails[0][0]*m.pi/180))

    stages = [] if save_stages else None

    w, h = len(grid[0]), len(grid)

    total_coverage = 1
    curr_strength = strength / strength_anchor

    def _rff_w(ax, ay):
        def at_limit():
            """
            The reach of edge is at a designated limit. Do not fill past this.
            :return:
            """
            return ax == w or ax == 0 or ay == h or ay == 0 or ax == (reach if reach != -1 else w) or ay == (
                reach if reach != -1 else h)

        save_stage()

    def rotate(x, y, deg: int = 90):
        theta = deg*m.pi/180
        return x*m.cos(theta) - y*m.sin(theta), y*m.cos(theta) + x*m.sin(theta)

    def save_stage():
        ...

    def impact(**kwargs):  # fixme add coverage for avoid functionality
        if func_inplace:
            func(g, kwargs['ax'], kwargs['ay'])
        else:
            g[kwargs['ax']][kwargs['ay']] = func(g[kwargs['ax']][kwargs['ay']])

    def signless_ceil(n):
        sign = -1 if n < 0 else 1
        return m.ceil(n * sign) * sign

    def signless_floor(n):
        sign = -1 if n < 0 else 1
        return m.floor(n * sign) * sign

    _rff_w(start[0], start[1])


def my_func(g: list, ax, ay):
    # _t = t
    _t = 'X'


w, h = 15, 12

g = [['_' for _ in range(w)] for _ in range(h)]
_start = (w // 2, h // 2)

f_not_inplace = lambda t: ord(t)

def f_in_place(g, ax, ay):
    g[ay][ax] = 1.9


# ff_w(g, _start, stage_strength_compounds_params=(True, 3, .4), func=f_not_inplace, func_inplace=False)
for i in range(0, -3, -1):
    print(i)
