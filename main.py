# -*- coding: utf-8 -*-
from crossover_analysis import Crossover_Analysis
from avalanche_probability_analysis import Avalanche_Probability_Analysis
from height_analysis import Height_Analysis
import matplotlib.pyplot as plt
#
#c = Crossover_Analysis(L=[8, 16, 32, 64], N=10**4)
#c.plot_heights()
#c.plot_t_c()

#a = Avalanche_Probability_Analysis(L=[8, 16, 32, 64, 128, 256], N=10**6, t_s=1.55, 
#                                   D=2.25, a=1.2, use_data=True)
#a.plot_log_binned_pdf()
#a.plot_pdf()

h = Height_Analysis(L=[8, 16, 32, 64, 128, 256], N=10**5, use_data=True)
h.plot_sd()
h.plot_scaling_correction()
h.plot_height_probability()

plt.show()