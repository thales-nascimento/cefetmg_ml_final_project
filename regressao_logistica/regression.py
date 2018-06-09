import pandas
import os
import sklearn
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

base_dir="../data/ETFs"
usecols=["Open", "High", "Low", "Close"]


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

    df_final.fillna(method='ffill', inplace=True)
    df_final.fillna(method='bfill', inplace=True)
    return df_final


def prepare_dataframe(base_etf, companion_etfs, pct_change_days):
    etf_list = [base_etf] + companion_etfs
    df = get_data(etf_list)

    for etf in etf_list:
        for dias in pct_change_days:
            for col in usecols:
                df['pctchange_{}_{}_{}'.format(col,dias,etf)] = df['{}_{}'.format(col,etf)].pct_change(dias)

    df['oraculo'] = df['Open_' + base_etf].shift(-1) > df['Open_' + base_etf]
    df.dropna(inplace=True)

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
    return {
        'accuracy': metrics.accuracy_score(y_test, predicted),
        'precision': metrics.precision_score(y_test, predicted),
        'recall': metrics.recall_score(y_test, predicted),
        'f1': metrics.f1_score(y_test, predicted)
    }


def run_regression(companion_etfs=[]):
    base_etf = 'spy.us'
    df = prepare_dataframe(base_etf, companion_etfs, range(1,5))
    return do_logistic_regression(base_etf, df)


if __name__ == "__main__":
    run_regression()
