# -*- coding: utf-8 -*-
"""
Created on Wed May 04 16:11:29 2016

@author: francesco
"""
import numpy as np
import pickle
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import _cntr as cntr
from shapely.ops import cascaded_union
from shapely.geometry import Polygon


def get_unfeasible_regions(xyz, z_bounds, area_thr=100, g_fil=0.5, debug=False, debug_plot=False):

    xyz, z_bounds, stat = check_bathymetry_format(xyz, z_bounds)
    if stat == -1:
        errStr = ("Error[InstalDepth]:\nNo feasible installation area"
                    "has been found for the device for the given bathymetry.")
        raise ValueError(errStr)
    elif stat == 1:
        #module_logger.info("No NOGO areas related to the machine depth"
        #        "installation constraints have been found.")
        print("No NOGO areas related to the machine depth"
                "installation constraints have been found.")
        return None, False
    
    dx = np.max(xyz[1:,0]-xyz[:-1,0])
    dy = np.max(xyz[1:,1]-xyz[:-1,1])

    X, Y = get_bathymetry_grid(xyz)
    nx, ny = Y.shape
        
    unfeasible_mask = np.logical_not((xyz[:,2]>=z_bounds[0])*(xyz[:,2]<=z_bounds[1]))
                     
    # restructure the data in a 2d matrix and binarise the result
    data = unfeasible_mask.astype(np.int).reshape(nx, ny)
    label_im, labels = clustering(data, dx*dy, area_thr=area_thr, g_fil=g_fil, debug=debug)
    
    if debug: plt.figure(200), plt.imshow(label_im, cmap=plt.cm.spectral), plt.show()
    
    return get_shapely_polygons(X, Y, label_im, labels, debug=debug), unfeasible_mask 
    

def get_shapely_polygons(X, Y, label_im, labels, debug=False):
    multi_polygon = []
    false_unfeasible = []
    
    for ind_label in labels:
        data_masked = label_im*(label_im == ind_label)
        if data_masked.max() < 1:
            continue
        c = cntr.Cntr(X, Y, data_masked)
        # trace a contour at z == 0.5
        res = c.trace(0.)
        nseg = len(res) // 2
        segments, codes = res[:nseg], res[nseg:]
        del codes
        multi_polygon.append(Polygon(segments[0]))
        if not len(segments) == 1:
            for iel in range(1,len(segments)):
                false_unfeasible.append(Polygon(segments[iel]))
    
    mp = cascaded_union(multi_polygon)-cascaded_union(false_unfeasible)
    
    return mp
    
    
def clustering(im, pixel_area, area_thr=10, g_fil=0.5, debug=False):
    
    # smooth the edges of the data edges
    im = ndimage.gaussian_filter(im, g_fil)
    
    # remove small areas with zeros and small areas with ones
    open_img = ndimage.binary_opening(im)
    close_img = ndimage.binary_closing(open_img)
    
    # cluster the all the independent areas
    label_im, nb_labels = ndimage.label(close_img)
    
    # calculate the areas of each cluster
    areas = ndimage.sum(im, label_im, range(nb_labels + 1))*pixel_area  # cos each pixels has an area of dx*dy

    # remove areas based on their size and the given threshold    
    mask_size = areas < area_thr
    remove_pixel = mask_size[label_im]
    label_im[remove_pixel] = 0
    
    # cleas up the IDs and short the areas
    labels = np.unique(label_im)
    label_im = np.searchsorted(labels, label_im)
    labels = np.unique(label_im) 
    
    return label_im, labels

def get_bathymetry_grid(xyz):
    if xyz[0,0]==xyz[1,0]:
        # search in x
        index = 0
    elif xyz[0,1]==xyz[1,1]:
        # search in y
        index = 1
    old = xyz[0,index]
    ind = 0
    for ii in range(1,len(xyz)):
        if old == xyz[ii,index]:
            ind += 1
        else:
            break
    
    Y = np.reshape(xyz[:,1], (-1, ind+1))
    y = Y[0,:]
    X = np.reshape(xyz[:,0], (-1, y.shape[0]))
    
    return X, Y

def check_bathymetry_format(xyz, bound):
    status = 0  # bathymetry constraints active
    if not isinstance(xyz, np.ndarray):
        raise IOError("The data type of the bathymetry needs to be a numpy.ndarray")
    if len(xyz.shape) == 1:
        nx, ny = 1, len(xyz)
        xyz = xyz.reshape(nx,ny)
    else:
        nx, ny = xyz.shape
        
    if not (nx==3 or ny==3):
        raise IOError("The size of the bathymetry needs to be [nx3], where n is the number of datapoints")
        
    elif not ny==3:
        xyz = xyz.T
        
    if np.all(xyz[:,2] < 0):
        xyz = xyz*np.array([1,1,-1])
    
    bound = np.abs(bound).tolist()
    if bound[0] > bound[1]:
        bound = bound[::-1]
    
    # check trivial solutions
    if min(bound) == 0 and max(bound) == np.inf:  # the all area is feasible
        status = 1
    elif min(bound) == max(bound):  # none of the area is feasible
        status = -1
    else:
        unfeasible_mask = np.logical_not((xyz[:,2]>=bound[0])*(xyz[:,2]<=bound[1]))
        if np.all(unfeasible_mask):  # again none of the area is feasible
            status = -1
        elif not np.any(unfeasible_mask):  # again the all area is feasible
            status = 1
                
    return xyz, bound, status
    

if __name__ == "__main__":
    from Visualise_polygons import *
    from shapely.geometry import Point
    
    z_bounds = [0, np.inf]

    # load a test bathymetry
    xyz = pickle.load( open('bathy_test.p', 'rb') ).T
    xyz = xyz*np.array([1,1,-1],'f')
        
    # generate a random array
    test_array = np.random.rand(1000,2)*100.
    
    # test the bathymetry function
    mp, unf = get_unfeasible_regions(xyz, z_bounds, debug=True)
    mask = np.array([mp.contains(Point(xx, yy)) for xx, yy in test_array])
    
    fig, ax = plt.subplots(1, 1)
    plotCompositePolygon(mp, ax=ax)
    
    ax.plot(test_array[mask==False, 0], test_array[mask==False, 1], "rx")
    ax.plot(test_array[mask, 0], test_array[mask, 1], "ro")
    
    
    
    
