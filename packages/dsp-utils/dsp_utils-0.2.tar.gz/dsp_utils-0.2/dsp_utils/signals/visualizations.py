from dataclasses import dataclass
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy.fftpack import fft, fftshift, fftfreq
from scipy.fftpack import rfft, rfftfreq
from matplotlib import pyplot as plt
import numpy as np


########################################################################
@dataclass
class Visualizer:
    figsize: tuple = (16, 7)
    dpi: int = 100
    grid: bool = True

    ## ----------------------------------------------------------------------
    # def __post_init__(self):
    # plt.rcParams["figure.figsize"] = self.figsize
    # plt.rcParams["figure.dpi"] = self.dpi

    # ----------------------------------------------------------------------
    def plot_signal(
        self,
        signal,
        *,
        ax=None,
        fn='plot',
        time=None,
        title=None,
        xlabel=None,
        ylabel=None,
        labels=None,
        **kwargs,
    ):
        """"""

        if ax is None:
            plt.figure(figsize=self.figsize, dpi=self.dpi)
            ax = plt.subplot(111)

        fn_plot = getattr(ax, fn)

        if title:
            plt.title(title)

        if not time is None:
            if signal.ndim == 2:
                [fn_plot(time, s, **kwargs) for s in signal]
            else:
                fn_plot(time, signal, **kwargs)
        else:
            if signal.ndim == 2:
                [fn_plot(s, **kwargs) for s in signal]
            else:
                fn_plot(signal, **kwargs)

        if xlabel:
            ax.set_xlabel(xlabel)

        if ylabel:
            ax.set_ylabel(ylabel)

        if labels:
            ax.legend(labels)

        ax.grid(self.grid)
        # plt.show()

    # ----------------------------------------------------------------------
    def plot_kde(
        self,
        signal,
        *,
        fn='plot',
        time=None,
        title=None,
        xlabel=None,
        ylabel=None,
        labels=None,
    ):
        """"""

        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        gs = GridSpec(1, 2, width_ratios=[3, 1])

        ax1 = fig.add_subplot(gs[0])
        self.plot_signal(
            signal,
            ax=ax1,
            fn=fn,
            time=time,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            labels=labels,
        )

        ax2 = fig.add_subplot(gs[1], sharey=ax1)
        ax2.grid(self.grid)
        sns.kdeplot(y=signal, ax=ax2, bw_adjust=0.5, label="Curva de Densidad")
        # ax2.yaxis.set_ticks([])

        plt.subplots_adjust(wspace=0.07)

    # ----------------------------------------------------------------------
    def plot_dsp(
        self,
        signal,
        *,
        ax=None,
        fn='plot',
        ffn='fill_between',
        time=None,
        title=None,
        xlabel=None,
        ylabel=None,
        labels=None,
        band=None,
        sample_rate=1,
        **kwargs,
    ):
        """"""
        if ax is None:
            plt.figure(figsize=self.figsize, dpi=self.dpi)
            ax1 = plt.subplot(121)
            ax2 = plt.subplot(122)
        else:
            ax1, ax2 = ax

        fn_plot = getattr(ax1, fn)

        if title:
            plt.title(title)

        if not time is None:
            if signal.ndim == 2:
                [fn_plot(time, s, **kwargs) for s in signal]
            else:
                fn_plot(time, signal, **kwargs)
        else:
            if signal.ndim == 2:
                [fn_plot(s, **kwargs) for s in signal]
            else:
                fn_plot(signal, **kwargs)

        if xlabel:
            ax1.set_xlabel(xlabel)

        if ylabel:
            ax1.set_ylabel(ylabel)

        if labels:
            ax1.legend(labels)

        ax1.grid(self.grid)

        # X = np.abs(fft(signal))
        # X = fftshift(X)
        # W = fftshift(fftfreq(len(X), 1 / sample_rate))

        X = np.abs(rfft(signal))
        W = rfftfreq(len(X), 1 / sample_rate)

        if ffn == 'plot':
            ax2.plot(W, X)
        elif ffn == 'vlines':
            ax2.vlines(W, 0, X, zorder=10)
        elif ffn == 'fill_between':
            ax2.fill_between(W, 0, X, zorder=10)

        if band:
            ax2.set_xlim(*band)

        ax2.grid(self.grid, zorder=-99)
