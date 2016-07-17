# -*- coding: utf-8 -*-

# This script describes how to use a time-dependent exogenous variable. It is 
# described in the accompanying iPython Notebook and at 
#
# http://misunderheard.org/monetary_economics/2016/07/17/exogenous_and_endogenous_variables/
#

# import required Python libraries
import matplotlib.pyplot as plt
import numpy as np

#%% Set up model

# set the number of time steps
N = 100

# initialise containers for endogenous variables
C = np.zeros(N) # consumption
Y = np.zeros(N) # income
H = np.zeros(N) # stock of accumulated savings

#%% Set up exogenous variables

# propensity to spend out of savings. This will be a constant
alpha_h = 0.05

# propensity to spend out of income. This will be a function of time.
# Two options below, comment/uncomment as appropriate

alpha_y = np.zeros(N) # initialize container array

# step function
alpha_y[0:40] = 0.90
alpha_y[40:] = 0.85

# sine function
# alpha_y = 0.90 - 0.05*np.sin(np.linspace(1,N,N)*(2*np.pi/N))

# plot alpha_y function
plt.plot(alpha_y)
plt.ylim([0.6, 1])
plt.grid()
plt.xlabel('time')
plt.ylabel('propensity to spend out of income')

#%% Set initial conditions

# These are steady state values for initial conditions
C[0] = 33.33
Y[0] = 33.33
H[0] = 66.66

#%% Propagate model economy through time

for t in range(1, N):
    C[t] = alpha_y[t] * Y[t-1] + alpha_h * H[t-1]                
    Y[t] = C[t]                                                  
    H[t] = H[t-1] + (1 - alpha_y[t]) * Y[t-1] - alpha_h * H[t-1] 


#%% Plot results

# create a figure
fig = plt.figure(figsize=(12, 4))

# create a subplot for consumption
consumption_plot = fig.add_subplot(131)
# plot consumption (C) versus time step (N)
consumption_plot.plot(range(N), C, lw=3)
# add gridlines
consumption_plot.grid()
# ensure a zero origin for the y axis
consumption_plot.set_ylim([0, 100])
# label axes
plt.xlabel('time')
plt.ylabel('consumption')

# create a second subplot for income
income_plot = fig.add_subplot(132)
# plot income (Y) versus time step (N)
income_plot.plot(range(N), Y, lw=3)
# add gridlines
income_plot.grid()
# ensure a zero origin for the y axis
income_plot.set_ylim([0, 100])
# label axes
plt.xlabel('time')
plt.ylabel('income')

# create a third subplot for private wealth
wealth_plot = fig.add_subplot(133)
# plot wealth (H) versus time step (N)
wealth_plot.plot(range(N), H, lw=3)
# add gridlines
wealth_plot.grid()
# ensure a zero origin for the y axis
wealth_plot.set_ylim([0, 100])
# label axes
plt.xlabel('time')
plt.ylabel('wealth')

# space subplots neatly
plt.tight_layout()

