
from collections import defaultdict
import random
import comp140_module3 as stocks

def markov_chain(data, order):
   
    dictionary = {}

    for i_0 in range(len(data)-(order)):
    
        for i_1 in range(order):
            combination = (data[i_0:i_0+order])
            tuples = tuple(combination)
            prediction = data[order+i_0]
            newlist = [tuples , prediction]
        print(newlist)

        if tuples in dictionary:
            if prediction in dictionary.get(tuples):
                dictionary.get(tuples)[prediction] = dictionary.get(tuples)[prediction]+ 1
            else:
                dictionary.get(tuples)[prediction] = 1
        else:
            dictionary[tuples] = {prediction: 1}
    chain = {}    

    for state in dictionary:
        numofpred = list(dictionary[state].values())
        probabilities = {}
        sumnumofpred = sum(numofpred)
        for pred, freq in dictionary[state].items():
            probabilities[pred] = freq/sumnumofpred
        chain[state] = probabilities
    
    return chain

def predict(model, last, num):
   
    nextstates = []
    copyoflast = last.copy()
    
    for i_0 in range(num):
        predictedprob = model.get(tuple(copyoflast[i_0:]),{})
        if predictedprob == {}:
            pred = int(random.randrange(0,4))
            copyoflast.append(pred)
            nextstates.append(pred)
        chance = random.random()
        finalp = 0
        nextp = 0
            
        for i_1 in predictedprob:
            nextp = nextp + predictedprob.get(i_1)
            if nextp > chance > finalp:
                copyoflast.append(i_1)
                nextstates.append(i_1)
            else:
                finalp = nextp        
    
    return nextstates

def mse(result, expected):
    
    totalsum = 0
    length_0 = len(result)
    for i_0 in range(length_0):
        squareddiff = (result[i_0] - expected[i_0])**2
        totalsum += squareddiff
        
    meansquarederror = totalsum / length_0
    
    return meansquarederror


def run_experiment(train, order, test, future, actual, trials):
    
    markovchain0 = markov_chain(train, order)
    sumsofmse = 0
    trial_0 = 0
    
    while trials > trial_0:
        nextstates = predict(markovchain0,test,future)
        trial_0 += 1
        sumsofmse += mse(actual, nextstates)
    
    return sumsofmse / trials


def run():
    
    symbols = stocks.get_supported_symbols()

   
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

   
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

   
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

   
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

run()
