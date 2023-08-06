import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import copy

from kurvy import utils


def simple_plot(X_data, Y_data, test_data=None):
    fig, ax = plt.subplots(figsize=(12, 4))

    # train data
    ax.scatter(
        X_data,
        Y_data,
        color="white",
        edgecolors="teal",
        alpha=0.5,
        s=20,
        zorder=-1,
    )

    # test data
    if test_data is not None:
        ax.scatter(
            test_data[:, 0],
            test_data[:, 1],
            color="mediumturquoise",
            edgecolors="teal",
            alpha=0.8,
            s=20,
            zorder=1,
        )

    ax.grid(visible=True)
    ax.set_axisbelow(True)
    plt.show()


def pred_plot(model, X_data, Y_data, test_data=None):
    Y_pred = model.predict(X_data)
    mse = np.round(utils.calculate_loss(Y_data, Y_pred), 4)
    r2 = np.round(utils.calculate_r2(Y_data, Y_pred), 4)

    X_space = np.linspace(np.min(X_data), np.max(X_data), 300)
    Y_predspace = model.predict(X_space)

    fig, ax = plt.subplots(figsize=(12, 4))

    # estimator
    ax.plot(
        X_space,
        Y_predspace,
        color="cyan",
        linewidth=5,
        alpha=0.8,
        solid_capstyle="round",
        zorder=2,
    )

    # train data
    ax.scatter(
        X_data,
        Y_data,
        color="white",
        edgecolors="teal",
        alpha=0.5,
        s=20,
        zorder=-1,
    )

    # test data
    if test_data is not None:
        ax.scatter(
            test_data[:, 0],
            test_data[:, 1],
            color="mediumturquoise",
            edgecolors="teal",
            alpha=0.8,
            s=20,
            zorder=1,
        )

        Y_pred_test = model.predict(test_data[:, 0])
        test_mse = np.round(
            utils.calculate_loss(test_data[:, 1], Y_pred_test), 4
        )
        test_r2 = np.round(utils.calculate_r2(test_data[:, 1], Y_pred_test), 4)

        ax.set_title(
            f"Train Loss = {mse}  /  Train R2 = {r2}\nTest Loss = {test_mse}  /  Test R2 = {test_r2}"
        )

    else:
        ax.set_title(f"Loss = {mse}  /  tR2 = {r2}")

    ax.grid(visible=True)
    ax.set_axisbelow(True)
    plt.show()


def plot_training(model, metric):
    best_loss = model.training_history[model.best_epoch][0]
    best_r2 = model.training_history[model.best_epoch][1]
    epochs = range(model.training_history.shape[0])
    titles = ["Loss", "R-Squared"]

    if (metric == "loss") or (metric == "r2"):
        if metric == "loss":
            plot_data = model.training_history[:, 0]
            title = titles[0]
            best = model.training_history[model.best_epoch][0]
            color = "royalblue"
        else:
            plot_data = model.training_history[:, 0]
            title = titles[1]
            best = model.training_history[model.best_epoch][1]
            color = "crimson"

        plt.figure(figsize=(7, 4))
        plt.plot(
            epochs,
            plot_data,
            linewidth=4,
            alpha=0.8,
            solid_capstyle="round",
            color=color,
            zorder=-1,
        )

        plt.scatter(
            model.best_epoch, best, color="white", edgecolors=color, s=60
        )
        plt.title(title)
        plt.grid(visible=True)
        plt.show()

    elif metric == "both":
        best = [best_loss, best_r2]
        color = ["royalblue", "crimson"]

        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        for i in range(2):
            axs[i].plot(
                epochs,
                model.training_history[:, i],
                linewidth=4,
                alpha=0.8,
                solid_capstyle="round",
                color=color[i],
                zorder=-1,
            )
            axs[i].scatter(
                model.best_epoch,
                best[i],
                color="white",
                edgecolors=color[i],
                s=60,
            )
            axs[i].set_xlabel("Epochs")
            axs[i].set_title(titles[i])
            axs[i].grid(visible=True)
        plt.show()

    else:
        raise ValueError(f"Unkown metric: {metric}.")


