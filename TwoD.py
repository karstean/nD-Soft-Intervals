import numpy as np
import matplotlib.pyplot as plt


class TwoD:
    def __init__(self, l_k_1, u_k_1, l_k_2, u_k_2, n_points=100, r=None,
                 show_hard=True):
        self.l_k_1 = l_k_1  # First lower bound
        self.u_k_1 = u_k_1  # First upper bound

        self.l_k_2 = l_k_2  # Second lower bound
        self.u_k_2 = u_k_2  # Second upper bound

        # Show what a hard interval would look like in this case
        self.show_hard = True

        # Various help variables for soft interval calculation
        self.b_k_1 = self.u_k_1 - self.l_k_1
        self.b_k_2 = self.u_k_2 - self.l_k_2
        #
        # self.sigma = ((1 / 0.95 - 1) / (1 - 0.6227 * math.sqrt(2 * math.pi))) \
        #              * self.b_k
        #
        # self.l_k_1_dash = l_k_1 + 0.0566 * self.b_k_1
        # self.u_k_2_dash = u_k_1 - 0.0566 * self.b_k_1
        #
        # self.l_k_1_dash = l_k_2 + 0.0566 * self.b_k_2
        # self.u_k_2_dash = u_k_2 - 0.0566 * self.b_k_2

        # How many points should be rendered for the line
        self.n_points = n_points
        # Show Graph in range "range" if the user provided a range or with a
        # MARGIN% margin on both sides
        self.range = r
        if self.range is not None:
            self.x = np.linspace(self.range[0], self.range[1], self.n_points)
            self.y = np.linspace(self.range[0], self.range[1], self.n_points)
        else:
            # TODO: Use the biggest interval for both instead?
            self.margin = 0.5
            self.offset_1 = round(self.b_k_1 * self.margin, 2)
            self.offset_2 = round(self.b_k_2 * self.margin, 2)
            self.x = np.linspace(self.l_k_1 - self.offset_1,
                                 self.u_k_1 + self.offset_1, self.n_points)
            self.y = np.linspace(self.l_k_2 - self.offset_2,
                                 self.u_k_2 + self.offset_2, self.n_points)

        # Points to be rendered
        self.X, self.Y = np.meshgrid(self.x, self.y)

    # Create and show plot
    def plot(self):
        plt.style.use("seaborn-darkgrid")

        ax = plt.axes(projection="3d")

        if self.show_hard:
            surf = ax.plot_surface(self.X, self.Y, self.hard_interval(),
                                   color="b", label="hard interval")
        # surf = ax.plot_surface(self.X, self.Y, self.m_k(),
        #                        label="soft interval")

        plt.title(f"Match probabilities for the classifier "
                  f"[{self.l_k_1}, {self.u_k_1}, {self.l_k_2}, {self.u_k_2}]")
        ax.set_xlabel("Inputs x")
        ax.set_ylabel("Inputs y")
        ax.set_zlabel("Match probability")

        # Legend doesn't work otherwise
        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d
        plt.legend()

        plt.show()

    # 2D soft interval
    def m_k(self):
        pass

    # 2D hard interval
    def hard_interval(self):
        res = np.zeros((self.n_points, self.n_points))
        for i, x in enumerate(self.x):
            for j, y in enumerate(self.y):
                res[i, j] = 1. if (self.l_k_1 < x < self.u_k_1 and
                                   self.l_k_2 < y < self.u_k_2) else 0.
        return res


if __name__ == "__main__":
    p = TwoD(0.2, 0.4, 0.3, 0.6)
    p.plot()
