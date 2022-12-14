import click

from OneD import OneD
from TwoD import TwoD


@click.command()
@click.argument('dim', type=int)
@click.argument('bounds', type=str)
@click.option('-n', '--n_points', type=int, default=100,
              help='How many points should be rendered?')
@click.option('-r', type=str, default=None,
              help='Graph range. Ex.: "0., 1.". If range is not given the '
                   'graph will be displayed with an offset to both sides.')
@click.option('-a', '--a_points', type=int, default=1000000,
              help='How many points should be used to estimate the area under '
                   'the graph curves? (Works only for dim 1)')
@click.option('--show_hard', type=bool, default=False,
              help='Should the hard interval be shown too? True/False')
@click.option('--print_ratio', type=bool, default=True,
              help='Should the estimated ratio of hard interval to soft '
                   'interval area be printed? True/False '
                   '(Works only for dim 1)')
def plot(dim, bounds, n_points, r, show_hard, a_points, print_ratio):
    """Prints a graph of the Soft Interval for a DIM-dimensional
    Classifier with BOUNDS. Please enter BOUNDS in quotation marks.
    Ex.: "0.2 0.3". For multidimensional bounds please enter the
    lower and upper bound of each axis together. Example for 2D:
    "lower-x upper-x lower-y upper-y".
    """

    bounds = tuple(map(float, bounds.split()))
    r = tuple(map(float, r.split())) if r is not None else None

    p = None

    if dim == 1:
        p = OneD(*bounds, n_points, r, show_hard, a_points, print_ratio)
    elif dim == 2:
        p = TwoD(*bounds, n_points, r, show_hard)
    else:
        print("Sorry, I've got nothing :(")
        exit(0)

    p.plot()


if __name__ == "__main__":
    plot()
