import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits

#read in the vac file
vac = fits.open('manga_firefly-v2_4_3.fits') 

#plate and ifu ID of the galaxy
plate = 8247
ifu = 9102

#choose the quantity to make the map, could be changed to other properties for which the extension names are listed in the data model  
prop = 'STELLAR_MASS_VORONOI'

binid = vac[5].data
basic = vac[1].data
galid = (basic['plate']==plate)&(basic['ifudsgn']==str(ifu))
mass = vac[prop].data[galid,:,0][0]
bin1d = vac[4].data[galid,:,0][0]
image_sz = 76
maps = np.zeros((image_sz,image_sz))-99
for i in range(image_sz):
 for j in range(image_sz):
   idbin = (bin1d==binid[galid,i,j])
   if len(bin1d[idbin])==1:
    maps[i,j] = mass[idbin]

#only show the spaxels with non-empty values
masked_array = np.ma.array(maps,mask=(maps<-10))

#colour scheme for the colour bar
cmap = matplotlib.cm.jet
cmap.set_bad('white',1.)

#plot the map 
f = plt.imshow(masked_array,interpolation='nearest',cmap='RdYlBu_r',origin='lower')

plt.minorticks_on()
plt.tick_params(length=10, width=1, which='major')
plt.tick_params(length=5, width=1, which='minor')
plt.xlabel(r"spaxels",fontsize=24) # this should read spaxels, not arcseconds 
plt.ylabel(r"spaxels",fontsize=24) # 

#plot the colour bar
cbar = plt.colorbar(f,fraction=0.15,shrink=0.9)
cbar.set_label(prop,fontsize=18, rotation=270, labelpad=20)
cbar.ax.tick_params(labelsize=22)

plt.tight_layout()
plt.show()
