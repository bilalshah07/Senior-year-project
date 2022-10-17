# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 22:13:27 2021

@author: Bilal Hyder
"""

import cmath as m
import numpy as np

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
th1 = -m.pi/8

# Basis changing waveplates
tq2 = m.pi/4
th2 = m.pi/8


#Making input state
inp = [[a],[b*m.exp(complex(0,phi))]]

print(inp)
#Making Waveplates

#State Generating QWP
qe11 = complex((m.cos(tq1))**2,(m.sin(tq1))**2)
qe123 = complex(m.cos(tq1)*m.sin(tq1),-m.cos(tq1)*m.sin(tq1))
qe14 = complex((m.sin(tq1))**2,(m.cos(tq1))**2)
qwp1 = [[qe11,qe123],[qe123,qe14]]

#Basis Changing QWP
qe21 = complex(m.cos(tq2)**2,m.sin(tq2)**2)
qe223 = complex(m.cos(tq2)*m.sin(tq2),-m.cos(tq2)*m.sin(tq2))
qe24 = complex(m.sin(tq2)**2,m.cos(tq2)**2)
qwp2 = [[qe21,qe223],[qe223,qe24]]

#State Generating HWP
hwp1 = [[m.cos(2*th1), m.sin(2*th1)],[m.sin(2*th1), -m.cos(2*th1)]]

#Basis Changing HWP
hwp2 = [[m.cos(2*th2), m.sin(2*th2)],[m.sin(2*th2), -m.cos(2*th2)]]

result = MatrixMultiply(qwp1, inp)
print('State after passing trough state generation QWP:', np.degrees(tq1),'\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')
#print('Prob H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)

result = MatrixMultiply(hwp1, result)
print('\nState after passing trough state generation HWP:', np.degrees(th1),'\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')
# print('Prob H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)

result = MatrixMultiply(qwp2, result)
print('\nState after passing trough basis changing QWP:', np.degrees(tq2),'\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')
#print('Prob H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)

result = MatrixMultiply(hwp2, result)
print('\nState after passing trough basis changing HWP:', np.degrees(th2),'\n[', "{:3.3f}".format(result[0][0]), ']\n[', "{:3.3f}".format(result[1][0]),']')

print('\nProb H: ', abs(result[0][0])**2, '\nProb V: ', abs(result[1][0])**2)

