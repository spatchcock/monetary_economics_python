# -*- coding: utf-8 -*-

# This script describes a simple the iteration of a simple economic model based
# on government money. It is described in the accompanying iPython Notebook and at 
#
# http://misunderheard.org/monetary_economics/2017/06/03/simple_economy_with_government_money/
#

# %% Include requrie libraries
import matplotlib.pyplot as plt
import numpy as np

#%% Define the number of time steps

N = 100

#%% Set the government fiscal policy

G     = 20  # government spending
theta = 0.2 # tax rate

#%% Set the propensity to consume

alpha = 0.9

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
    Y[t] = G/(1 - alpha*(1-theta))
    
    # calculate the tax paid on income for this time step (3)
    T[t] = theta * Y[t]
    
    # calculate the consumption spending for this time step (4)
    C[t] = alpha*(1 - theta)*Y[t]
    
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

#%% Plot government spending and tax revenue

# initialise plot figure
fig = plt.figure(figsize=(8, 4))

gov_plot = fig.add_subplot(121, xlim=(0, N), ylim=(0, np.max(G)*1.5))   # set axis limits
gov_plot.plot(range(N), np.repeat(G,N), lw=3)                           # plot constant G versus time
gov_plot.grid()                                                         # add gridlines
plt.xlabel('time')                                                      # label x axis
plt.ylabel('government spending')                                       # label y axis

tax_plot = fig.add_subplot(122, xlim=(0, N), ylim=(0, np.max(G)*1.5))   # set axis limits
tax_plot.plot(range(N), T, lw=3)                                        # plot tax revenue versus time
tax_plot.grid()                                                         # add gridlines
plt.xlabel('time')                                                      # label x axis
plt.ylabel('tax revenue')                                               # label y axis

plt.tight_layout() # space subplots neatly

#%% Out put some results from first time step

# Government spending (constant)
print(G)
# Tax revenue
print(T[0])
# Government budget position (deficit)
print(T[0]-G)
# Private saving rate
Y[0] - T[0] - C[0] # alternative formulation: (1-alpha)*(1-theta)*Y[0]

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

#%% Output sector balances at last time step

print(H_h[-1]) # the -1 index represents the last value in the array
print(H_g[-1])
