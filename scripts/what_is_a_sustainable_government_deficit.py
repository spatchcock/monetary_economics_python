# -*- coding: utf-8 -*-

# This script describes the interaction of economic growth rate, government budget
# deficit and the size of government debt. It is also described in the accompanying
# iPython Notebook and at 
#
# http://misunderheard.org/blog/2015/07/14/what-is-a-sustainable-government-deficit/
#

import numpy as np  
import matplotlib.pyplot as plt  
%matplotlib inline

#%% Create function which simulates economics scenario and plots course of government debt

def run_economy(time_steps, growth_rate, deficit_rate, start_income, start_debt):
       
    # Calculate the rate constant for economy growth based on passed in growth rate
    growth_rate_constant = (np.log(1 + growth_rate))
    
    # Initialize a list of timestep indices, e.g. 0, 1, 2, 3,...
    # This will be used to solve each of the equations through this number of timesteps
    # Since we're using the numpy library we can simply pass this vector of timesteps into 
    # the equations and get a vector of solutions
    time_vector = np.linspace(0,time_steps-1,time_steps)
    
    # Calculate incomes (i.e. GDP with growth) across all timesteps
    income = start_income * np.exp(growth_rate_constant * time_vector)
    
    # Calculate debt across all timesteps
    debt   = start_debt + (deficit_rate * start_income / growth_rate_constant) * (np.exp(growth_rate_constant * time_vector) - 1)

    # Calculate the debt ratio across all timesteps
    # We could just divide the debt and income variables at this stage but lets use the elegant form!
    debt_ratio = (deficit_rate / growth_rate_constant) + ((start_debt / start_income) - (deficit_rate / growth_rate_constant))*np.exp(-(growth_rate_constant * time_vector))

    # Now plot all
    fig = plt.figure()
    
    gdp_plot = fig.add_subplot(311, xlim=(0, time_steps), ylim=(0, np.max(income)))
    gdp_plot.grid()
    gdp_plot.plot(range(time_steps),income)
    plt.ylabel('GDP')
    
    debt_plot = fig.add_subplot(312, xlim=(0, time_steps), ylim=(0, np.max(debt)))
    debt_plot.grid()
    debt_plot.plot(range(time_steps),debt)
    plt.ylabel('Debt')

    debt_ratio_plot = fig.add_subplot(313, xlim=(0, time_steps), ylim=(0, np.max(debt_ratio)))
    debt_ratio_plot.grid()
    debt_ratio_plot.plot(range(time_steps),debt_ratio)
    plt.ylabel('Debt/GDP')    
    plt.xlabel('Time (arbitrary)')

    fig.show()

#%% Run some scenarios

run_economy(200, 0.02, 0.01, 500.0, 500.0)

run_economy(200, 0.02, 0.01, 500.0, 0.0)

run_economy(200, 0.02, 0.02, 500.0, 50.0)