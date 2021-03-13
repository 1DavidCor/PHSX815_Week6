# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 18:03:56 2021

@author: d338c921
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


# - Choose a function on a closed interval (the function *cannot* be a low order polynomial, but need not be too complicated). Choose a function that you can calculate the integral for analytically.

# - Implement Monte Carlo integration method to calculate the integral of a function

# - Compare the difference between the two numerical integrals, and their difference with the correct/analytic answer, as a function of the number sub-intervals. Is the difference between the two estimates a good indicator of the actual error?

### NUMERICAL INTEGRATION ###

#Set help flag to print flags
if '-h' in sys.argv:
    p = sys.argv.index('-h')
    print("Flags:")
    print("-sample_size [# of sample points]")
    print("-int_bound_l [left integration bound, float]")
    print("-int_bound_r [right integration bound, float]")
    sys.exit()

# Number of sub-intervals from user input
if '-sample_size' in sys.argv:
    p = sys.argv.index('-sample_size')
    N = int(sys.argv[p+1])
    
#set integration bounds from user input
if '-int_bound_l' in sys.argv:
    p = sys.argv.index('-int_bound_l')
    a = float(sys.argv[p+1])
    
if '-int_bound_r' in sys.argv:
    p = sys.argv.index('-int_bound_r')
    b = float(sys.argv[p+1])

##############################################################################
#Integrate!!! Define a function (positive for all x) to be integrated:
f = lambda x: x*x*x + 3*x*x
##############################################################################

#Sample from a uniform distribution; need an x and a y sample over region [a,b] U [f(a),f(b)]
x_sample = np.random.uniform(a, b, size = N)

#Area of the box (formed by y = 0 and y = f(max(a,b))) being sampled
if (f(b) > f(a)):
    area_bounds = (b - a) * f(b)
    y_sample = np.random.uniform(0, f(b), size = N)
else:
    area_bounds = (b - a) * f(a)
    y_sample = np.random.uniform(0, f(a), size = N)


def integrate_MC(f, a, b, N):
    
    #reject/accept
    accept = 0 #initiate accept counter
    x_accept = []
    y_accept = []
    x_reject = []
    y_reject = []

    for i in range(N):
    #Test if a point (x_i, y_i) is less than (x_i, f(x_i)); count # of "accepts"; seperate accepts vs. rejects to be plotted in different colors
        if (y_sample[i] < f(x_sample[i])): ###NEED SOMETHING ELSE HERE!!! ONLY WORKS FOR bounds where f(x)>0 right now
            accept = accept + 1 #add one to accept counter for an accept
            x_accept = np.append(x_accept, x_sample[i])
            y_accept = np.append(y_accept, y_sample[i])
        else:
            x_reject = np.append(x_reject, x_sample[i])
            y_reject = np.append(y_reject, y_sample[i])
    
    # plt.scatter(x_accept, y_accept, color = "g", marker = ".", label = "accepts")
    # plt.scatter(x_reject, y_reject, color = "r", marker = ".", label = "rejects")
    # plt.legend()
    # plt.show()
    
    integral = area_bounds * accept / N
    
    return integral #, area_bounds, accept, x_accept, y_accept, x_reject, y_reject

integral_arr = []   
for j in range(1, N+1, 100): 
    integral = integrate_MC(f, a, b, j)
    integral_arr = np.append(integral_arr, integral)

# print("Sample Size: N = " + str(N) + "\n")
# print("Number of accepts " + str(accept) + "\n")
# print("Number of rejects: " + str(N - accept) + "\n")
# print("Number of accepts / N : " + str(accept / N) + "\n")
# print("Area sampled : " + str(box_A) + "\n")
# print("Integral approx: " + str(accept / N * box_A) + "\n")

#plot integral approx as a function of num_intervals
plt.figure()
plt.title("Monte Carlo Integration: Accuracy vs. # Sample Points")
plt.xlabel("# Sample Points")
plt.ylabel("Calculated Integral Value")
plt.axhline(y = integrate.quad(f, a, b)[0], color = 'k', linestyle = '--', label = "Exact Integral Value")
plt.plot(np.linspace(0, N, integral_arr.size), integral_arr, color = "r", label = "Monte Carlo Integration")
plt.legend()
plt.show()