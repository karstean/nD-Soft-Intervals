import math
import numpy as np
import matplotlib.pyplot as plt


class OneD:
    def __init__(self, l_k, u_k, n_points=100, range=(0, 1), show_hard=False):
        self.l_k = l_k  # Lower bound
        self.u_k = u_k  # Upper bound

        self.n_points = n_points    # How many points should be rendered for the line
        self.range = range          # Show Graph in range

        self.show_hard = show_hard  # Show what a hard interval would look like in this case

        # Various help variables for soft interval calculation
        self.b_k = self.u_k - self.l_k
        self.sigma = ((1 / 0.95 - 1) / (1 - 0.6227 * math.sqrt(2 * math.pi))) * self.b_k
        self.l_k_dash = l_k + 0.0566 * self.b_k
        self.u_k_dash = u_k - 0.0566 * self.b_k

        # Points to be rendered
        self.line = np.linspace(self.range[0], self.range[1], self.n_points)

    # Create and show plot
    def plot(self):
        plt.style.use("seaborn-darkgrid")

        if self.show_hard:
            plt.plot(self.line, self.hard_interval(), color='blue', label="hard interval")
        plt.plot(self.line, self.m_k(), color='red', label="soft interval")

        plt.title(f"Match probabilities for the classifier [{self.l_k}, {self.u_k}] "
                  f"in range [{self.range[0]}, {self.range[1]}]")
        plt.xlabel('Inputs')
        plt.ylabel('Match probability')
        plt.legend()

        plt.show()

    # 1D soft interval
    def m_k(self):
        res = []

        for x in self.line:
            if x < self.l_k_dash:
                res.append(math.exp(-(1 / (2 * self.sigma ** 2)) * (x - self.l_k_dash) ** 2))
            elif x > self.u_k_dash:
                res.append(math.exp(-(1 / (2 * self.sigma ** 2)) * (x - self.u_k_dash) ** 2))
            else:
                res.append(1)

        return res

    # 1D hard interval
    def hard_interval(self):
        res = []

        for x in self.line:
            res.append(1 if self.l_k < x < self.u_k else 0)

        return res


if __name__ == "__main__":
    p = OneD(0.2, 0.4)
    p.plot()