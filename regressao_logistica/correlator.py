import pandas
import os
from regressao import *

usecols=["Open", "High", "Low", "Close"] # redefine usecols


def run_correlator():
    base_etf = 'spy.us'
    etf_list = [x[:x.rfind(".")] for x in os.listdir(base_dir)]

    df = get_data(etf_list, usecols)
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
    final_corr = final_corr.sort_values('avg_corr', ascending=False)
    print(final_corr)



if __name__ == "__main__":
    run_correlator()
