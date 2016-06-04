# -*- coding: utf-8 -*-

# This script describes the circulation of a fixed amount of money on the assumption 
# that everyone spends all of their income. It is described in the accompanying
# iPython Notebook and at 
#
# http://misunderheard.org/monetary_economics/2016/06/04/spending-income-and-the-circular-flow-of-money/
#

import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline  

#%% Set up model

# Set number of time steps
N = 100

# Initialize arrays for storing time evolution of variables
C = np.zeros(N) # consumption
Y = np.zeros(N) # income

# Set initial conditions
C[0] = 100
Y[0] = 100

#%% Propagate model economy through time

for t in range(1, N):
    C[t] = Y[t-1] # calculate spending based on earlier income
    Y[t] = C[t]   # calculcate income earned in this time period

#%% Plot results

# create a figure
fig = plt.figure(figsize=(8, 4))

# create a subplot for consumption
consumption_plot = fig.add_subplot(121)
# plot consumption (C) versus time step (N)
consumption_plot.plot(range(N), C, lw=3)
# add gridlines
consumption_plot.grid()
# label axes
plt.xlabel('time')
plt.ylabel('consumption')

# create a second subplot for income
income_plot = fig.add_subplot(122)
# plot income (Y) versus time step (N)
income_plot.plot(range(N), Y, lw=3)
# add gridlines
income_plot.grid()
# label axes
plt.xlabel('time')
plt.ylabel('income')

# space subplots neatly
plt.tight_layout()