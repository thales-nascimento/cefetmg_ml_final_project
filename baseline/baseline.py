import pandas
import matplotlib.pyplot as plt
import sys

window=24

ibm_df = pandas.read_csv('../data/Stocks/ibm.us.txt', index_col='Date', parse_dates=True, usecols=['Date', 'Open'])
ibm_df['Rolling mean'] = pandas.Series.rolling(ibm_df, window).mean();


ax = ibm_df.plot(title="IBM Open prices")
ax.legend(['IBM', 'Rolling mean'], loc='upper left')
ax.set_xlabel('Date')
ax.set_ylabel('Open prices')
plt.show(block=False)


ibm_df['oraculo'] = ibm_df['Open'].shift(-1) > ibm_df['Open']
ibm_df['oraculo'] = ibm_df['oraculo'].apply(lambda x: 'vender' if x else 'comprar')

ibm_df = ibm_df.assign(decisao=ibm_df['Open'] > ibm_df['Rolling mean'].shift())
ibm_df['decisao'] = ibm_df['decisao'].apply(lambda x: 'vender' if x else 'comprar')

print(ibm_df)

hit_rate = ibm_df[(ibm_df.oraculo == ibm_df.decisao)].shape[0] / ibm_df.shape[0]

print()
print('taxa de acerto: {}'.format(hit_rate))

plt.show();
