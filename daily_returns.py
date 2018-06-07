import pandas
import matplotlib.pyplot as plt



def plot_data(df, legend=[], title="Stock prices", xlabel="Date", ylabel="Price"):
    ax = df.plot(title=title)
    ax.legend(legend, loc='upper left')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()



ibm_df = pandas.read_csv('data/Stocks/ibm.us.txt', index_col='Date', parse_dates=True, usecols=['Date', 'Open'])

daily_returns = ibm_df.pct_change(1).fillna(0);
daily_returns['rmean'] = pandas.Series.rolling(daily_returns, 20).mean();
plot_data(daily_returns, ['Daily returns', 'Rolling mean'], "Daily returns");
