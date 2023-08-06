import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import copy

from kurvy import utils


def make_trig_data(X_range, n_samples, params=None, fuzz=None, seed=None):
    rng = np.random.default_rng(seed)

    if not isinstance(X_range, tuple):
        raise ValueError(
            f"Expected 2-tuple for 'X_range'; got {type(X_range)}."
        )
    if not all([isinstance(i, int) for i in X_range]):
        raise ValueError(f"'X_range' must be tuple of integers: (min, max).")
    if not isinstance(n_samples, int):
        raise ValueError(
            f"Expected integer for 'n_samples'; got {type(n_samples)}."
        )
    if fuzz:
        if not isinstance(fuzz, int) or (not 0 <= fuzz <= 3):
            raise ValueError(f"'fuzz' must be integer in [0,3].")
    if params:
        if not isinstance(params, tuple):
            raise ValueError(
                f"Expected 5-tuple for 'params'; got {type(params)}."
            )
        if len(params) != 5:
            raise ValueError(
                f"Expected 5-tuple for 'params'; got {len(params)}-tuple."
            )

        a, b, c, d, e = params

    else:
        mu = np.mean(X_range)
        std = mu * 0.5

        a = np.round(rng.normal(mu, std), 3)
        b = np.round(
            rng.integers(np.floor(X_range[1] * 0.75)) + rng.random(), 3
        )
        c = np.round(rng.integers(np.floor(b)) + rng.random(), 3)
        d = np.round(rng.integers(np.floor(X_range[1] * 2)) + rng.random(), 3)
        e = np.round(rng.uniform(-10, 10), 3)

    X = np.linspace(X_range[0], X_range[1], n_samples)

    cos_val = np.cos(2 * np.pi * X / b - c)
    Y = a * cos_val + d + e * X

    if fuzz == 1:
        Y_fuzzy = utils.add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)

    elif fuzz == 2:
        Y_fuzzy = utils.add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)
        Y_fuzzy = utils.add_fuzz(Y_fuzzy, 0.3, 0, X_range[1] * 0.075, seed=seed)

    elif fuzz == 3:
        Y_fuzzy = utils.add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)
        Y_fuzzy = utils.add_fuzz(Y_fuzzy, 0.3, 0, X_range[1] * 0.075, seed=seed)
        Y_fuzzy = utils.add_fuzz(Y_fuzzy, 0.05, 0, X_range[1] * 0.3, seed=seed)

    else:
        Y_fuzzy = Y

    return (a, b, c, d, e), X, Y_fuzzy


