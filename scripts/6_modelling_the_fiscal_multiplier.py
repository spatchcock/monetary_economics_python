# -*- coding: utf-8 -*-

# This script describes how truncated and fully compounded fiscal multiplier
# scenarios can be consider to be equivalent. It is described in the accompanying 
# iPython Notebook and at 
#
# http://misunderheard.org/monetary_economics/2017/04/10/modelling_the_fiscal_multiplier/
#

# %%
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline 

G     = 100 # government spending
theta = 0.2 # tax rate

rounds = 5

# solve equation 1 for the 5th spending round
sum_y = G*(1-(1-theta)**(rounds+1))/(1-(1-theta))

print(sum_y)


# calculate the total tax paid after the 5th spending round
T = theta*sum_y

print(T)

# solve equation 2 for the 6th spending round
y = G*(1-theta)**(rounds) # gross income

# subtract the tax paid
y_d = (1-theta)*y           # disposable income

print(y_d)

# derive the implied alpha value

alpha = (1-(G/sum_y))/(1-theta)

print(alpha)

# calculate the total income with saving

sum_y = G/(1-alpha*(1-theta))

print(sum_y)

# calculate the implied savings and tax revenue

s = (1-alpha)*(1-theta)*sum_y
T = theta*sum_y

print(s)
print(T)


