import numpy as np
from numpy import cumsum, log, polyfit, sqrt, std, subtract
import statsmodels.api as sm
import scipy.stats as sps

def dynamic_hurst_component(returns):
    power = 10
    n = 2**power
    
    hursts = np.array([])
    tstats = np.array([])
    pvalues = np.array([])
    res = np.array([])
    
    for t in np.arange(n, len(returns) + 1):
        # Specify subsample
        data = returns[t-n:t]
        X = np.arange(2, power + 1)
        Y = np.array([])
        for p in X:
            m = 2**p
            s = 2**(power-p)
            rs_array = np.array([])
            
            # Move across subsamples
            for i in np.arange(0, s):
                subsample = data[i*m:(i+1)*m]
                mean = np.average(subsample)
                deviate = np.cumsum(subsample-mean)
                difference = max(deviate) - min(deviate)
                stdev = np.std(subsample)
                rescaled_range = difference / stdev
                rs_array = np.append(rs_array, rescaled_range)
                
            # Calculating the log2 of average rescaled range
            Y = np.append(Y, np.log2(np.average(rs_array)))
        reg = sm.OLS(Y, sm.add_constant(X))
        res = reg.fit()
        hurst = res.params[1]
        tstat = (res.params[1] - 0.5) / res.bse[1]
        pvalue = 2 * (1 - sps.t.cdf(abs(tstat), res.df_resid))
        hursts = np.append(hursts, hurst)
        tstats = np.append(tstats, tstat)
        pvalues = np.append(pvalues, pvalue)
        
    return hursts, tstats, pvalues, n, res


def hurst_test(ts, min_lag=1, max_lag=100):
        lags = range(min_lag, max_lag)
        tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
        poly = polyfit(log(lags), log(tau), 1)
        return poly[0]*2.0