import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


def plot_control_chart(
    UCL,
    CL,
    LCL,
    samples,
    ax,
    calibration_samples=None,
    title="",
    ylabel="",
    fill_alpha=0.07,
    restrict_zero=True,
):
    """
    Plots a control_card. Draws either on an existing axis (ax) or creates a new figure.
    """
    if restrict_zero:
        if LCL < 0:
            LCL = 0

    if calibration_samples is not None:
        x_min = -len(calibration_samples)
    else:
        x_min = 0

    # Draw control limits
    ax.hlines([UCL, CL, LCL], x_min, len(samples) - 1, colors=["black"], alpha=0.8)
    area_height = (UCL - CL) / 3
    ax.hlines(
        [CL + area_height, CL + 2 * area_height, CL - area_height, CL - 2 * area_height],
        x_min,
        len(samples) - 1,
        colors=["black"],
        alpha=0.3,
        linestyles="dashed",
    )

    # Add some coloring for the areas
    width = (x_min, len(samples) - 1)
    ax.fill_between(width, CL - area_height, CL + area_height, alpha=fill_alpha, color="green")
    ax.fill_between(width, CL + area_height, CL + 2 * area_height, alpha=fill_alpha, color="yellow")
    ax.fill_between(width, CL - area_height, CL - 2 * area_height, alpha=fill_alpha, color="yellow")
    ax.fill_between(width, CL + 2 * area_height, UCL, alpha=fill_alpha, color="red")
    ax.fill_between(width, CL - 2 * area_height, LCL, alpha=fill_alpha, color="red")

    # Plot setup
    ax.set_title(title)
    ax.set_xlabel("Sample")
    ax.set_ylabel(ylabel)
    ax.grid()

    return ax


def shewhart_card(
    UCL,
    CL,
    LCL,
    samples,
    calibration_samples=None,
    title="",
    ylabel="",
    fill_alpha=0.07,
    restrict_zero=True,
    ax=None,
):
    """
    Plots a shewhart_card. Draws either on an existing axis (ax) or creates a new figure.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = None

    ax = plot_control_chart(
        UCL, CL, LCL, samples, ax, calibration_samples, title, ylabel, fill_alpha, restrict_zero
    )

    # Plot points
    if calibration_samples is not None:
        ax.vlines(0, ymin=LCL, ymax=UCL, colors=["red"], linestyles="dotted", alpha=0.6)
        ax.plot(range(-len(calibration_samples), 0, 1), calibration_samples, "o-")
    ax.plot(range(len(samples)), samples, "o-")

    return fig if fig else ax


def ewma_card(
    UCL,
    CL,
    LCL,
    samples,
    ewma_line,
    lambda_,
    calibration_samples=None,
    calibration_ewma_line=None,
    title="EWMA-Karte",
    ylabel="",
    fill_alpha=0.07,
    restrict_zero=True,
    ax=None,
):
    """
    Plots a ewma_card. Draws either on an existing axis (ax) or creates a new figure.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = None

    ax = plot_control_chart(
        UCL, CL, LCL, samples, ax, calibration_samples, title, ylabel, fill_alpha, restrict_zero
    )

    # Plot points
    if calibration_samples is not None:
        ax.vlines(0, ymin=LCL, ymax=UCL, colors=["red"], linestyles="dotted", alpha=0.6)
        ax.plot(
            range(-len(calibration_samples), 0, 1),
            calibration_samples,
            "o",
            color="black",
            alpha=0.2,
        )
        ax.plot(range(-len(calibration_samples), 0, 1), calibration_ewma_line, linewidth=1.5)

    ax.plot(range(len(samples)), samples, "o", color="black", alpha=0.2)
    ax.plot(range(len(ewma_line)), ewma_line, linewidth=1.5, label=f"EWMA (λ={lambda_})")

    return fig if fig else ax


def plot_histogram_normal(
    data,
    bins=20,
    title="Histogram with Normal Distribution Overlay",
    xlabel="Data",
    ylabel="Density",
    alpha=0.6,
    color="blue",
    fill_color="red",
    grid_alpha=0.4,
    ax=None,
):
    """
    Plots a histogram of the data with an overlay of a fitted normal distribution.
    Draws either on an existing axis (ax) or creates a new figure.

    Args:
        data (np.ndarray): A 1D array of numerical data to be plotted.
        bins (int): Number of bins for the histogram.
        alpha (float): Transparency for the histogram bars.
        color (str): Color for the histogram bars.
        fill_color (str): Color for the normal distribution line.
        grid_alpha (float): Transparency for the grid lines.
        ax (matplotlib.axes.Axes, optional): Existing axes to draw on.

    Returns:
        matplotlib.figure.Figure or matplotlib.axes.Axes: The figure or axes object.
    """
    mu = data.mean()
    sigma = data.std(ddof=1)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = None

    # Plot histogram
    ax.hist(data, bins=bins, density=True, alpha=alpha, color=color, label="Data")

    # Plot normal distribution
    ax.plot(x, st.norm.pdf(x, loc=mu, scale=sigma), color=fill_color, label="Normal PDF")

    # Customize plot
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=grid_alpha)
    ax.legend()

    return fig if fig else ax


def plot_qq_plot(
    data,
    title="QQ-Plot",
    xlabel="Theoretical Quantiles",
    ylabel="Sample Quantiles",
    grid_alpha=0.4,
    ax=None,
):
    """
    Plots a QQ-Plot to check for normality.
    Draws either on an existing axis (ax) or creates a new figure.

    Args:
          data (np.ndarray): A 1D array of numerical data to be plotted.
        grid_alpha (float): Transparency for the grid lines.
        ax (matplotlib.axes.Axes, optional): Existing axes to draw on.

    Returns:
        matplotlib.figure.Figure or matplotlib.axes.Axes: The figure or axes object.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = None

    # Generate QQ-Plot
    st.probplot(data, dist="norm", plot=ax)

    # Customize plot
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=grid_alpha)

    return fig if fig else ax
