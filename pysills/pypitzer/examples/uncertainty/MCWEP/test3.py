

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from MCWEP.models import FluidPitzer

# Set the parameters
a = 2,
b = 25
# Set the uncertainties in the parameters
da = 0.28
db = 0.2
# Define the number of Monte Carlo simulations to run
N = 1000
# Define an array to store the results
x_values = np.zeros(N)

# Define arrays to store the values of a_rand and b_rand
a_rand = np.zeros(N)
b_rand = np.zeros(N)

# Perform the Monte Carlo simulation
for i in range(N):
    # Generate random values for the parameters based on their uncertainties
    a_rand[i] = np.random.normal(a, da)
    b_rand[i] = np.random.normal(b, db)
    # Use the find_x function to find the value of x given the random parameters
    # print('a_rand:',a_rand)
    fluid = FluidPitzer(
        x0=0.1,
        species={
            'Na+': 1,
            'K+': a_rand[i],
        },
        t=b_rand[i],
        solids=['KCl']
    )

    x_values[i] = fluid.find_x()
    print('finished:', i)

x_mean = np.mean(x_values)
x_std = np.std(x_values)

np.savetxt('E:\\work\\data\\low-T\\error_analysis.csv', np.column_stack((a_rand, b_rand, x_values)), delimiter=',',
           header='RK,Tm,mNa', comments='')

# # Plot the histograms of a_rand, b_rand, and x_values
# fig, axs = plt.subplots(1, 3, figsize=(12, 4))
# axs[0].hist(a_rand, bins=20)
# axs[0].set_xlabel('RK')
# axs[0].set_ylabel('Frequency')
# axs[1].hist(b_rand, bins=20)
# axs[1].set_xlabel('Tm')
# axs[1].set_ylabel('Frequency')
# axs[2].hist(x_values, bins=20)
# axs[2].set_xlabel('mNa')
# axs[2].set_ylabel('Frequency')
# plt.tight_layout()
# plt.show()

# Print the results
print("Mean value of x: ", x_mean)
print("Standard deviation of x: ", x_std)
