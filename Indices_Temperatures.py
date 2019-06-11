# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 13:56:30 2018

@author: guillaume
"""

def Tmax90p(S):
     import numpy as np
     ind_tmax90p=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
# Nom: 90eme centile de la temperature maximale quotidienne
     if ((N2/N) < 0.8): 
         ind_tmax90p = np.empty(1)
         ind_tmax90p = np.nan
     else:    
        s_sorted = np.sort(S_no_nan)
 #  La formule de Blom's pour le calculer de la probabilite empirique afin dobtenir m(=rang ou index de la matrice) 
        m = (N2+0.25)*0.9 +(3/8) 
        if np.remainder(m,1) != 0:
            m_floor=np.floor(m)
            m_ceil=np.ceil(m)
            slope=(s_sorted[int(m_ceil)-1]-s_sorted[int(m_floor)-1])/(m_ceil-m_floor)
            ind_tmax90p=s_sorted[int(m_floor)-1]+slope*(m-m_floor)
        else: 
            ind_tmax90p=s_sorted[int(m)-1];
     return ind_tmax90p


def Tmin10p(S):
     import numpy as np
     ind_tmin10p=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
# Nom: 90eme centile de la temperature maximale quotidienne
     if ((N2/N) < 0.8): 
         ind_tmin10p = np.empty(1)
         ind_tmin10p = np.nan
     else:    
        s_sorted = np.sort(S_no_nan)
 #  La formule de Blom's pour le calculer de la probabilite empirique afin dobtenir m(=rang ou index de la matrice) 
        m = (N2+0.25)*0.1 +(3/8) 
        if  np.remainder(m,1)!= 0:
            m_floor=np.floor(m)
            m_ceil=np.ceil(m)
            slope=(s_sorted[int(m_ceil)-1]-s_sorted[int(m_floor)-1])/(m_ceil-m_floor)
            ind_tmin10p=s_sorted[int(m_floor)-1]+slope*(m-m_floor)
        else: 
            ind_tmin10p=s_sorted[int(m)-1];
     return ind_tmin10p            


def MOY(S):
     import numpy as np
     ind_moy=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
# Nom: 90eme centile de la temperature maximale quotidienne
     if ((N2/N) < 0.8): 
         ind_moy = np.empty(1)
         ind_moy = np.nan
     else:    
         ind_moy = np.nanmean(S_no_nan)  
     return ind_moy      
  

    