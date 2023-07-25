from itertools import combinations
import pandas as pd
import numpy as np
import math
df= pd.read_csv(r'Performance.csv')
submatrix = {}

for i in range(0, 64, 4):
    submatrix[i]= df.iloc[0+i:4+i]

for i in combinations(submatrix, 8):

    training_set={}
    testing_set = {}
    for element in (i):
        training_set[element] = submatrix[element]
    for x in submatrix:
        if x not in training_set:
            testing_set[x] = submatrix[x]
    J = pd.concat(training_set)
    R = J.mean()/J.std()
    best = R[['SMAC', 'EMAC','RSISystem']].idxmax()
    Jbar = pd.concat(testing_set)
    Rbar = Jbar.mean()/Jbar.std()
    Rbar['pct_rank'] = Rbar.rank(pct=True)
    rank = Rbar['pct_rank'][best]
    logit = math.log(rank/(1-rank))