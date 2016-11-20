# -*- coding: utf-8 -*-

# This script describes how private sector savings interact affect the fiscal
# multiplier based on a geometric series interpretation. It is described in the
# accompanying iPython Notebook and at
#
# http://misunderheard.org/monetary_economics/2016/11/20/government_money_and_saving/
#

import matplotlib.pyplot as plt
import numpy as np

G     = 100 # government spending
theta = 0.2 # tax rate
alpha = 0.9 # propensity to consume

n_rounds = 30 # number of rounds we'll consider

# create an array of numbers from 0-30, one for each spending round
r = np.arange(0,n_rounds)

# solve equation 1 for each individual round
y_n = G*(alpha*(1-theta))**r

# solve equation 2 for each individual round
sum_y = G*(1-(alpha*(1-theta))**(r+1))/(1-alpha*(1-theta))

# plot
plt.bar(r,sum_y, color='r',label='cumulative income')
plt.bar(r,y_n, label='spending round income')
plt.grid()
plt.legend(loc='center right')
plt.xlabel('Spending round, n')
plt.ylabel('Income')

plt.tight_layout()
plt.show()

# calculate the final income
Y = G/(1-alpha*(1-theta))
print(Y)

# calculate the fiscal multiplier
print(1/(1-alpha*(1-theta)))

# calculate the total tax revenue
T = theta * Y
print(T)

# calculate the government budget position
print(T - G)

# calculate the total, accumulated savings
S = (1-alpha) * (1-theta) * Y
print(S)
