import time
import matplotlib.pyplot as plt
from column_analysis_5.utilities import get_kernel, PoissonPopulation, IAFPSCDeltaPopulation, connect_one_to_one, SpikeMonitor, connect_nsyn 
import numpy as np
import pickle
import scipy.stats as sps

N = 10000
dt=.0001
tf=1
seed=12346
number_of_processors=4
verbose=True
NN=1

nsyn_bg = 1
bgfr = 200
weight_bg = .1
weight_recc = -.1
nsyn_recc = 20
delay = .15


neuron_params = {   "V_reset"   : 0.,
                    "tau_m"     : 50.,
                    "C_m"       : 250.,
                    "V_th"      : 1.,
                    "t_ref"     : 0.,
                    "V_m"       : 0.,
                    "E_L"       : 0.}

t0 = time.time()
for ii in range(NN):
    
    print ii
    kernel = get_kernel(dt=dt, tf=tf, seed=seed+ii, number_of_processors=number_of_processors, verbose=verbose)
    
    background_population = PoissonPopulation('bg', bgfr, N, kernel) 
    internal_population = IAFPSCDeltaPopulation('int', N, kernel, neuron_params=neuron_params)
    
    
    # for curr_gid in internal_population.gids:
    #     kernel.SetStatus([curr_gid], {'V_m': IC_dist_data['edges'][IC_dist.rvs()]})
    
    monitor = SpikeMonitor('int_m', internal_population, kernel)
    
    connect_one_to_one(background_population,internal_population, .001*weight_bg, kernel, delay=0)
    connect_nsyn(internal_population, internal_population, nsyn_recc, .001*weight_recc, kernel, delay=delay)
    
    kernel.Simulate(tf*1000)
    
    t, y = monitor.firing_rate(0, tf, .005)
    
    try:
        y_tot += y
    except:
        y_tot = y

print time.time()-t0

plt.plot(t, y_tot/NN)

plt.show()