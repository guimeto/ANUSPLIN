"""
Created on Mon Feb  5 13:56:30 2018

@author: Guillaume Dueymes 
UQAM - Centre ESCER 
Librairie des indices de precipitation
"""

# Calcule la somme totale du signal entrant (moins de 20 % de valeurs manquantes)
def PrecTOT(S):
     import numpy as np
     ind_PrecTOT=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
     if ((N2/N) < 0.8):
         ind_PrecTOT = np.empty(1)
         ind_PrecTOT = np.nan
     else:     
         ind_PrecTOT = np.nansum(S_no_nan)        
     return ind_PrecTOT 
 
# Calcule la moyenne du signal entrant (moins de 20 % de valeurs manquantes)
def MOY(S):
     import numpy as np
     ind_moy=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
     if ((N2/N) < 0.8): 
         ind_moy = np.empty(1)
         ind_moy = np.nan
     else:    
         ind_moy = np.nanmean(S_no_nan)  
     return ind_moy      


# Calcul du pourcentage de jours de précipitation dans le signal entrant  (moins de 20 % de valeurs manquantes)
def Prcp1(S):
     import numpy as np
     ind_Prcp1=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
     if (N2 == 0):
         N2=1
         
     if ((N2/N) < 0.8): 
         ind_Prcp1 = np.empty(1)
         ind_Prcp1 = np.nan
     else:
         ind_Prcp1 = 0
         for row in S_no_nan:
             if row >= 1 :
                 ind_Prcp1 += 1 
                 
         ind_Prcp1 = 100 * (ind_Prcp1/N2)
     return ind_Prcp1        
 
# Calcul du 90ieme percentile de la distribution de la precipitation en mm/jour (moins de 20 % de valeurs manquantes)
def Prec90p(S):
     import numpy as np
     ind_Prec90p=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
#Le bloque suivant calcule le 90ieme percentile de la serie temporelle entree si il y au moins 80% des donnees entrantes qui correspondent a des valeurs valides (non-manquantes). 
#Dans les cas ou il y a plus de 20 % de valeurs manquantes,l'indice n'est pas calcule et la variable Prec_90p est definie par NaN.
     if ((N2/N) < 0.8): 
         ind_Prec90p = np.empty(1)
         ind_Prec90p = np.nan
     else:
         SS = S[S > 1]
# afin que l'index Prec90p soit significatif, il faut qu'il soit calcule avec au moins 15 valeurs
         if len(SS)  < 15 :
             ind_Prec90p = np.empty(1)
             ind_Prec90p = np.nan  
         else :        
             s_sorted = np.sort(SS)
# le rang 'm' est calcule apartir de la formule semi-empirique de probabilite de Cunnane (1978) 
             m=(len(SS)+0.2)*0.9 +0.4
# si le rang 'm' n'est pas un nombre entier, ils faut poursuivre avec une interpolation lineaire            
             if np.remainder(m,1) != 0:
                 m_floor=np.floor(m)
                 m_ceil=np.ceil(m)
                 slope=(s_sorted[int(m_ceil)-1]-s_sorted[int(m_floor)-1])/(m_ceil-m_floor)
                 ind_Prec90p=s_sorted[int(m_floor)-1]+slope*(m-m_floor)
             else: 
                 ind_Prec90p=s_sorted[int(m)-1];
     return ind_Prec90p
 
    
# valeur moyenne de l'intensite de precipitation pour les jours humides (PR sup a 1mm) (moins de 20 % de valeurs manquantes)
def SDII(S):
     import numpy as np
     ind_SDII=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
     if ((N2/N) < 0.8): 
         ind_SDII = np.empty(1)
         ind_SDII = np.nan
     else:
         SS = S[S > 1]        
         ind_SDII = np.nanmean(SS)
     return ind_SDII       

# calcul du nombre maximal de jours secs (inf a 1mm) consecutifs sur le signal entrant (moins de 20 % de valeurs manquantes)
def CDD(S):
     import numpy as np
     ind_CDD=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
     if ((N2/N) < 0.8): 
         ind_CDD = np.empty(1)
         ind_CDD = np.nan
     else:
         temp = 0
         ind_CDD = 0 
         j =0
         while (j < N2):
             while (j < N2 ) and (S_no_nan[j] < 1.0 ):
                 j += 1
                 temp +=1
             if ind_CDD < temp:
                 ind_CDD = temp
             temp = 0
             j += 1 
     return ind_CDD      
 
# calcul du nombre maximal de jours humides (sup a 1mm) consecutifs sur le signal entrant (moins de 20 % de valeurs manquantes)
def CWD(S):
     import numpy as np
     ind_CWD=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
     if ((N2/N) < 0.8): 
         ind_CWD = np.empty(1)
         ind_CWD = np.nan
     else:
         temp = 0
         ind_CWD = 0 
         j =0
         while (j < N2):
             while (j < N2 ) and (S_no_nan[j] > 1.0 ):
                 j += 1
                 temp +=1
             if ind_CWD < temp:
                 ind_CWD = temp
             temp = 0
             j += 1 
     return ind_CWD      
 
 # cumul maximal de precipitation sur 3 jours consecutifs de pluie (R3d)       
def R3d(S):
     import numpy as np
     ind_R3d=[]
     S_no_nan = S[~np.isnan(S)]
     N = len(S)
     N2 = len(S_no_nan)
     if ((N2/N) < 0.8): 
         ind_R3d = np.empty(1)
         ind_R3d = np.nan
     else:
         temp = 0
         ind_R3d = 0 
         for i in range(0,N-2):
             if (~np.isnan(S[i])) and  (~np.isnan(S[i+1]))  and  (~np.isnan(S[i+2])):
                 temp = S[i] + S[i+1] + S[i+2]
             if ind_R3d < temp:
                 ind_R3d = temp
     return ind_R3d    

       
         