def loss_vis(model, param_name, markers=False):
    if model.training_history is None:
        raise ValueError("No training history - model has not yet been fit.")

    if model.params[param_name]["trainable"]:
        best_overall_loss = model.best_epoch

        col = "abcde".find(param_name) + 2

        p_values = model.training_history[:, col]
        loss_values = model.training_history[:, 0]

        best_value_overall = p_values[model.best_epoch]
        best_loss_overall = loss_values[model.best_epoch]

        fig, ax = plt.subplots(figsize=(12, 4))

        ax.scatter(
            p_values[0],
            loss_values[0],
            color="white",
            edgecolors="royalblue",
            s=60,
        )
        if markers:
            ax.plot(
                p_values,
                loss_values,
                color="royalblue",
                zorder=-1,
                marker="o",
            )
        else:
            ax.plot(p_values, loss_values, color="royalblue", zorder=-1)

        ax.scatter(p_values[-1], loss_values[-1], color="royalblue", s=60)
        ax.scatter(
            best_value_overall,
            best_loss_overall,
            color="red",
            edgecolors="royalblue",
            s=60,
        )

        plt.show()

    else:
        raise ValueError(f"{param_name} is not a trainable parameter.")


def single_param_loss_vis(
    param_name,
    param_space,
    initial_params,
    X,
    Y,
    learning_rate=0.1,
    epochs=5,
    momentum=None,
    random_init=False,
    plot_all=False,
    seed=None,
):
    """
    Performs gradient descent on single parameter (keeping other parameters
    constant), and plots the parameter updates.

    Args:
    -----

        param_name (str): the chosen parameter to on which to perform gradient
        descent. Must be one of "a", "b", "c", "d", or "e".

        param_space (1-D array): value space for the chosen parameter.

        initial_params (dict): initial values for each of the parameters "a",
        "b", "c", "d", and "e" (dict keys). Note that only the chosen parameter
        will be updated; the others will be held constant.

        X (1-D array): input training data (features).

        Y (1-D array): output training data (values).

    Kwargs:
    -------

        learning_rate (float, default = 0.1): constant multiple for calculating
        parameter update step in each epoch, where:
            new param value = old param value - learning_rate * deriv

        epochs (int, default = 5): number of times to process entire dataset and
        update parameter values through gradient descent.

        momentum (float, default = None): if given, will apply gradient descent
        with momentum, taking into account prior gradients, where:
            new velocity = momentum * old velocity - learning_rate * deriv
            new param value = old param value + new velocity

        random_init (bool, default = False): if True, will initialize the chosen
        parameter value randomly. Otherwise, the initial value will be taken
        from the 'initial_params' arg.

        plot_all (bool, default = False): if True, will plot all of the parameter
        values computed during gradient descent.

        seed (int, default = None): sets random seed.

    Returns:
    --------

        Plot showing the parameter values computed through gradient descent,
        highlighting the initial and final values.
    """

    n = X.shape[0]
    params = copy.deepcopy(initial_params)

    if random_init:
        init_rng = np.random.default_rng(seed)
        initial_param_value = init_rng.choice(param_space)
    else:
        initial_param_value = initial_params[param_name]

    params[param_name] = initial_param_value

    def _fetch_params():
        a = params["a"]
        b = params["b"]
        c = params["c"]
        d = params["d"]
        e = params["e"]

        return a, b, c, d, e

    def _loss(a, b, c, d, e):
        cos_val = np.cos(2 * np.pi * X / b - c)
        Y_pred = a * cos_val + d + e * X
        sq_errors = [(i[0] - i[1]) ** 2 for i in np.dstack((Y, Y_pred))[0]]
        loss = np.sum(sq_errors) / n

        return loss

    def _get_loss_space(param_name, param_space):
        loss_space = []
        for i in param_space:
            a, b, c, d, e = _fetch_params()

            if param_name == "a":
                a = i
            elif param_name == "b":
                b = i
            elif param_name == "c":
                c = i
            elif param_name == "d":
                d = i
            elif param_name == "e":
                e = i

            loss = _loss(a, b, c, d, e)
            loss_space.append(loss)
        loss_space = np.array(loss_space)
        return loss_space

    def _get_deriv(param_name):
        a, b, c, d, e = _fetch_params()

        cos_val = np.cos(2 * np.pi * X / b - c)
        sin_val = np.sin(2 * np.pi * X / b - c)

        if param_name == "a":
            deriv = (1 / n) * np.sum(
                2 * cos_val * (a * cos_val + d + e * X - Y)
            )
        elif param_name == "b":
            deriv = (1 / n) * np.sum(
                (4 * np.pi * a * X * (a * cos_val + d + e * X - Y) * sin_val)
                / b**2
            )
        elif param_name == "c":
            deriv = (1 / n) * np.sum(
                2 * (a * cos_val + d + e * X - Y) * (a * sin_val)
            )
        elif param_name == "d":
            deriv = (1 / n) * np.sum(2 * (a * cos_val + d + e * X - Y))
        elif param_name == "e":
            deriv = (1 / n) * np.sum(2 * X * (a * cos_val + d + e * X - Y))
        else:
            deriv = 0

        return deriv

    p_values = [initial_param_value]
    a, b, c, d, e = _fetch_params()
    initial_loss = _loss(a, b, c, d, e)
    loss_values = [initial_loss]

    if momentum:
        v = 0

    for i in tqdm(range(1, epochs + 1)):
        deriv = _get_deriv(param_name)
        old_p = params[param_name]
        if momentum:
            v = momentum * v - learning_rate * deriv
            new_p = old_p + v
        else:
            new_p = old_p - learning_rate * deriv
        params[param_name] = new_p

        a, b, c, d, e = _fetch_params()
        loss = _loss(a, b, c, d, e)

        p_values.append(new_p)
        loss_values.append(loss)

    loss_space = _get_loss_space(param_name, param_space)
    param_combined = np.concatenate((param_space, p_values))
    loss_combined = np.concatenate((loss_space, loss_values))
    res_combined = np.dstack((param_combined, loss_combined))[0]
    res_combined = res_combined[np.argsort(res_combined[:, 0])]
    param_points = res_combined[:, 0]
    loss_points = res_combined[:, 1]

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.set_xlim(left=np.min(param_points), right=np.max(param_points))

    y_buffer = (np.max(loss_points) - np.min(loss_points)) * 0.1
    ax.set_ylim(
        bottom=np.min(loss_points) - y_buffer,
        top=np.max(loss_points) + y_buffer,
    )

    # plot full parameter / loss space
    ax.plot(
        param_points,
        loss_points,
        color="tomato",
        linewidth=3,
        solid_capstyle="round",
        zorder=0,
    )

    # plot all parameter / loss values
    if plot_all:
        res_points = zip(p_values, loss_values)

        for i, j in enumerate(res_points):
            x_j = j[0]
            y_j = j[1]
            ax.scatter(x_j, y_j, color="teal", zorder=1, s=30)

    # plot lines marking minimum loss values
    ax.plot(
        (np.min(param_points), p_values[-1]),
        (loss_values[-1], loss_values[-1]),
        color="steelblue",
        alpha=0.7,
        linestyle="--",
        zorder=-1,
    )

    ax.plot(
        (p_values[-1], p_values[-1]),
        (np.min(loss_points) - y_buffer, loss_values[-1]),
        color="steelblue",
        alpha=0.7,
        linestyle="--",
        zorder=-1,
    )

    # plot initial and final parameter / loss value
    ax.scatter(
        initial_param_value,
        initial_loss,
        color="white",
        edgecolors="tomato",
        zorder=2,
        s=60,
    )
    ax.scatter(p_values[-1], loss_values[-1], color="black", zorder=2, s=60)

    plt.show()
