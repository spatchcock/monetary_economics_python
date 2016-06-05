# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline  

N = 100

C = np.zeros(N) # consumption
Y = np.zeros(N) # income
H = np.zeros(N) # stock of accumulated savings

alpha = 0.90

C[0] = 100
Y[0] = 100

for t in range(1, N):
    C[t] = alpha * Y[t-1]                # calculate spending based on earlier income (with some saving)
    Y[t] = C[t]                          # calculcate income earned in this time period
    H[t] = H[t-1] + (1 - alpha) * Y[t-1] # calculate increase in accumulated savings


# create a figure
fig = plt.figure(figsize=(12, 4))

# create a subplot for consumption
consumption_plot = fig.add_subplot(131)
# plot consumption (C) versus time step (N)
consumption_plot.plot(range(N), C, lw=3)
# add gridlines
consumption_plot.grid()
# ensure a zero origin for the y axis
consumption_plot.set_ylim([0, np.max(C)])
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
income_plot.set_ylim([0, np.max(Y)])
# label axes
plt.xlabel('time')
plt.ylabel('income')

# create a third subplot for private wealth
savings_plot = fig.add_subplot(133)
# plot savings (H) versus time step (N)
savings_plot.plot(range(N), H, lw=3)
# add gridlines
savings_plot.grid()
# ensure a zero origin for the y axis
savings_plot.set_ylim([0, 100])
# label axes
plt.xlabel('time')
plt.ylabel('accumulated savings')

# space subplots neatly
plt.tight_layout()

