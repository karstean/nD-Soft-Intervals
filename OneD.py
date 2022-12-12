import math
import random

import numpy as np
import matplotlib.pyplot as plt


class OneD:
    def __init__(self, l_k, u_k, n_points=100, r=None, show_hard=False,
                 a_points=1000000, print_ratio=True):
        self.l_k = l_k  # Lower bound
        self.u_k = u_k  # Upper bound

        # Show what a hard interval would look like in this case
        self.show_hard = show_hard

        # Various help variables for soft interval calculation
        self.b_k = self.u_k - self.l_k
        self.sigma = ((1 / 0.95 - 1)
                      / (1 - 0.6227 * math.sqrt(2 * math.pi))) * self.b_k
        self.l_k_dash = l_k + 0.0566 * self.b_k
        self.u_k_dash = u_k - 0.0566 * self.b_k

        # How many points should be rendered for the line
        self.n_points = n_points
        # Show Graph in range "range" if the user provided a range or
        # with a MARGIN% margin on both sides
        self.margin = 0.5
        self.offset = round(self.b_k * self.margin, 2)
        self.range = r if r is not None \
            else (self.l_k - self.offset, self.u_k + self.offset)
        # Points to be rendered
        self.line = np.linspace(self.range[0], self.range[1], self.n_points)
        # Number of points used to estimate the area beneath the graphs
        self.a_points = a_points
        # Print the ratio of the estimated areas under the hard interval graph
        # and the soft interval graph
        self.print_ratio = print_ratio

    # Create and show plot
    def plot(self):
        if self.print_ratio:
            self.area_ratio()

        plt.style.use("seaborn-darkgrid")

        if self.show_hard:
            plt.plot(self.line, self.hard_interval(), color="blue",
                     label="hard interval")
        plt.plot(self.line, self.m_k(), color='red', label="soft interval")

        plt.title(f"Match probabilities for the classifier "
                  f"[{self.l_k}, {self.u_k}]")
        plt.xlabel("Inputs")
        plt.ylabel("Match probability")
        plt.legend()

        plt.show()

    # 1D soft interval
    def m_k(self):
        f = -(1 / (2 * self.sigma ** 2))

        return [math.exp(f * (x - self.l_k_dash) ** 2) if x < self.l_k_dash
                else math.exp(f * (x - self.u_k_dash) ** 2) if x > self.u_k_dash
        else 1 for x in self.line]

    # 1D hard interval
    def hard_interval(self):
        return [1 if self.l_k < x < self.u_k
                else np.finfo(None).tiny for x in self.line]

    def area_ratio(self):
        points = zip(np.random.random_sample((self.a_points,)),
                     np.random.random_sample((self.a_points,)))

        below_hard = 0
        below_soft = 0

        for point in points:
            hard = 1 if self.l_k < point[0] < self.u_k else np.finfo(None).tiny

            if hard >= point[1]:
                below_hard += 1

            f = -(1 / (2 * self.sigma ** 2))
            m_k = math.exp(f * (point[0] - self.l_k_dash) ** 2) \
                if point[0] < self.l_k_dash else \
                math.exp(f * (point[0] - self.u_k_dash) ** 2) \
                if point[0] > self.u_k_dash else 1

            if m_k >= point[1]:
                below_soft += 1

        print(f"Number of points below the hard interval: {below_hard} "
              f"out of {self.a_points} \n"
              f"Number of points below the soft interval: {below_soft} "
              f"out of {self.a_points} \n "
              f"Ratio of the estimated area hard / soft: "
              f"{below_hard / below_soft}")


if __name__ == "__main__":
    p = OneD(0.3, 0.4)
    p.plot()
