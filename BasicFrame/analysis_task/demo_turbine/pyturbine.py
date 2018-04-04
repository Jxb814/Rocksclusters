# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""

from seuif97 import pt2h, ps2h, pt2s

def CylinderEff(cylinder):
    """simple function  for cylinde using 'dict' """

    cylinder['inlet']['h'] = pt2h(cylinder['inlet']['p'], cylinder['inlet']['t'])
    cylinder['inlet']['s'] = pt2s(cylinder['inlet']['p'], cylinder['inlet']['t'])

    cylinder['outlet']['h'] = pt2h(cylinder['outlet']['p'], cylinder['outlet']['t'])
    cylinder['outlet']['s'] = pt2s(cylinder['outlet']['p'], cylinder['outlet']['t'])

    # h2s is the specific enthalpy at state 2 for the isentropic turbine
    h2s = ps2h(cylinder['outlet']['p'], cylinder['inlet']['s'])
    
    cylinder['h2s'] = h2s
     
    hds = cylinder['inlet']['h'] - h2s  # isentropic specific enthalpy drop
    hd = cylinder['inlet']['h'] - cylinder['outlet']['h']  # specific enthalpy drop

    cylinder['ef'] = 100 * hd / hds

    return cylinder

