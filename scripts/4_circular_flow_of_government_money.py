# -*- coding: utf-8 -*-

# This script describes the calculation of aggregate income based on the concept
# of the fiscal multiplier as a geometric series. It is described in the
# accompanying iPython Notebook and at:
#
# http://misunderheard.org/monetary_economics/2016/11/20/circular-flow-of-government-money/
#

# import libraries
import matplotlib.pyplot as plt
import numpy as np

G     = 100 # government spending
theta = 0.2 # tax rate

n_rounds = 30 # number of rounds we'll consider

# create an array of numbers from 0-30, one for each spending round
r = np.arange(0,n_rounds)

# solve equation 1 for each individual round
y = G*(1-theta)**r

# solve equation 2 for each individual round
sum_y = G*(1-(1-theta)**(r+1))/(1-(1-theta))

# plot
plt.bar(r,sum_y, color='r',label='cumulative income')
plt.bar(r,y, color='b', label='spending round income')
plt.grid()
plt.legend(loc='center right')
plt.xlabel('Spending round, n')
plt.ylabel('Income')

plt.tight_layout()
plt.show()
