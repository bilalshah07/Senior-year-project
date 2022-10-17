# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:14:03 2021

@author: Bilal Hyder
"""

"""
Created on Tue Aug  3 22:13:27 2021

@author: Bilal Hyder
"""

import cmath as m
import pylab as pl
import numpy as np

def Send(a, b, phi, tq1, th1, tq2, th2):
    
    # Making input state
    inp = [[a],[b*m.exp(complex(0,phi))]]
    
    
    # Making Waveplates
    
    # State Generating QWP
    qe11 = complex((m.cos(tq1))**2, (m.sin(tq1))**2)
    qe123 = complex(m.cos(tq1)*m.sin(tq1), -m.cos(tq1)*m.sin(tq1))
    qe14 = complex((m.sin(tq1))**2, (m.cos(tq1))**2)
    qwp1 = [[qe11,qe123],[qe123,qe14]]
    
    # Basis Changing QWP
    qe21 = complex(m.cos(tq2)**2,m.sin(tq2)**2)
    qe223 = complex(m.cos(tq2)*m.sin(tq2),-m.cos(tq2)*m.sin(tq2))
    qe24 = complex(m.sin(tq2)**2,m.cos(tq2)**2)
    qwp2 = [[qe21,qe223],[qe223,qe24]]
    
    # State Generating HWP
    hwp1 = [[m.cos(2*th1), m.sin(2*th1)],[m.sin(2*th1), -m.cos(2*th1)]]
    
    # Basis Changing HWP
    hwp2 = [[m.cos(2*th2), m.sin(2*th2)],[m.sin(2*th2), -m.cos(2*th2)]]
    
    # Passing through apparatus
    
    result = MatrixMultiply(qwp1, inp)
    #print('State after passing trough state generation QWP:\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')
    #print('Prob H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)
    
    # result = MatrixMultiply(hwp1, result)
    #print('\nState after passing trough state generation HWP:\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')
    #print('Prob H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)
    
    # result = MatrixMultiply(qwp2, result)
    #print('\nState after passing trough basis changing QWP:\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')
    #print('Prob H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)
    
    # result = MatrixMultiply(hwp2, result)
    #print('\nState after passing trough basis changing HWP:\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')
    
    #print('\nProb H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)
    
    return result
    

def MatrixMultiply(matrix1, matrix2):
        matrixr = [[0],[0]]
        for i in range(2):
            for j in range(1):
                for k in range(2):
                    matrixr[i][j] += matrix1[i][k] * matrix2[k][j]
        
        return matrixr


# Input state
a = 1
b = 0
phi = 0


# Waveplate angles (All angles in radians)

# State generation waveplates
tq1 = 0
th1 = 0

# Basis changing waveplates
tq2 = 0
th2 = 0


# Lists to store data

hlist = []
vlist = []
tlist = []
tq1list = []
tq2list = []
th1list = []
th2list = []


# Making Waveplate Rotations


# State Generating QWP
for i in np.arange(0, 2*m.pi, 0.01):
    tq1 = i
    result = Send(a, b, phi, tq1, th1, tq2, th2)
    tq1list.append(tq1 * 180/m.pi)
    hlist.append(abs(result[0][0])**2)
    vlist.append(abs(result[1][0])**2)

'''
# State Generating HWP
for i in np.arange(0, m.pi, 0.01):
    th1 = i
    result = Send(a, b, phi, tq1, th1, tq2, th2)
    th1list.append(th1 * 180/m.pi)
    hlist.append(abs(result[0][0])**2)
    vlist.append(abs(result[1][0])**2)
'''
'''
# Basis Changing QWP
for i in np.arange(0, 2*m.pi, 0.01):
    tq2 = i
    result = Send(a, b, phi, tq1, th1, tq2, th2)
    tq2list.append(tq2 * 180/m.pi)
    hlist.append(abs(result[0][0])**2)
    vlist.append(abs(result[1][0])**2)
'''
  
# # Basis Changing HWP
# for i in np.arange(0, 2*m.pi, 0.01):
#     th2 = i
#     result = Send(a, b, phi, tq1, th1, tq2, th2)
#     th2list.append(th2 * 180/m.pi)
#     hlist.append(abs(result[0][0])**2)
#     vlist.append(abs(result[1][0])**2)



pl.plot(tq1list, hlist, label = 'H pol.')
pl.plot(tq1list, vlist, label = 'V pol.')
pl.xlabel("HWP Angle (degrees)")
pl.ylabel("Probability of state")
pl.show()
    