class ParamEstimator:
    def __init__(self):
        """
        NOTE: X and Y data must be sorted for this to work.
        """

    def _period_estimation(self, X_data, Y_data, Y_reg, window_size):
        window = window_size
        window_start = 0

        Y_window = Y_data[0:window]
        Y_reg_window = Y_reg[0:window]
        self.start_sign = np.sign(np.mean(Y_window - Y_reg_window))
        start_sign = self.start_sign

        Y_window_n = Y_data[window_start:window]
        Y_reg_window_n = Y_reg[window_start:window]
        window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))

        while window_sign == start_sign:
            window += 1
            window_start += 1
            Y_window_n = Y_data[window_start:window]
            Y_reg_window_n = Y_reg[window_start:window]
            window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        p1 = int(np.mean((window_start, window)))

        start_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        while window_sign == start_sign:
            window += 1
            window_start += 1
            Y_window_n = Y_data[window_start:window]
            Y_reg_window_n = Y_reg[window_start:window]
            window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        p2 = int(np.mean((window_start, window)))

        start_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        while window_sign == start_sign:
            window += 1
            window_start += 1
            Y_window_n = Y_data[window_start:window]
            Y_reg_window_n = Y_reg[window_start:window]
            window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        p3 = int(np.mean((window_start, window)))

        return p1, p2, p3

    def fit(self, X_data, Y_data, window_size=100, sort_data=False):
        if sort_data:
            XY_data = np.dstack((X_data, Y_data))[0]
            self.X_data = XY_data[np.argsort(XY_data[:, 0])][:, 0]
            self.Y_data = XY_data[np.argsort(XY_data[:, 0])][:, 1]

        else:
            self.X_data = X_data
            self.Y_data = Y_data

        # compute regression line for X points
        self.trend, self.offset = utils.lin_reg(self.X_data, self.Y_data)
        self.Y_reg = self.X_data * self.trend + self.offset

        self.p0 = (self.X_data[0], self.Y_reg[0])

        p1, p2, p3 = self._period_estimation(
            self.X_data, self.Y_data, self.Y_reg, window_size
        )

        self.p1 = (self.X_data[p1], self.X_data[p1] * self.trend + self.offset)
        self.p2 = (self.X_data[p2], self.X_data[p2] * self.trend + self.offset)
        self.p3 = (self.X_data[p3], self.X_data[p3] * self.trend + self.offset)

        self.period = self.X_data[p3] - self.X_data[p1]
        self.q_dist = self.period / 4

        # find first peak
        # (assumed to be a quarter of the period back from p1)
        # first peak cast onto regression line
        if self.p1[0] - self.q_dist < 0:
            self.peak_0_reg = (
                self.p1[0] - self.q_dist + self.period,
                (self.p1[0] - self.q_dist + self.period) * self.trend
                + self.offset,
            )
        else:
            self.peak_0_reg = (
                self.p1[0] - self.q_dist,
                (self.p1[0] - self.q_dist) * self.trend + self.offset,
            )

        # find nearest value in X data to computed first peak
        nearest_idx = np.argmin(np.abs(self.X_data - self.peak_0_reg[0]))

        # find coords on regression line for nearest value
        X_peakval = self.X_data[nearest_idx]
        Y_reg_peakval = X_peakval * self.trend + self.offset

        # find coords in Y data for nearest value
        # use mean abs value of points either side to exlcude fuzz
        Y_peakval = np.mean(
            [np.abs(self.Y_data[nearest_idx + i]) for i in range(-5, 5)]
        )

        # set coords value to nearest value
        self.peak_0_reg = (X_peakval, Y_reg_peakval)
        self.peak_0 = (X_peakval, Y_peakval)

        # set amplitude sign based on first section of curve
        abs_amplitude = np.abs(Y_peakval - Y_reg_peakval)
        self.amplitude = abs_amplitude * self.start_sign

        # estimate Y with no phase shift keeping other params fixed
        est_cos_val_c0 = np.cos(2 * np.pi * self.X_data / self.period - 0)
        Y_est_c0 = (
            self.amplitude * est_cos_val_c0
            + self.offset
            + self.trend * self.X_data
        )

        # use smaller window size
        c0_window = int(window_size / 2)
        p1_c0, p2_c0, p3_c0 = self._period_estimation(
            self.X_data, Y_est_c0, self.Y_reg, window_size=c0_window
        )

        mean_shift = np.mean(
            [
                self.X_data[p1] - self.X_data[p1_c0],
                self.X_data[p3] - self.X_data[p3_c0],
            ]
        )

        self.phase_shift = mean_shift / self.period * 2 * np.pi

    def plot(self):
        fig, ax = plt.subplots(figsize=(12, 4))

        # (sorted) raw data
        ax.scatter(
            self.X_data,
            self.Y_data,
            color="white",
            edgecolors="teal",
            alpha=0.5,
            s=20,
            zorder=-1,
        )

        # regression line
        ax.plot(
            (self.X_data[0], self.X_data[-1]),
            (self.Y_reg[0], self.Y_reg[-1]),
            color="dodgerblue",
            linewidth=3,
            alpha=0.7,
            solid_capstyle="round",
            zorder=1,
        )

        # points of interest
        ax.scatter(
            *self.p1,
            color="white",
            edgecolors="tomato",
            s=60,
            linewidth=2,
            zorder=4,
        )
        ax.scatter(
            *self.p3,
            color="white",
            edgecolors="tomato",
            s=60,
            linewidth=2,
            zorder=4,
        )
        ax.scatter(
            *self.peak_0,
            color="white",
            edgecolors="teal",
            s=60,
            linewidth=2,
            zorder=4,
        )
        ax.scatter(
            *self.peak_0_reg,
            color="white",
            edgecolors="dodgerblue",
            s=60,
            linewidth=2,
            zorder=4,
        )

        # vertical period lines
        ax.axvline(
            x=self.p1[0], color="tomato", alpha=0.9, linestyle="--", zorder=2
        )
        ax.axvline(
            x=self.p3[0], color="tomato", alpha=0.9, linestyle="--", zorder=2
        )

        # regression line trace in period
        ax.plot(
            (self.p1[0], self.p3[0]),
            (self.p1[1], self.p3[1]),
            color="white",
            alpha=1,
            linestyle="--",
            zorder=1,
        )

        # vertical amplitude line
        ax.plot(
            (self.peak_0[0], self.peak_0[0]),
            (self.peak_0_reg[1], self.peak_0[1]),
            color="black",
            linestyle="dotted",
            zorder=3,
        )

        # estimator
        est_cos_val = np.cos(
            2 * np.pi * self.X_data / self.period - self.phase_shift
        )
        Y_est = (
            self.amplitude * est_cos_val
            + self.offset
            + self.trend * self.X_data
        )
        ax.plot(
            self.X_data,
            Y_est,
            color="cyan",
            linewidth=5,
            alpha=0.8,
            solid_capstyle="round",
            zorder=1,
        )

        ax.grid(visible=True)
        ax.set_axisbelow(True)
        plt.show()


