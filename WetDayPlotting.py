import xarray
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
from matplotlib import colors as clr
import matplotlib.transforms as mtransforms
from cartopy.util import add_cyclic_point

#this function defines the colourbar
def inter_from_256(x):
    return np.interp(x=x,xp=[0,255],fp=[0,1])

cdict = {
    'red':((0.0,inter_from_256(64),inter_from_256(64)),
            (1/5*1,inter_from_256(102),inter_from_256(102)),
            (1/5*2,inter_from_256(235),inter_from_256(235)),
            (1/5*3,inter_from_256(253),inter_from_256(253)),
            (1/5*4,inter_from_256(244),inter_from_256(244)),
            (1.0,inter_from_256(169),inter_from_256(169))),
    'green': ((0.0, inter_from_256(57), inter_from_256(57)),
            (1 / 5 * 1, inter_from_256(178), inter_from_256(178)),
            (1 / 5 * 2, inter_from_256(240), inter_from_256(240)),
            (1 / 5 * 3, inter_from_256(219), inter_from_256(219)),
            (1 / 5 * 4, inter_from_256(109), inter_from_256(109)),
            (1 / 5 * 5, inter_from_256(23), inter_from_256(23))),
    'blue': ((0.0, inter_from_256(144), inter_from_256(144)),
              (1 / 5 * 1, inter_from_256(255), inter_from_256(255)),
              (1 / 5 * 2, inter_from_256(185), inter_from_256(185)),
              (1 / 5 * 3, inter_from_256(127), inter_from_256(127)),
              (1 / 5 * 4, inter_from_256(69), inter_from_256(69)),
              (1.0, inter_from_256(69), inter_from_256(69))),
}
cmap = clr.LinearSegmentedColormap('new_cmap',segmentdata=cdict,N = 20)
colors = cmap(np.linspace(0, 1, 100))

#loading in wet day frequency data for subplot 1
infile= xarray.open_dataset('D:/Precipitation/1980_2019_total_precipitation_masked.nc')

#loading in wet day percentile data for subplot 2
dist = np.load('D:/Precipitation/total_precipitation_distribution.npy')
dist_arr = np.asarray(dist)
dist_arr  = np.multiply(dist_arr,1000) #converts from m to mm.
 


##PLOTTING##

#Defining the figure size
fig = plt.figure(figsize=(13,15))
fig.subplots_adjust(top=0.975)

#setting axes and labels for subplot 1
ax = plt.subplot(2,1,1,projection=ccrs.PlateCarree())
trans = mtransforms.ScaledTranslation(10/72, -5/72, fig.dpi_scale_trans)
ax.text(0.0, 1.0, 'a.', transform=ax.transAxes + trans,
            fontsize='large', verticalalignment='top', fontfamily='sans-serif', weight = 'bold',color = 'black',
            bbox=dict(facecolor='white', edgecolor='none', pad=1.0))
ax.coastlines()

ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())

#Plotting
plt.xlabel('Longitude',fontsize='15')
plt.ylabel('Latitude',fontsize='15')
tp, longitude = add_cyclic_point(infile.tp,infile.longitude) #connects the two ends of the longitude array
cont = plt.contourf(longitude,infile.latitude,tp,levels = 20,cmap = cmap,vmin = 0,vmax = 100)


#setting axes and labels for subplot 2
ax = plt.subplot(2,1,2)
trans = mtransforms.ScaledTranslation(10/72, -5/72, fig.dpi_scale_trans)
ax.text(0.0, 1.0, 'b.', transform=ax.transAxes + trans,
            fontsize='large', verticalalignment='top', fontfamily='sans-serif', weight = 'bold',
            bbox=dict(facecolor='none', edgecolor='none', pad=3.0))

for ind,d in enumerate(dist_arr[0:100,:]):  
    if str(type(d)) == "<class 'float'>": #this statement ignores data that doesn't exist. 
        None
    else:
         plt.plot(d,np.arange(0,100,1),'.', color = colors[ind])

#labelling figure and setting scaling and limits
plt.ylabel('Percentile',fontsize = 15)
plt.xlabel('Cumulative precipitation (mm/hr)',fontsize = 15) 
plt.yticks([1,10,25,50,75,90,99])
plt.grid(ls = "--",color = 'k', alpha = 0.5)
plt.xscale("log")
plt.xlim(0.04, 10)
plt.xticks([0.04,0.1,1,10,100], labels = [0.04,0.1,1,10,100])#,fontsize = 14)

#adding the colourbar
cmap = plt.get_cmap(cmap,20)
norm = mpl.colors.Normalize(vmin=0,vmax=100)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar_ax = fig.add_axes([0.94, 0.25, 0.02, 0.55])
clbar = fig.colorbar(sm,cax=cbar_ax)
clbar.set_label("Wet-day frequency (%)",fontsize='16')

#saving
#plt.savefig('D:/Precipitation/Plots/Figure1',dpi = 400,bbox_inches = "tight")  