import regression
from regression import run_regression
from correlator import run_correlator


def run_regression_with_companions(first,last):
    df_correlation = run_correlator()
    companion = list(df_correlation.index[first:last])
    print(first,last,companion)
    run_regression(companion_etfs=companion)
    print()


if __name__ == "__main__":
    import sys
    for q in range(1,11):
        for first in range(20):
            run_regression_with_companions(first,first+q)
