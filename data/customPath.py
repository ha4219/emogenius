import os
import datetime
import matplotlib.pyplot as plt


def _get_path_name(model: str, des: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    return f'{now}_{model}_{des}'


def _mkdir_path(path: str):
    if os.path.isdir(path):
        return
    os.mkdir(path)
    return


def _plot_acc(path: str, training_acc: list, validation_acc: list = None,
              show: bool = True, save: bool = True):
    title = f'{path}_acc'
    plt.figure(1)
    lm = max(training_acc)
    l = len(training_acc)
    plt.plot(range(l), training_acc, label='train')
    if validation_acc:
        lm = max(max(validation_acc), lm)
        plt.plot(range(l), validation_acc, label='val')
    plt.title(title)
    # plt.ylim((0, lm))
    plt.legend()
    if save:
        plt.savefig(f'{path}/acc_plot.png')
    if show:
        plt.show()
    return


def _plot_loss(path: str, training_loss: list, validation_loss: list = None,
               show: bool = True, save: bool = True):
    title = f'{path}_loss'
    plt.figure(2)
    lm = max(training_loss)
    l = len(training_loss)
    plt.plot(range(l), training_loss, label='train')
    if validation_loss:
        lm = max(max(validation_loss), lm)
        plt.plot(range(l), validation_loss, label='val')
    plt.title(title)
    # plt.ylim((0, lm))
    plt.legend()
    if save:
        plt.savefig(f'{path}/loss_plot.png')
    if show:
        plt.show()
    return
