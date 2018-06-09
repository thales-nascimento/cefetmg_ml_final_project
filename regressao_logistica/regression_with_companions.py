import regression
from regression import run_regression
from correlator import run_correlator


df_correlation = run_correlator()


def run_regression_with_companions(first,last):
    companions = list(df_correlation.index[first:last])
    score = run_regression(companion_etfs=companions)
    score['num_companions'] = len(companions)
    score['first'] = first
    score['companions'] = companions
    return score


def exaustive_search():
    num_etfs = df_correlation.shape[0]
    best_accuracy = {'accuracy':0}
    best_f1 = {'f1':0}
    for q in range(1,num_etfs):
        for first in range(num_etfs-q):
            score = run_regression_with_companions(first,first+q)
            if score['accuracy'] > best_accuracy['accuracy']:
                best_accuracy = score
                print('\nnew best ACCURACY:',score)
            if score['f1'] > best_f1['f1']:
                best_f1 = score
                print('\nnew best F1:',score)


if __name__ == "__main__":
    exaustive_search()
