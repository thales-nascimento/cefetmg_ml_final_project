import matplotlib.pyplot as plt


def plot_data(df, dias):
    ax = df.plot(title="Variação percentual de preços (dias = {})".format(dias), fontsize=8)
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço")
    ax.legend().set_visible(False)
    plt.show(block=False)
