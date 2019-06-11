# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:25:54 2019

@author: guillaume
"""

def plot_closed_points(*args):
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib.pylab as plt
    import numpy as np  
  
    lats = args[0]
    lons = args[1]  
    names = args[2]
    var = args[3]
    colors=['black','red','blue', 'green']
    
    fig = plt.figure(figsize=(28,16))   
    ax = plt.axes(projection=ccrs.PlateCarree())    
    ax.set_extent((lons[0] - 3, lons[0] + 3, lats[0] - 3, lats[0] + 3)) 
       
    ax.add_feature(cfeature.OCEAN.with_scale('50m'))      # couche ocean
    ax.add_feature(cfeature.LAND.with_scale('50m'))       # couche land
    ax.add_feature(cfeature.LAKES.with_scale('50m'))      # couche lac
    
    ax.add_feature(cfeature.BORDERS.with_scale('50m'))    # couche frontieres
    ax.add_feature(cfeature.RIVERS.with_scale('50m'))     # couche rivières      
    coast = cfeature.NaturalEarthFeature(category='physical', scale='10m',     # ajout de la couche cotière 
                        facecolor='none', name='coastline')
    ax.add_feature(coast, edgecolor='black')
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')
    
    ax.add_feature(states_provinces, edgecolor='gray')     
    ax.gridlines() 
    i = 0     
    for name in names:         
        ax.scatter(lons[i], lats[i], c= colors[i], s=100, label=name)
        print(lats[i])
        print(lons[i])
        i += 1       
    plt.legend(loc="best", markerscale=1., scatterpoints=1, fontsize=40)              
    # Define gridline locations and draw the lines using cartopy's built-in gridliner:
    xticks = np.arange(-150.0,-40.0,20)
    yticks =np.arange(10,80,10)     
    fig.canvas.draw()  
    
    plt.savefig('./Localisation_site_'+str(var)+'.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()  
    plt.close()