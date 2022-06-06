import numpy as np
import pandas as pd
from math import exp

def BinomialTree3(option_type, S0, K, r, sigma, q, T, N=2000, american="false"):
    # we improve the previous tree by checking for early exercise for american options
    '''
    option_type = 'C'
    S0 = 100
    K = 130
    r = 0.01
    sigma = 0.3
    q = 0.03
    T = 2
    N=2000
    american="false" 
    '''

    # calculate delta T    
    deltaT = float(T)/N
 
    #Calculate CRR u and d factors
    u = np.exp(sigma*np.sqrt(deltaT))
    d = 1.0 / u
 
    #init the arrays using numpy
    fs =  np.asarray([0.0 for i in range(N + 1)])
    
    #stock tree for calculations of expiration values
    fs2 = np.asarray([(S0*(1-q) * u**j * d**(N - j)) for j in range(N + 1)])
    
    #vectorize the strikes as well so the expiration check will be faster
    fs3 =np.asarray( [float(K) for i in range(N + 1)])
    
    #rates are fixed so the probability of up and down are fixed.
    #this is used to make sure the drift is the risk free rate
    p = (np.exp((r-q)*deltaT) - d)/(u - d)
    oneMinusP = 1.0 - p
    
    # Compute the leaves, f_{N, j}
    if type =="C":
        fs[:] = np.maximum(fs2-fs3, 0.0)
    else:
        fs[:] = np.maximum(-fs2+fs3, 0.0)
    
    #calculate backward the option prices
    for i in range(N-1, -1, -1):
        fs[:-1]=np.exp(-r * deltaT) * (p * fs[1:] + oneMinusP * fs[:-1])
        fs2[:]=fs2[:]*u
      
        if american=='true':
            #Simply check if the option is worth more alive or dead
            if type =='C':
                fs[:]=np.maximum(fs[:],fs2[:]-fs3[:])
            else:
                fs[:]=np.maximum(fs[:],-fs2[:]+fs3[:])
    return fs[0]

def BinomialTreePayoff(option_type, S0, K, r, sigma, q, T, N=2000):
    # we improve the previous tree by checking for early exercise for american options
    '''
    option_type = 'Call'
    S0 = 100
    K = 130
    r = 0.05
    sigma = 0.3
    q = 0.03
    T = 1
    N = 5
    '''

    # calculate delta T    
    deltaT = float(T)/N
 
    #Calculate CRR u and d factors
    u = np.exp(sigma*np.sqrt(deltaT))
    d = 1.0 / u
 
    #init the arrays using numpy
    px = pd.DataFrame([[S0*(1-q) * (u**(i - j - 1)) * (d**(j)) 
                           for j in range(i) ] 
                              for i in range(1, N + 2) ]).T
    
    #rates are fixed so the probability of up and down are fixed.
    #this is used to make sure the drift is the risk free rate
    p = (exp((r-q)*deltaT) - d)/(u - d)
    e_mrt = exp(-r * deltaT)
    
    f_ud = pd.DataFrame(np.zeros((N + 1, N + 1)))
    
    # Compute the payoff of the terminal leaf
    if option_type.lower() =="call":
        f_ud.iloc[:,-1] = (px - K).iloc[:,-1].map(lambda x: max(x, 0))
    else:
        f_ud.iloc[:,-1] = (K - px).iloc[:,-1].map(lambda x: max(x, 0))
    
    #calculate backward the option prices
    for i in range(N, 0, -1):
        f_ud.iloc[:, i - 1] = [e_mrt * (p * f_ud.iloc[j, i] + (1 - p) * f_ud.iloc[j+1, i]) if j < i else 0
                              for j in range(N + 1)]
        
    return(px, f_ud)

def BinomialTreeConvergence(option_type, S0, K, r, sigma, q, T, N, american):
    # this loops over the N deltas of the tree
    px = []
    for itr in range(N):
        px.append(BinomialTree3('C', S0, K, r, sigma, q, T, itr + 1, 'false'))
    return(px)

def tester():
    print('BT succesfully imported')