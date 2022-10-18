import click
from OneD import OneD
from TwoD import TwoD


@click.command()
@click.argument('dim', type=int)
@click.argument('bounds', type=str)
# @click.option('-d', '--dim', type=int, default=1, prompt='Please enter the number of dimensions:',
#               help='Soft Integral dimensions')
# @click.option('-b', '--bounds', type=str, prompt='Please enter the classifier bounds:',
#               help='The lower and upper bounds of the classifier. Ex. "0.2, 0.3"')
@click.option('--n_points', type=int, default=100, help='How many points should be rendered?')
@click.option('--range', type=str, default="0. 1.", help='Graph range. Eg.: \"0., 1.\"')
@click.option('--show_hard', type=bool, default=False, help='Should the hard interval be shown too? True/False')
def plot(dim, bounds, n_points, range, show_hard):
    """Prints a graph of the Soft Interval for a DIM-dimensional Classifier with BOUNDS.
    Please enter BOUNDS in quotation marks. Ex.: \"0.2 0.3\" """

    bounds = tuple(map(float, bounds.split()))
    range = tuple(map(float, range.split()))
    p = None

    if dim == 1:
        p = OneD(*bounds, n_points, range, show_hard)
    elif dim == 2:
        p = TwoD(*bounds, n_points, range, show_hard)
    else:
        print("Sorry, I've got nothing :(")
        exit(0)

    p.plot()


if __name__ == '__main__':
    plot()
