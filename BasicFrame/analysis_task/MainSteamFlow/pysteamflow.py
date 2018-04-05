# -*- coding: utf-8 -*-
'''
Created on 2018年4月5日

@author: user
'''
from seuif97 import pt2v
from numpy import square

def SteamFlow(inletstate, RatedState):

    inletstate['v'] = pt2v(inletstate['p'], inletstate['t'])
    RatedState['v'] = pt2v(RatedState['p'], RatedState['t'])
    
    inletstate['G'] = {RatedState['G']*inletstate['p']/RatedState['p']
                       *square(RatedState['p']*RatedState['v']/(inletstate['p']*inletstate['v']))}
    
    return inletstate['G']