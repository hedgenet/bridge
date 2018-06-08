import krakenex

def spot(pair):
    """ returns the spot price of the currency pair """

    api = krakenex.API()

    params = {'pair':pair, 'count':1}
    result = api.query_public('Depth',data=params)['result'][pair]

    ask = result['asks'][0][0]
    bid = result['bids'][0][0]

    return (bid, ask)
