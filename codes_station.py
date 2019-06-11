# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:03:03 2019

@author: guillaume
"""

def get_closed_station_precip(lati, loni, yeari, yearf):
    
     import pandas as pd
     import os 
     import calendar
     import numpy as np
     from datetime import date
     
     dataframe = pd.read_excel("K:/DATA/Donnees_Stations/2nd_generation_V2018/Adj_Precipitation_Stations.xls", skiprows = range(0, 3))
     dataframe_2 =  dataframe.loc[(dataframe["année déb."] <= yeari) & (dataframe["année fin."] >= yearf),:]
     dataframe_2 = dataframe_2.reset_index(drop=True)
     lats = dataframe_2['lat (deg)']
     lons = dataframe_2['long (deg)']
     dist_sq = (lats-lati)**2 + (lons-loni)**2 
     # 1D index of minimum dist_sq element
     minindex = dist_sq.idxmin()     
     stnid = dataframe_2.iloc[minindex]['stnid'] 
     df_station =  pd.DataFrame(dataframe_2.iloc[minindex]) 
     f1 = open('K:/DATA/Donnees_Stations/2nd_generation_V2018/Adj_Daily_Total_v2017/dt'+str(stnid).replace(' ', '')+'.txt', 'r')
     f2 = open('./tmp.txt', 'w')
    
    ### nettoyage des données: Suppression des Caractères   
     for line in f1:
            for word in line:
                if word == 'M':
                    f2.write(word.replace('M', ' '))
                elif word == 'a':
                    f2.write(word.replace('a', ' '))  
                elif word == 'Z':
                    f2.write(word.replace('Z', ' '))   
                elif word == 'Z':
                    f2.write(word.replace('X', ' '))   
                elif word == 'T':
                    f2.write(word.replace('T', ' '))  
                elif word == 'Y':
                    f2.write(word.replace('Y', ' ')) 
                elif word == 'X':
                    f2.write(word.replace('X', ' '))     
                else:
                    f2.write(word)
     f1.close()
     f2.close()
              
     station = pd.read_csv('./tmp.txt', delim_whitespace=True, skiprows = range(0, 1))
       
     station.columns = ['Annee', 'Mois', 'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10',
                                      'D11','D12','D13','D14','D15','D16','D17','D18','D19','D20',
                                      'D21','D22','D23','D24','D25','D26','D27','D28','D29','D30','D31']
         
     os.remove("./tmp.txt")
       
       # nettoyage des valeurs manquantes 
     try:  
           station = station.replace({'E':''}, regex=True)
     except:
           pass
     try: 
           station = station.replace({'a':''}, regex=True)
     except:
           pass
     try:     
           station = station.replace({'-9999.9':''}, regex=True)
     except:
           pass
     try:     
           station = station.replace({-9999.9:''}, regex=True)
     except:
           pass    
           
     for col in  station.columns[2:]:
           station[col] = pd.to_numeric(station[col], errors='coerce')
           
     m_start =  station['Mois'].loc[(station['Annee'] == yeari)].min()
     m_end   =  station['Mois'].loc[(station['Annee'] == yearf)].max()
       
     d_end = calendar.monthrange(yearf, m_end)[1]
       
    ####################################Extraction des données quotidiennes  et ajout d'une colonne Date      
     tmp_tmin = [ ] 
     for year in range(yeari, yearf+1):    ### Boucle sur les annees
           for month in range(1,13):
               df = []
               last_day = calendar.monthrange(year, month)[1] 
               tmin = station.loc[(station["Annee"] == year) & (station["Mois"] == month)].iloc[:,2:last_day+2].values
               
               if len(tmin) == 0:
                   a = np.empty((calendar.monthrange(year,month)[1]))
                   a[:] = np.nan
                   df=pd.DataFrame(a)
               else:
                   df=pd.DataFrame(tmin.T)
                   
               start = date(year, month, 1)
               end =   date(year, month, last_day)
               delta=(end-start) 
               nb_days = delta.days + 1 
               rng = pd.date_range(start, periods=nb_days, freq='D')          
               df['datetime'] = rng
               df.index = df['datetime']
               tmp_tmin.append(df)
               
     tmp_tmin = pd.concat(tmp_tmin) 
     df = pd.DataFrame({'datetime': tmp_tmin['datetime'], 'variable': tmp_tmin.iloc[:,0]}, columns = ['datetime','variable']) 
     df.index = df['datetime']
     df = df.drop(["datetime"], axis=1)
     
     
     return df, df_station


def get_closed_station_temp(lati, loni, yeari, yearf, variable):
    
     import pandas as pd
     import os 
     import calendar
     import numpy as np
     from datetime import date
 
     dataframe = pd.read_excel("K:/DATA/Donnees_Stations/2nd_generation_V2018/Temperature_Stations.xls", skiprows = range(0, 3))
     dataframe_2 =  dataframe.loc[(dataframe["année déb."] <= yeari) & (dataframe["année fin."] >= yearf),:]
     dataframe_2 = dataframe_2.reset_index(drop=True)
     lats = dataframe_2['lat (deg)']
     lons = dataframe_2['long (deg)']
     dist_sq = (lats-lati)**2 + (lons-loni)**2 
     # 1D index of minimum dist_sq element
     minindex = dist_sq.idxmin()     
     stnid = dataframe_2.iloc[minindex]['stnid'] 
     df_station =  pd.DataFrame(dataframe_2.iloc[minindex]) 
     if variable == 'tasmax':         
         f1 = open('K:/DATA/Donnees_Stations/2nd_generation_V2018/Homog_daily_max_temp_v2018/dx'+str(stnid).replace(' ', '')+'.txt', 'r')
         f2 = open('./tmp.txt', 'w')
     elif variable == 'tasmin':         
         f1 = open('K:/DATA/Donnees_Stations/2nd_generation_V2018/Homog_daily_min_temp_v2018/dn'+str(stnid).replace(' ', '')+'.txt', 'r')
         f2 = open('./tmp.txt', 'w')  
     elif variable == 'tasmoy':         
         f1 = open('K:/DATA/Donnees_Stations/2nd_generation_V2018/Homog_daily_mean_temp_v2018/dm'+str(stnid).replace(' ', '')+'.txt', 'r')
         f2 = open('./tmp.txt', 'w')    
         
    
    ### nettoyage des données: Suppression des Caractères   
     for line in f1:
        for word in line:
            if word == 'M':
                f2.write(word.replace('M', ' '))
            elif word == 'a':
                f2.write(word.replace('a', ' '))                    
            else:
                f2.write(word)
     f1.close()
     f2.close()
          
     station = pd.read_csv('./tmp.txt', delim_whitespace=True, skiprows = range(0, 4))
   
     station.columns = ['Annee', 'Mois', 'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10',
                                  'D11','D12','D13','D14','D15','D16','D17','D18','D19','D20',
                                  'D21','D22','D23','D24','D25','D26','D27','D28','D29','D30','D31']
     
     os.remove("./tmp.txt")
   
   # nettoyage des valeurs manquantes 
     try:  
       station = station.replace({'E':''}, regex=True)
     except:
       pass
     try: 
       station = station.replace({'a':''}, regex=True)
     except:
       pass
     try:     
       station = station.replace({'-9999.9':''}, regex=True)
     except:
       pass
     try:     
       station = station.replace({-9999.9:''}, regex=True)
     except:
       pass    
       
     for col in  station.columns[2:]:
       station[col] = pd.to_numeric(station[col], errors='coerce')
       
     m_start =  station['Mois'].loc[(station['Annee'] == yeari)].min()
     m_end   =  station['Mois'].loc[(station['Annee'] == yearf)].max()
   
     d_end = calendar.monthrange(yearf, m_end)[1]
   
####################################Extraction des données quotidiennes  et ajout d'une colonne Date   
     tmp_tmin = [ ] 
     for year in range(yeari,yearf+1):    ### Boucle sur les annees
       for month in range(1,13):
           df = []
           last_day = calendar.monthrange(year, month)[1] 
           tmin = station.loc[(station["Annee"] == year) & (station["Mois"] == month)].iloc[:,2:last_day+2].values
           
           if len(tmin) == 0:
               a = np.empty((calendar.monthrange(year,month)[1]))
               a[:] = np.nan
               df=pd.DataFrame(a)
           else:
               df=pd.DataFrame(tmin.T)
               
           start = date(year, month, 1)
           end =   date(year, month, last_day)
           delta=(end-start) 
           nb_days = delta.days + 1 
           rng = pd.date_range(start, periods=nb_days, freq='D')          
           df['datetime'] = rng
           df.index = df['datetime']
           tmp_tmin.append(df)
           
     tmp_tmin = pd.concat(tmp_tmin) 
     df = pd.DataFrame({'datetime': tmp_tmin['datetime'], variable: tmp_tmin.iloc[:,0].values}, columns = ['datetime',variable]) 
     df.index = df['datetime']
     df = df.drop(["datetime"], axis=1)
     
     
     return df, df_station

