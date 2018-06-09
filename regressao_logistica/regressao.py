import pandas
import matplotlib.pyplot as plt
import os
import sklearn
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

base_dir="../data/ETFs"
usecols=["Open", "High", "Low", "Close"]

def fill_missing_values(df):
    """Fill missing values in data frame, in place."""
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)


def get_data(etf_list):
    df_final = None
    for etf in etf_list:
        f = os.path.join(base_dir, etf+'.txt')
        df_temp = pandas.read_csv(f, parse_dates=True, index_col="Date", usecols=["Date"]+usecols, na_values=["nan"])
        for col in usecols:
            df_temp = df_temp.rename(columns={col: col+'_'+etf})
        if df_final is None:
            df_final = df_temp
        else:
            df_final = df_final.join(df_temp, how='outer')

    return df_final


def plot_data(df, dias):
    ax = df.plot(title="Variação percentual de preços (dias = {})".format(dias), fontsize=8)
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço")
    ax.legend().set_visible(False)
    plt.show(block=False)


def prepare_dataframe(base_etf, companion_etfs, pct_change_days):
    etf_list = [base_etf] + companion_etfs
    df = get_data(etf_list)
    fill_missing_values(df)

    for etf in etf_list:
        for dias in pct_change_days:
            for col in usecols:
                df['pctchange_{}_{}_{}'.format(col,dias,etf)] = df['{}_{}'.format(col,etf)].pct_change(dias)

    df['oraculo'] = df['Open_' + base_etf].shift(-1) > df['Open_' + base_etf]
    df.dropna(inplace=True)

    #print(df)
    #plot_data(df['pctchange'], dias)

    return df


def do_logistic_regression(base_etf, df):
    train_data = df.sample(frac=0.8, random_state=0)
    test_data = df.drop(train_data.index)

    x_train = train_data.filter(regex='^pctchange_.*')
    y_train = train_data['oraculo']
    x_test = test_data.filter(regex='^pctchange_.*')
    y_test = test_data['oraculo']

    if x_train.shape[1] == 1:
        #reshape porque o sklearn chia quando só tem uma feature
        x_train = x_train.values.reshape(-1,1)
        x_test = x_test.values.reshape(-1,1)
    classifier = LogisticRegression()
    classifier.fit(x_train, y_train)
    predicted = classifier.predict(x_test)
    probs = classifier.predict_proba(x_test)
    print('accuracy:', metrics.accuracy_score(y_test, predicted))
    print('precision:', metrics.precision_score(y_test, predicted))
    print('recall:', metrics.recall_score(y_test, predicted))
    print('f1:', metrics.f1_score(y_test, predicted))


def test_run():
    base_etf = 'spy.us'
    companion_etfs = []
    df = prepare_dataframe(base_etf, companion_etfs, range(1,5))
    do_logistic_regression(base_etf, df)


if __name__ == "__main__":
    test_run()
    plt.show();
