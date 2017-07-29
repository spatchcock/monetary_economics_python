# -*- coding: utf-8 -*-

# This script describes the iteration of a simple economic model examining changing
# private sector spending behaviour. It is described in the accompanying iPython 
# Notebook and at 
#
# http://misunderheard.org/monetary_economics/2017/07/29/simple-model-of-boom-and-bust/
#

#%% Include libraries
import matplotlib.pyplot as plt
import numpy as np

# number of time steps
N = 100

# exogeneous variables

G = 20            # government spending

theta = 0.2       # tax rate

alpha_H = 0.2     # propensity to spend out of saved wealth

# endogeneous variables

Y   = np.zeros(N) # income
T   = np.zeros(N) # tax revenue
C   = np.zeros(N) # consumption
H_h = np.zeros(N) # private savings
H_g = np.zeros(N) # government balance

#%%  define propensity to consume time series

alpha_Y = np.zeros(N) 

alpha_Y[0:10]  = 0.9 # set the first 10 elements
alpha_Y[10:N]  = 0.8 # set the remainder of the elements

print(alpha_Y[0:15])

#%% set initial conditions

Y[0]   =  100
C[0]   =  80
T[0]   =  20
H_h[0] =  40
H_g[0] = -40

#%% run model

for t in range(1, N):
    
    # calculate total income for this time step (equation 1)
    Y[t] = (G + alpha_H*H_h[t-1])/(1 - alpha_Y[t]*(1-theta))
    
    # calculate the tax paid on income for this time step (3)
    T[t] = theta * Y[t]
    
    # calculate the consumption spending for this time step (4)
    C[t] = alpha_Y[t]*(1 - theta)*Y[t] + alpha_H*H_h[t-1]
    
    # calculate the new level of private savings for this time step (5)
    H_h[t] = H_h[t-1] + Y[t] - T[t] - C[t]
    
    # calculate the new level of government money balance (6)
    H_g[t] = H_g[t-1] + T[t]- G
   

#%% plot aggregates

# initialise plot figure
fig = plt.figure(figsize=(12, 4))

# plot government spending (G) through time
gov_plot = fig.add_subplot(131, xlim=(0, N), ylim=(0, 120))         # set axis limits
gov_plot.plot(range(N), np.repeat(G,N), lw=3)                       # plot constant G versus time
gov_plot.grid()                                                     # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('government spending')                                   # label y axis

# plot consumption spending (C) through time
consumption_plot = fig.add_subplot(132, xlim=(0, N), ylim=(0, 120)) # set axis limits
consumption_plot.plot(range(N), C, lw=3)                            # plot C versus time
consumption_plot.grid()                                             # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('consumption')     
# label y axis

# plot aggregate income (Y) through time
income_plot = fig.add_subplot(133, xlim=(0, N), ylim=(0, 120))      # set axis limits
income_plot.plot(range(N), Y, lw=3)                                 # plot Y versus time
income_plot.grid()                                                  # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('income')                                                # label y axis

plt.tight_layout() # space subplots neatly

#%% plot government

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

#%% plot sectoral balances

# initialise plot figure
fig = plt.figure(figsize=(8, 4))

budget_plot = fig.add_subplot(121, xlim=(0, N), ylim=(-10, 10))                     # set axis limits
budget_plot.plot(range(N), T-np.repeat(G,N), lw=3, label='Government')              # plot gov budget versus time
budget_plot.plot(range(N), Y-T-C, lw=3, label='Private sector')                     # plot private budget versus time
budget_plot.grid()                                                                  # add gridlines
plt.xlabel('time')                                                                  # label x axis
plt.ylabel('budget position')                                                       # label y axis
plt.legend(loc='upper right')

balance_plot = fig.add_subplot(122, xlim=(0, N), ylim=(np.min(H_g), np.max(H_h)))   # set axis limits
balance_plot.plot(range(N), H_g, lw=3, label='Government')                          # plot gov balance versus time
balance_plot.plot(range(N), H_h, lw=3, label='Private sector')                      # plot private balance versus time
balance_plot.grid()                                                                 # add gridlines
plt.xlabel('time')                                                                  # label x axis
plt.ylabel('money balance')                                                         # label y axis
plt.legend(loc='center right')

plt.tight_layout() # space subplots neatly

#%% reset propensity to consum time series

alpha_Y[0:10]  = 0.9
alpha_Y[10:50] = 0.8
alpha_Y[50:N]  = 0.9

#%% run model

for t in range(1, N):
    
    # calculate total income for this time step (equation 1)
    Y[t] = (G + alpha_H*H_h[t-1])/(1 - alpha_Y[t]*(1-theta))
    
    # calculate the tax paid on income for this time step (3)
    T[t] = theta * Y[t]
    
    # calculate the consumption spending for this time step (4)
    C[t] = alpha_Y[t]*(1 - theta)*Y[t] + alpha_H*H_h[t-1]
    
    # calculate the new level of private savings for this time step (5)
    H_h[t] = H_h[t-1] + Y[t] - T[t] - C[t]
    
    # calculate the new level of government money balance (6)
    H_g[t] = H_g[t-1] + T[t]- G
   
#%% plot aggregates
   
# initialise plot figure
fig = plt.figure(figsize=(12, 4))

# plot government spending (G) through time
gov_plot = fig.add_subplot(131, xlim=(0, N), ylim=(0, 130))         # set axis limits
gov_plot.plot(range(N), np.repeat(G,N), lw=3)                       # plot constant G versus time
gov_plot.grid()                                                     # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('government spending')                                   # label y axis

# plot consumption spending (C) through time
consumption_plot = fig.add_subplot(132, xlim=(0, N), ylim=(0, 130)) # set axis limits
consumption_plot.plot(range(N), C, lw=3)                            # plot C versus time
consumption_plot.grid()                                             # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('consumption')                                           # label y axis

# plot aggregate income (Y) through time
income_plot = fig.add_subplot(133, xlim=(0, N), ylim=(0, 130))      # set axis limits
income_plot.plot(range(N), Y, lw=3)                                 # plot Y versus time
income_plot.grid()                                                  # add gridlines
plt.xlabel('time')                                                  # label x axis
plt.ylabel('income')                                                # label y axis

plt.tight_layout() # space subplots neatly

#%% plot government

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

#%% plot sectoral balances

# initialise plot figure
fig = plt.figure(figsize=(8, 4))

budget_plot = fig.add_subplot(121, xlim=(0, N), ylim=(-10, 10))                     # set axis limits
budget_plot.plot(range(N), T-np.repeat(G,N), lw=3, label='Government')              # plot gov budget versus time
budget_plot.plot(range(N), Y-T-C, lw=3, label='Private sector')                     # plot private budget versus time
budget_plot.grid()                                                                  # add gridlines
plt.xlabel('time')                                                                  # label x axis
plt.ylabel('budget position')                                                       # label y axis
plt.legend(loc='upper right')

balance_plot = fig.add_subplot(122, xlim=(0, N), ylim=(np.min(H_g), np.max(H_h)))   # set axis limits
balance_plot.plot(range(N), H_g, lw=3, label='Government')                          # plot gov balance versus time
balance_plot.plot(range(N), H_h, lw=3, label='Private sector')                      # plot private balance versus time
balance_plot.grid()                                                                 # add gridlines
plt.xlabel('time')                                                                  # label x axis
plt.ylabel('money balance')                                                         # label y axis
plt.legend(loc='center right')

plt.tight_layout() # space subplots neatly

#%%
