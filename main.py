# -*- coding: utf-8 -*-
from crossover_analysis import Crossover_Analysis, Crossover_Analysis_Multi
from avalanche_probability_analysis import Avalanche_Probability_Analysis, Avalanche_Probability_Analysis_Multi
from height_analysis import Height_Analysis, Height_Analysis_Multi
import matplotlib.pyplot as plt
from run_oslo import run_oslo, run_oslo_multi
from helper import latexfigure

latexfigure(0.5) # for plotting latex figures

L = [8, 16, 32, 64, 128, 256]
N = 100000
p = 0.5
M = 5

heights_data, recurrent_h_data, recurrent_s_data, t_c_data, t_c_th_data = run_oslo('cpp', N, L, p)
height_mean_multi, height_sd_multi, t_c_multi, t_c_th_multi, s_data_multi = run_oslo_multi('cpp', M, N, L, p)

c = Crossover_Analysis(L=L, N=N, h_data=heights_data, t_c_data=t_c_data, t_c_th_data=t_c_th_data)
c.plot_heights() # plots time series of heights
c.plot_t_c() # plots t_c for different system sizes

c_m = Crossover_Analysis_Multi(L, t_c_multi, t_c_th_multi)
c_m.plot_t_c_multi() # plots mean t_c for different system sizes and std 

L = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
N = 1000000
p = 0.5
M = 10

heights_data, recurrent_h_data, recurrent_s_data, t_c_data, t_c_th_data = run_oslo('cpp', N, L, p)
height_mean_multi, height_sd_multi, t_c_multi, t_c_th_multi, s_data_multi = run_oslo_multi('cpp', M, N, L, p)

a = Avalanche_Probability_Analysis(L=L, N=N, t_s=1.55, 
                                   D=2.25, a=1.2, recurrent_s_data=recurrent_s_data)
a.plot_log_binned_pdf() # plots log binned avalanche probability distribution
a.plot_pdf() # plots unbinned avalanche size probability distribution
a.plot_moments() # plots moments of avalanche size pdf and carries out moment analysis/critical exponent estimation

a_m = Avalanche_Probability_Analysis_Multi(L, s_data_multi)
a_m.exponents_multi() # carries out critical exponent estimation to find mean t_s, D and std

h = Height_Analysis(L=L, N=N, recurrent_h_data=recurrent_h_data)
h.plot_sd() # plots relation between height std and system size
h.plot_scaling_correction() # carries out scaling correction analysis and plots results
h.plot_height_probability() # plots system height pdfs and data collapse

h_m = Height_Analysis_Multi(L, height_mean_multi, height_sd_multi)
h_m.plot_mean_multi() # plots relation between average height and system size
h_m.plot_sd_multi() # plots relation between average height std and system size.
h_m.plot_scaling_correction_multi() # carries out scaling correction analysis and plots results

plt.tight_layout()
plt.show()