class TrigModel:
    def __init__(
        self, initial_params=None, initializer=None, smart_init=False, seed=None
    ):
        if initial_params is None:
            initial_params = {
                "a": {"value": None, "trainable": True},
                "b": {"value": None, "trainable": True},
                "c": {"value": None, "trainable": True},
                "d": {"value": None, "trainable": True},
                "e": {"value": None, "trainable": True},
            }

        init_rng = np.random.default_rng(seed)

        if initializer is not None:
            random_init = initializer
        else:
            random_init = init_rng.uniform(-1, 1, size=5)

        for i, (k, v) in enumerate(initial_params.items()):
            if v["value"] is None:
                v["value"] = random_init[i]

        self.smart = False
        if smart_init:
            self.smart = True

        self.initial_params = copy.deepcopy(initial_params)
        self.params = copy.deepcopy(initial_params)
        self.training_history = None

    def predict(self, x):
        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]

        cos_val = np.cos(2 * np.pi * x / b - c)
        pred = a * cos_val + d + e * x

        return pred

    def dL_da(self, X, Y):
        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        dL_da = (1 / n) * np.sum(2 * cos_val * (a * cos_val + d + e * X - Y))
        return dL_da

    def dL_db(self, X, Y):
        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        sin_val = np.sin(2 * np.pi * X / b - c)
        dL_db = (1 / n) * np.sum(
            (4 * np.pi * a * X * (a * cos_val + d + e * X - Y) * sin_val)
            / b**2
        )
        return dL_db

    def dL_dc(self, X, Y):
        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        sin_val = np.sin(2 * np.pi * X / b - c)
        dL_dc = (1 / n) * np.sum(
            2 * (a * cos_val + d + e * X - Y) * (a * sin_val)
        )
        return dL_dc

    def dL_dd(self, X, Y):
        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        dL_dd = (1 / n) * np.sum(2 * (a * cos_val + d + e * X - Y))
        return dL_dd

    def dL_de(self, X, Y):
        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        dL_de = (1 / n) * np.sum(2 * X * (a * cos_val + d + e * X - Y))
        return dL_de

    def compile_diff_funcs(self):
        diff_funcs = [
            ("a", self.dL_da),
            ("b", self.dL_db),
            ("c", self.dL_dc),
            ("d", self.dL_dd),
            ("e", self.dL_de),
        ]

        trainable_params = {
            k: v["value"]
            for k, v in self.params.items()
            if self.params[k]["trainable"]
        }
        diff_funcs = [f for f in diff_funcs if f[0] in trainable_params.keys()]

        return diff_funcs

    def fit(
        self,
        X,
        Y,
        epochs=5,
        learning_rate=0.1,
        momentum=None,
        lambda_2=None,
        window_size=None,
        save_best=False,
    ):
        if self.smart == True:
            if window_size is None:
                raise ValueError(
                    "Must provide value for 'window_size' if using smart inititalization."
                )
            else:
                pe = ParamEstimator()
                pe.fit(X, Y, window_size=window_size, sort_data=True)
                self.params["a"]["value"] = pe.amplitude
                self.params["b"]["value"] = pe.period
                self.params["c"]["value"] = pe.phase_shift
                self.params["d"]["value"] = pe.offset
                self.params["e"]["value"] = pe.trend

        Y_pred = self.predict(X)
        mse = utils.calculate_loss(Y_pred, Y)
        r2 = utils.calculate_r2(Y, Y_pred)

        training_history = np.array(
            [
                mse,
                r2,
                self.params["a"]["value"],
                self.params["b"]["value"],
                self.params["c"]["value"],
                self.params["d"]["value"],
                self.params["e"]["value"],
            ]
        )

        if self.training_history is None:
            self.training_history = training_history

        print(f"Initial Loss: {mse}")

        self.diff_funcs = self.compile_diff_funcs()
        if momentum:
            v = np.zeros(len(self.diff_funcs))

        if lambda_2:
            if not all([self.params[k]["trainable"] for k in lambda_2.keys()]):
                raise ValueError(
                    "Can only use L2 regularization on trainable params."
                )

        for epoch in tqdm(range(1, epochs + 1)):
            res = np.array(training_history)

            for i, f in enumerate(self.diff_funcs):
                param_name = f[0]
                p = self.__dict__["params"][param_name]["value"]

                dL_dp = f[1]
                dp = dL_dp(X, Y)

                if lambda_2:
                    if param_name in lambda_2.keys():
                        l2_reg = lambda_2[param_name]
                        if momentum:
                            v[i] = momentum * v[i] - learning_rate * dp
                            update = v[i] - learning_rate * l2_reg * p
                        else:
                            update = (
                                -learning_rate * dp - learning_rate * l2_reg * p
                            )
                    else:
                        if momentum:
                            v[i] = momentum * v[i] - learning_rate * dp
                            update = v[i]
                else:
                    if momentum:
                        v[i] = momentum * v[i] - learning_rate * dp
                        update = v[i]
                    else:
                        update = -learning_rate * dp

                p = p + update

                self.__dict__["params"][param_name]["value"] = p

                res[i + 2] = p

            Y_pred = self.predict(X)

            mse = utils.calculate_loss(Y_pred, Y)
            res[0] = mse

            r2 = utils.calculate_r2(Y, Y_pred)
            res[1] = r2

            self.training_history = np.vstack((self.training_history, res))

        print(f"Final Loss: {mse}")

        self.best_epoch = self.training_history.argmin(axis=0)[0]

        self.best_params = self.training_history[self.best_epoch][2:]

        if save_best:
            self.params["a"]["value"] = self.best_params[0]
            self.params["b"]["value"] = self.best_params[1]
            self.params["c"]["value"] = self.best_params[2]
            self.params["d"]["value"] = self.best_params[3]
            self.params["e"]["value"] = self.best_params[4]
