# -*- coding: utf-8 -*-
"""
Example tidal:
used to solve the issue #4 on bitbucket
"""

import numpy as np

from dtocean_hydro import start_logging
from dtocean_hydro.input import WP2_SiteData, WP2_MachineData, WP2input
from dtocean_hydro.main import WP2

# input data generated by Mat Topper
# and posted in bitbubket issue #4
# Setup
x = np.linspace(0.,1000.,75)
y = np.linspace(0.,300.,11) 
X, Y = np.meshgrid(x,y)
Z = -X * 0.1 - 1
G = X * 0. + 0.003
xyz = np.vstack((X.ravel(),Y.ravel(),Z.ravel())).T
geoxyz = np.vstack((X.ravel(),Y.ravel(),G.ravel())).T

# Machine data
X = np.array([   0.        ,   0.1010101 ,   0.2020202 ,   0.3030303 ,
                 0.4040404 ,   0.50505051,   0.60606061,   0.70707071,
                 0.80808081,   0.90909091,   1.01010101,   1.11111111,
                 1.21212121,   1.31313131,   1.41414141,   1.51515152,
                 1.61616162,   1.71717172,   1.81818182,   1.91919192,
                 2.02020202,   2.12121212,   2.22222222,   2.32323232,
                 2.42424242,   2.52525253,   2.62626263,   2.72727273,
                 2.82828283,   2.92929293,   3.03030303,   3.13131313,
                 3.23232323,   3.33333333,   3.43434343,   3.53535354,
                 3.63636364,   3.73737374,   3.83838384,   3.93939394,
                 4.04040404,   4.14141414,   4.24242424,   4.34343434,
                 4.44444444,   4.54545455,   4.64646465,   4.74747475,
                 4.84848485,   4.94949495,   5.05050505,   5.15151515,
                 5.25252525,   5.35353535,   5.45454545,   5.55555556,
                 5.65656566,   5.75757576,   5.85858586,   5.95959596,
                 6.06060606,   6.16161616,   6.26262626,   6.36363636,
                 6.46464646,   6.56565657,   6.66666667,   6.76767677,
                 6.86868687,   6.96969697,   7.07070707,   7.17171717,
                 7.27272727,   7.37373737,   7.47474747,   7.57575758,
                 7.67676768,   7.77777778,   7.87878788,   7.97979798,
                 8.08080808,   8.18181818,   8.28282828,   8.38383838,
                 8.48484848,   8.58585859,   8.68686869,   8.78787879,
                 8.88888889,   8.98989899,   9.09090909,   9.19191919,
                 9.29292929,   9.39393939,   9.49494949,   9.5959596 ,
                 9.6969697 ,   9.7979798 ,   9.8989899 ,   10.          ])

Cp = np.array([ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
                0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
                0.00248182,  0.0273    ,  0.05211818,  0.07693636,  0.10175455,
                0.12657273,  0.15139091,  0.17620909,  0.20102727,  0.22584545,
                0.25066364,  0.27548182,  0.3003    ,  0.32511818,  0.34993636,
                0.37475455,  0.39957273,  0.42439091,  0.44920909,  0.47402727,
                0.49884545,  0.52366364,  0.54848182,  0.5733    ,  0.59811818,
                0.62293636,  0.64775455,  0.67257273,  0.69739091,  0.72220909,
                0.74702727,  0.77184545,  0.79666364,  0.82148182,  0.8463    ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      ,
                0.86      ,  0.86      ,  0.86      ,  0.86      ,  0.86      
             ])

p = np.array([1.])
nx = len(x)
ny = len(y)
N = len(p)
TI = np.array([0.1])
V = 1.*np.ones((ny,nx,N))
U = 2.*np.ones((ny,nx,N))
SSH = 3.0*np.ones((N))
tide_matrix = {'V':V,'U':U,'p':p,'TI':TI,'x':x,'y':y,'SSH':SSH} 

bathymetry = xyz #np.array([-60.]) 
geophysics = geoxyz #np.array([0.003])
lease_area = np.array([[50., 50.],[950., 50.],[950., 250.],[50., 250.]],dtype=float)
power_law_exponent = np.array([7.])
nogo_areas = [np.array([[0, 0],[.1, 0],[.1, .1],[0, .1]])]
rated_array_power = 10
main_direction = None
blockage_ratio = 1.
tidal_matrix_farm = tide_matrix
lCS = np.array([0, 0., 20.])
performance_velocity = X
Cp_curve = Cp
Ct_curve = 0.4*np.ones((100))
user_array_option = 'rectangular'
user_array_layout = None 
rotor_diam = 8.
turbine_interdist = 20.
float_flag = False
min_install = -np.inf
max_install = 0.
min_dist_x = 40.
min_dist_y = 40.
bidirection = False
rated_power_device = 1
op_threshold = 0
yaw_angle = 0./180*np.pi
cut_in = 1.
cut_out = 4.
# end of inputs


# Start the logging system
start_logging()

Site = WP2_SiteData(lease_area,
                    nogo_areas,
                    tidal_matrix_farm,
                    power_law_exponent,
                    main_direction,
                    bathymetry,
                    geophysics,
                    blockage_ratio) 

y = np.empty((1))
z = np.empty((1))
c_io = np.array([cut_in, cut_out])

single_machine_description = {'pf':Cp_curve,'Lf2':bidirection,'Lf1':Ct_curve,'x':performance_velocity,'y':y,'z':z,'Add':c_io}                    

                   
Machine = WP2_MachineData('tidal',
                          lCS,
                          (rotor_diam, turbine_interdist),
                          yaw_angle,
                          single_machine_description,
                          float_flag,
                          (min_install, max_install),
                          (min_dist_x, min_dist_y),
                          op_threshold,
                          {'Option':1,'Value':user_array_option},
                          rated_array_power,
                          rated_power_device,
                          user_array_layout)


" Input assembly "
iWP2input = WP2input(Machine,Site)

if not iWP2input.stopWP2run:
    WPobj = WP2(iWP2input,debug=True)
    #Out = WPobj.optimisationLoop(FixedLayOut=FixedArrayLayout)
    Out = WPobj.optimisationLoop()
    Out.printRes()
