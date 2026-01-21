# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from MCWEP.models_low_t import FluidPitzer

data = {
    't' : [-21.66016784	,0.03317214],
    'Ca': [0.272868977	,0.021785111],
    'K' : [0.073348259	,0.00786989],
    'Li': [0.016466741	,0.001107493],
    'Mg': [0.008402273	,0.001581756],
    'Sr': [0.004591392	,0.000378183],
    'Cs': [0.000260204	,8.67744E-06],
    'Rb': [0.000407099	,5.51968E-05],
    'Mn': [0.001878174	,0.000478762],
    'Zn': [0.001839751	,0.00031582],
    'Pb': [0.000334627	,4.35571E-05],
}

sample_no = 's2_9'

def uncertainty():
    # Set the parameters
    t= data['t' ][0]
    Ca=data['Ca'][0]
    K=data['K'][0]
    Li=data['Li'][0]
    Mg=data['Mg'][0]
    Sr=data['Sr'][0]
    Cs=data['Cs'][0]
    Rb=data['Rb'][0]
    Mn=data['Mn'][0]
    Zn=data['Zn'][0]
    Pb=data['Pb'][0]

    # Set the uncertainties in the parameters
    dt =   data['t'][1]
    dCa = data['Ca'][1]
    dK = data['K'][1]
    dLi = data['Li'][1]
    dMg = data['Mg'][1]
    dSr = data['Sr'][1]
    dCs = data['Cs'][1]
    dRb = data['Rb'][1]
    dMn = data['Mn'][1]
    dZn = data['Zn'][1]
    dPb = data['Pb'][1]

    # Define the number of Monte Carlo simulations to run
    N = 1000
    # Define an array to store the results
    x_values = np.zeros(N)

    # Define arrays to store the values of a_rand and b_rand

    t_rand  =  np.zeros(N)
    Ca_rand = np.zeros(N)
    K_rand = np.zeros(N)
    Li_rand = np.zeros(N)
    Mg_rand = np.zeros(N)
    Sr_rand = np.zeros(N)
    Cs_rand = np.zeros(N)
    Rb_rand = np.zeros(N)
    Mn_rand = np.zeros(N)
    Zn_rand = np.zeros(N)
    Pb_rand = np.zeros(N)

    # Perform the Monte Carlo simulation
    for i in range(N):
        # Generate random values for the parameters based on their uncertainties
        t_rand[i]  = np.random.normal(t ,  dt )
        Ca_rand[i] = np.random.normal(Ca,  dCa)
        K_rand[i]  = np.random.normal(K,   dK)
        Li_rand[i] = np.random.normal(Li,  dLi)
        Mg_rand[i] = np.random.normal(Mg,  dMg)
        Sr_rand[i] = np.random.normal(Sr,  dSr)
        Cs_rand[i] = np.random.normal(Cs,  dCs)
        Rb_rand[i] = np.random.normal(Rb,  dRb)
        Mn_rand[i] = np.random.normal(Mn,  dMn)
        Zn_rand[i] = np.random.normal(Zn,  dZn)
        Pb_rand[i] = np.random.normal(Pb,  dPb)
        # Use the find_x function to find the value of x given the random parameters
        # print('a_rand:',a_rand)

        fluid = FluidPitzer(
            x0=(3.38),
            species={
                'Na+': 1,
                'Ca+2': Ca_rand[i],
                'K+':   K_rand[i],
                'Li+':  Li_rand[i],
                'Mg+2': Mg_rand[i],
                'Sr+2': Sr_rand[i],
                'Cs+':  Cs_rand[i],
                'Rb+':  Rb_rand[i],
                'Mn+2': Mn_rand[i],
                'Zn+2': Zn_rand[i],
                'Pb+2': Pb_rand[i],
            },
            t=t_rand[i],
            solids=['H2O(S)']
        )

        x_values[i] = fluid.find_x()
        print('finished:', i)
    x_mean = np.mean(x_values)
    x_std = np.std(x_values)

    np.savetxt('E:\\work\\data\\low-T\\error_analysis_{}.csv'.format(sample_no), np.column_stack((
        t_rand ,
        Ca_rand,
        K_rand,
        Li_rand,
        Mg_rand,
        Sr_rand,
        Cs_rand,
        Rb_rand,
        Mn_rand,
        Zn_rand,
        Pb_rand,
        x_values
    )), delimiter=',',
               header='t,Ca,K,Li,Mg,Sr,Cs,Rb,Mn,Zn,Pb,Na', comments='')

    print("Mean value of x: ", x_mean)
    print("Standard deviation of x: ", x_std)

uncertainty()
