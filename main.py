# -*- coding: utf-8 -*-
from crossover_analysis import Crossover_Analysis
from avalanche_probability_analysis import Avalanche_Probability_Analysis
from height_analysis import Height_Analysis
import matplotlib.pyplot as plt
from run_oslo import run_oslo
from helper import latexfigure

latexfigure(0.5) # for plotting latex figures

L = [8, 16, 32, 64, 128, 256]
N = 100000
p = 0.5


heights_data, recurrent_h_data, recurrent_s_data, t_c_data, t_c_th_data = run_oslo('cpp', N, L, p)

c = Crossover_Analysis(L=L, N=N, h_data=heights_data, t_c_data=t_c_data, t_c_th_data=t_c_th_data)
c.plot_heights()
c.plot_t_c()

#L = [8, 16, 32, 64, 128, 256]
#N = 1000000
#p = 0.5
#
#heights_data, recurrent_h_data, recurrent_s_data, t_c_data, t_c_th_data = run_oslo('cpp', N, L, p)
#
#a = Avalanche_Probability_Analysis(L=L, N=N, t_s=1.55, 
#                                   D=2.25, a=1.2, recurrent_s_data=recurrent_s_data)
#a.plot_log_binned_pdf()
#a.plot_pdf()
#a.plot_moments()
#
#h = Height_Analysis(L=L, N=N, recurrent_h_data=recurrent_h_data)
#h.plot_sd()
#h.plot_scaling_correction()
#h.plot_height_probability()

plt.show()