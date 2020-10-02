import os
import datetime as dt  # Python standard library datetime  module
import numpy as np
#from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import netCDF4
import matplotlib
import matplotlib.pyplot as plt



for file in os.listdir("../../NetCDF"):
 if file.endswith(".nc"):
  
  ncfile = os.path.join("../../NetCDF", file)
  print("Filename: " + ncfile)
  f = netCDF4.Dataset(ncfile)

  lat, lon = f.variables['XLAT'], f.variables['XLONG']

  latvals = lat[:]; lonvals = lon[:]


  # a function to find the index of the point closest pt
  # (in squared distance) to give lat/lon value.
  def getclosest_ij(lats,lons,latpt,lonpt):
   # find squared distance of every point on grid
   dist_sq = (lats-latpt)**2 + (lons-lonpt)**2
   # 1D index of minimum dist_sq element
   minindex_flattened = dist_sq.argmin()

   # Get 2D index for latvals and lonvals arrays from 1D index
   return np.unravel_index(minindex_flattened, lats.shape)
 
  iy_min, ix_min = getclosest_ij(latvals, lonvals, 42.33, -72)



  print(f.variables.keys()) # get all variable namesnde

  invalid_dimension = ['XLONG','Time','XLAT','XTIME','height','Times']

  for feature in f.variables:
   if feature in invalid_dimension:
    continue
   print(feature)
   vals = f.variables[feature]
   print(vals)
   print(vals.shape)
   print("units: " + vals.units)
   if feature == 'U' or feature == 'V':
    print(vals[0,:,iy_min,ix_min])
   else:
    print(vals[:,iy_min,ix_min])
    
