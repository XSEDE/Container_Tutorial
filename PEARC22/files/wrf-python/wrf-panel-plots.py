import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import cartopy.feature as cfeature
from netCDF4 import Dataset

from wrf import (getvar, to_np, vertcross, smooth2d, CoordPair, GeoBounds,
                 get_cartopy, latlon_coords, cartopy_xlim, cartopy_ylim)

# Open the NetCDF file
ncfile = Dataset("/Users/smarru/code-repo/sandbox/wrf-python/wrfout_d01_2016-10-07_00_00_00_subset.nc")

# Get the WRF variables
slp = getvar(ncfile, "slp")
smooth_slp = smooth2d(slp, 3)
ctt = getvar(ncfile, "ctt")
z = getvar(ncfile, "z")
dbz = getvar(ncfile, "dbz")
Z = 10**(dbz/10.)
wspd =  getvar(ncfile, "wspd_wdir", units="kt")[0,:]

# Set the start point and end point for the cross section
start_point = CoordPair(lat=26.76, lon=-80.0)
end_point = CoordPair(lat=26.76, lon=-77.8)

# Compute the vertical cross-section interpolation.  Also, include the
# lat/lon points along the cross-section in the metadata by setting latlon
# to True.
z_cross = vertcross(Z, z, wrfin=ncfile, start_point=start_point,
                    end_point=end_point, latlon=True, meta=True)
wspd_cross = vertcross(wspd, z, wrfin=ncfile, start_point=start_point,
                       end_point=end_point, latlon=True, meta=True)
dbz_cross = 10.0 * np.log10(z_cross)

# Get the lat/lon points
lats, lons = latlon_coords(slp)

# Get the cartopy projection object
cart_proj = get_cartopy(slp)

# Create a figure that will have 3 subplots
fig = plt.figure(figsize=(12,9))
ax_ctt = fig.add_subplot(1,2,1,projection=cart_proj)
ax_wspd = fig.add_subplot(2,2,2)
ax_dbz = fig.add_subplot(2,2,4)

# Download and create the states, land, and oceans using cartopy features
states = cfeature.NaturalEarthFeature(category='cultural', scale='50m',
                                      facecolor='none',
                                      name='admin_1_states_provinces_shp')
land = cfeature.NaturalEarthFeature(category='physical', name='land',
                                    scale='50m',
                                    facecolor=cfeature.COLORS['land'])
ocean = cfeature.NaturalEarthFeature(category='physical', name='ocean',
                                     scale='50m',
                                     facecolor=cfeature.COLORS['water'])

# Make the pressure contours
contour_levels = [960, 965, 970, 975, 980, 990]
c1 = ax_ctt.contour(lons, lats, to_np(smooth_slp), levels=contour_levels,
                    colors="white", transform=crs.PlateCarree(), zorder=3,
                    linewidths=1.0)

# Create the filled cloud top temperature contours
contour_levels = [-80.0, -70.0, -60, -50, -40, -30, -20, -10, 0, 10]
ctt_contours = ax_ctt.contourf(to_np(lons), to_np(lats), to_np(ctt),
                               contour_levels, cmap=get_cmap("Greys"),
                               transform=crs.PlateCarree(), zorder=2)

ax_ctt.plot([start_point.lon, end_point.lon],
            [start_point.lat, end_point.lat], color="yellow", marker="o",
            transform=crs.PlateCarree(), zorder=3)

# Create the color bar for cloud top temperature
cb_ctt = fig.colorbar(ctt_contours, ax=ax_ctt, shrink=.60)
cb_ctt.ax.tick_params(labelsize=5)

# Draw the oceans, land, and states
ax_ctt.add_feature(ocean)
ax_ctt.add_feature(land)
ax_ctt.add_feature(states, linewidth=.5, edgecolor="black")

# Crop the domain to the region around the hurricane
hur_bounds = GeoBounds(CoordPair(lat=np.amin(to_np(lats)), lon=-85.0),
                       CoordPair(lat=30.0, lon=-72.0))
ax_ctt.set_xlim(cartopy_xlim(ctt, geobounds=hur_bounds))
ax_ctt.set_ylim(cartopy_ylim(ctt, geobounds=hur_bounds))
ax_ctt.gridlines(color="white", linestyle="dotted")

# Make the contour plot for wind speed
wspd_contours = ax_wspd.contourf(to_np(wspd_cross), cmap=get_cmap("jet"))
# Add the color bar
cb_wspd = fig.colorbar(wspd_contours, ax=ax_wspd)
cb_wspd.ax.tick_params(labelsize=5)

# Make the contour plot for dbz
levels = [5 + 5*n for n in range(15)]
dbz_contours = ax_dbz.contourf(to_np(dbz_cross), levels=levels,
                               cmap=get_cmap("jet"))
cb_dbz = fig.colorbar(dbz_contours, ax=ax_dbz)
cb_dbz.ax.tick_params(labelsize=5)

# Set the x-ticks to use latitude and longitude labels
coord_pairs = to_np(dbz_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in to_np(coord_pairs)]
ax_wspd.set_xticks(x_ticks[::20])
ax_wspd.set_xticklabels([], rotation=45)
ax_dbz.set_xticks(x_ticks[::20])
ax_dbz.set_xticklabels(x_labels[::20], rotation=45, fontsize=4)

# Set the y-ticks to be height
vert_vals = to_np(dbz_cross.coords["vertical"])
v_ticks = np.arange(vert_vals.shape[0])
ax_wspd.set_yticks(v_ticks[::20])
ax_wspd.set_yticklabels(vert_vals[::20], fontsize=4)
ax_dbz.set_yticks(v_ticks[::20])
ax_dbz.set_yticklabels(vert_vals[::20], fontsize=4)

# Set the x-axis and  y-axis labels
ax_dbz.set_xlabel("Latitude, Longitude", fontsize=5)
ax_wspd.set_ylabel("Height (m)", fontsize=5)
ax_dbz.set_ylabel("Height (m)", fontsize=5)

# Add a title
ax_ctt.set_title("Cloud Top Temperature (degC)", {"fontsize" : 7})
ax_wspd.set_title("Cross-Section of Wind Speed (kt)", {"fontsize" : 7})
ax_dbz.set_title("Cross-Section of Reflectivity (dBZ)", {"fontsize" : 7})

plt.show()
