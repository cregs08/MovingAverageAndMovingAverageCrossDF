import FindPatternInColumn
import talib

import pandas as pd


def create_market_close_data_and_moving_average_df(market_close_data, low_time_period, high_time_period,):
    #time_periods as ints
    market_close_data = pd.Series(market_close_data)

    low_ma = pd.Series(talib.MA(market_close_data, timeperiod=low_time_period, matype=0))
    high_ma = pd.Series(talib.MA(market_close_data, timeperiod=high_time_period, matype=0))

    #renaming so column names will be readable
    low_ma.name = low_time_period
    high_ma.name = high_time_period

    #there will be NaN values because of how MAs are calculated
    close_data_and_moving_average_df = pd.concat([market_close_data, low_ma, high_ma, ], axis=1).dropna()

    return close_data_and_moving_average_df


def create_market_data_MA_MAcross_DF(market_data, low_ma, high_ma):

    market_data_MAs = create_market_close_data_and_moving_average_df(market_data, low_ma, high_ma)

    low_MA_over_high_MA_boolean_series = \
        market_data_MAs[low_ma] > market_data_MAs[high_ma]

    #our cross is defined here e.g at period1 5ma = 10, 10ma = 11 => false; period2 5ma = 12, 10ma = 11.5 => True
    ma_crosses = FindPatternInColumn.find_boolean_pattern_in_column\
        ([False, True], low_MA_over_high_MA_boolean_series)

    market_data_MAs_and_crosses = pd.concat([market_data_MAs, low_MA_over_high_MA_boolean_series, ma_crosses],
                                            ignore_index=True, axis=1)

    market_data_MAs_and_crosses.columns = ['close', low_ma, high_ma, 'low_over_high', 'cross']

    return market_data_MAs_and_crosses

#demo code
#sample data as BTCUSDT 4h stored as pickle file 

if __name__ == '__main__':
    data_file = ''
    symbol = ''
    BTCUSDT_market_close_data = pd.read_pickle(data_file)[symbol]['close']
    low_ma = 5
    high_ma = 10
    print('Sample Code')

    print('Market Data\n', BTCUSDT_market_close_data.head())


    print('\nGetting the {}MA and the {}MA for {}....'.format(low_ma, high_ma, symbol))

    market_data_MA_df = \
        create_market_close_data_and_moving_average_df(BTCUSDT_market_close_data, low_ma, high_ma)
    print(market_data_MA_df.head())

    print('\nFinding crosses....')

    market_data_MA_MAcross_DF = create_market_data_MA_MAcross_DF(BTCUSDT_market_close_data, low_ma, high_ma)

    print(market_data_MA_MAcross_DF.head())

    crosses = market_data_MA_MAcross_DF[market_data_MA_MAcross_DF['cross']]
    print('\nIndices where crosses Occured')
    print(crosses.head())

    print("\nexample of cross\n")
    cross_idx = crosses.index
    first_cross = cross_idx[0]
    print(market_data_MA_MAcross_DF.loc[first_cross-5:first_cross+5])




