import krakenex
import statistics

def candles(pair, interval=1, since=None):
    """ returns OHLC candles for the pair """

    api = krakenex.API()

    params = {'pair':pair, 'interval':interval, 'since':since}
    result = api.query_public('OHLC', data=params)['result'][pair]

    return result

def moments(pair, interval=1, since=None):
    """ returns the parameters (mean, stddev) of the magnitudes of the candles """

    # get the candles
    cs = candles(pair, interval, since)

    # compute their magnitudes
    magnitudes = [ float(c[4]) - float(c[1]) for c in cs ]

    # compute the statistics
    mean = statistics.mean(magnitudes)
    stdev = statistics.stdev(magnitudes)

    return mean, stdev
