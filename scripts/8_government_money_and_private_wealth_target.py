# -*- coding: utf-8 -*-

# This script describes the iteration of a simple economic model based
# on government money and including spending out of savings. It is described 
# in the accompanying iPython Notebook and at 
#
# http://misunderheard.org/monetary_economics/2017/07/19/government-money-and-private-wealth-target/
#

# %% Include requrie libraries
import matplotlib.pyplot as plt
import numpy as np

#%% Define the number of time steps

N = 100

#%% Set the government fiscal policy

G     = 20  # government spending
theta = 0.2 # tax rate

#%% Set the propensity to consume out of income and saved wealth

alpha_Y = 0.9
alpha_H = 0.2


#%% Initialize containers to hold results

# These are arrays of length N (the number of time steps)
Y   = np.zeros(N) # income
T   = np.zeros(N) # tax revenue
C   = np.zeros(N) # consumption
H_h = np.zeros(N) # private savings
H_g = np.zeros(N) # government balance

#%% Run model

for t in range(0, N):
    
    # calculate total income for this time step (equation 1)
    Y[t] = (G + alpha_H*H_h[t-1])/(1 - alpha_Y*(1-theta))
    
    # calculate the tax paid on income for this time step (3)
    T[t] = theta * Y[t]
    
    # calculate the consumption spending for this time step (4)
    C[t] = alpha_Y*(1 - theta)*Y[t] + alpha_H*H_h[t-1]
    
    # calculate the new level of private savings for this time step (5)
    H_h[t] = H_h[t-1] + Y[t] - T[t] - C[t]
    
    # calculate the new level of government money balance (6)
    H_g[t] = H_g[t-1] + T[t]- G
   

#%% Plot spending and income

# initialise plot figure
fig = plt.figure(figsize=(12, 4))

# plot government spending (G) through time
gov_plot = fig.add_subplot(131, xlim=(0, N), ylim=(0, 100))         # set axis limits
gov_plot.plot(range(N), np.repeat(G,N), lw=3)                       # plot constant G versus time
gov_plot.grid()                                                     # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('government spending')                                   # label y axis

# plot consumption spending (C) through time
consumption_plot = fig.add_subplot(132, xlim=(0, N), ylim=(0, 100)) # set axis limits
consumption_plot.plot(range(N), C, lw=3)                            # plot C versus time
consumption_plot.grid()                                             # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('consumption')                                           # label y axis

# plot aggregate income (Y) through time
income_plot = fig.add_subplot(133, xlim=(0, N), ylim=(0, 100))      # set axis limits
income_plot.plot(range(N), Y, lw=3)                                 # plot Y versus time
income_plot.grid()                                                  # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('income')                                                # label y axis

plt.tight_layout() # space subplots neatly

#%% Output some results from first time step

print(G)    # this is a constant
print(C[0]) # first time period - index 0
print(Y[0]) # first time period - index 0

#%% Output some results from last time step

print(G)     # this is a constant
print(C[-1]) # last time period - index -1
print(Y[-1]) # last time period - index -1

#%% Plot sector budget and balances

# initialise plot figure
fig = plt.figure(figsize=(8, 4))

budget_plot = fig.add_subplot(121, xlim=(0, N), ylim=(-10, 10))                     # set axis limits
budget_plot.plot(range(N), T-np.repeat(G,N), lw=3)                                  # plot gov budget versus time
budget_plot.plot(range(N), Y-T-C, lw=3)                                             # plot private budget versus time
budget_plot.grid()                                                                  # add gridlines
plt.xlabel('time')                                                                  # label x axis
plt.ylabel('budget position')                                                       # label y axis

balance_plot = fig.add_subplot(122, xlim=(0, N), ylim=(np.min(H_g), np.max(H_h)))   # set axis limits
balance_plot.plot(range(N), H_g, lw=3)                                              # plot gov balance versus time
balance_plot.plot(range(N), H_h, lw=3)                                              # plot private balance versus time
balance_plot.grid()                                                                 # add gridlines
plt.xlabel('time')                                                                  # label x axis
plt.ylabel('money balance')                                                         # label y axis

plt.tight_layout() # space subplots neatly

#%% Plot net saving dynamics

# calculate saving from income 
S_Y = (1-theta)*(1-alpha_Y)*Y

# calculate spending from saved wealth
C_H = (np.append(0, H_h[0:-1]))*alpha_H

# initialise plot figure
fig = plt.figure(figsize=(8, 4))

saving_plot = fig.add_subplot(111, xlim=(0, N), ylim=(0, 10))               # set axis limits

saving_plot.plot(range(N), S_Y,       lw=3, label='saving out of income')   # plot saving from income
saving_plot.plot(range(N), C_H,       lw=3, label='spending out of wealth') # plot spending from savings
saving_plot.plot(range(N), S_Y - C_H, lw=3, label='net saving')             # plot net saving

saving_plot.grid()                                                          # add gridlines

plt.xlabel('time')                                                          # label x axis
plt.ylabel('saving / dissaving per time period')                            # label y axis

legend = saving_plot.legend(loc='lower right', shadow=True)

plt.tight_layout() # space subplots neatly

#%% calculate steady state wealth-income ratio
(1 - alpha_Y)*(1 - theta)            # fractional saving out of income rate
((1 - alpha_Y)*(1 - theta))/alpha_H  # ratio of fractional saving from income and spending from savings

print(H_h[-1])        # final savings
print(Y[-1])          # final income
print(H_h[-1]/Y[-1])  # final wealth-income ratio













