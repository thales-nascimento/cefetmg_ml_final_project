import pandas
import matplotlib.pyplot as plt
import os

base_dir="../data/ETFs"

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)


def get_data(file_list, dates):
    df_final = pandas.DataFrame(index=dates)

    for file in file_list:
        etf_name = file[0:file.rfind('.')]
        file = os.path.join(base_dir, file)
        df_temp = pandas.read_csv(file, parse_dates=True, index_col="Date", usecols=["Date", "Open"], na_values=["nan"])
        df_temp = df_temp.rename(columns={"Open": etf_name})
        df_final = df_final.join(df_temp)

    return df_final


def plot_data(df_data):
    """Plot stock data with appropriate axis labels."""
    ax = df_data.plot(title="Preço de 189 ETFs desde 2005", fontsize=8)
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço")
    ax.legend().set_visible(False)
    plt.show()


def test_run():
    path_list = os.listdir(base_dir)  # list of symbols
    start_date = "2005-01-04"
    end_date = "2017-11-10"
    dates = pandas.date_range(start_date, end_date)  # date range as index
    df_data = get_data(path_list, dates)  # get data for each symbol

    # Fill missing values
    fill_missing_values(df_data)

    # Compute correlation
    corr = df_data.corr()
    print(corr)

    # Plot
    plot_data(df_data)


if __name__ == "__main__":
    test_run()
