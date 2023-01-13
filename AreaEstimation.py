import random
import click
import numpy as np
import matplotlib.pylab as plt

from OneD import OneD


@click.command()
@click.option('-p', type=int, default=10000,
              help='How many points should be generated for the area '
                   'estimation?')
@click.option('-i', type=int, default=10,
              help='For how many random intervals should the area be '
                   'estimated?')
def estimate(p, i):
    """Prints the ratio of the estimated area hard-/soft-interval of i-many
    intervals with p-many points used for area estimation and a total average
    of all ratios.
    """

    x = []
    y = []
    average = []
    sizes = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7,
             0.75, 0.8, 0.85, 0.9, 0.95, 1]

    for s in sizes:
        ratios = []
        for _ in range(i):
            l = random.uniform(0, 1 - s)
            r = random.uniform(l, l + s)
            d = OneD(l, r, a_points=p)
            hard, soft = d.area_ratio()
            try:
                ratios.append(hard/soft)
            except ZeroDivisionError:
                ratios.append(0.0)

            # print(f"[{l}; {r}]: {hard/soft}")

        x.extend([s] * len(ratios))
        y.extend(ratios)
        average.append(sum(ratios)/len(ratios))
        # print(f"The average ratio of the estimated area hard/soft for "
        #      f"interval of size {s}: {sum(ratios)/len(ratios)}")

    plt.style.use("seaborn-darkgrid")
    plt.scatter(x, y)
    plt.plot(sizes, average, color='m', label="average per size")
    plt.xlabel("Interval Size")
    plt.ylabel("Ratios")
    plt.axhline(y=np.nanmean(y), color='green', label="total average", ls='--')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    estimate()
