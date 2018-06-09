import pandas
import os
import regression
from regression import *
from functools import lru_cache


regression.usecols=["Open", "High", "Low", "Close"] # redefine usecols


@lru_cache(1)
def run_correlator():
    base_etf = 'spy.us'
    etf_list = [x[:x.rfind(".")] for x in os.listdir(base_dir)]

    df = get_data(etf_list)
    final_corr = None

    for col in usecols:
        index = '{}_{}'.format(col,base_etf)

        # Compute correlation
        corr = df.filter(regex=col).corr()

        # Choose only columns related to the base etf
        corr = corr[index]

        #drop the correlation of the base etf with itself
        corr = corr.drop(index)

        #assign to pandas dataframe
        if final_corr is None:
            final_corr = pandas.DataFrame()
            final_corr[index] = corr
            final_corr = final_corr.rename(lambda s: s[s.find("_")+1:], axis='index')
        else:
            final_corr[index] = corr.values

    #Sort by average correlation
    final_corr['avg_corr'] = final_corr.mean(axis=1)
    final_corr['abs_avg_corr'] = final_corr['avg_corr'].abs()
    final_corr.sort_values('abs_avg_corr', ascending=False, inplace=True)

    return final_corr


if __name__ == "__main__":
    corr = run_correlator()
    print(run_correlator)
