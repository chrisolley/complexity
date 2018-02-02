# -*- coding: utf-8 -*-
import oslo as oslo
import matplotlib.pyplot as plt

#N = 10000
L = range(2,128,5)

# array of system objects for different sizes
systems = [oslo.System(l) for l in L]
# array of system iterators for each of the system objects
systemiterators = [oslo.SystemIterator(s) for s in systems]
t_c = [s.t_c for s in systems]
t_c_theory = [s.t_c_theory for s in systemiterators]

recurrent_mean_h = [s.recurrent_mean_h for s in systemiterators]
sd_h = [s.sd_h for s in systemiterators]

fig1, ax1 = plt.subplots()
ax1.plot(L, t_c, label = 'Observed')
ax1.plot(L, t_c_theory, label = 'Theory', color = 'red', linestyle = '--')
ax1.set_xlabel('System Size, L')
ax1.set_ylabel('Cross-over time, t_c')
ax1.legend(loc='best')
ax1.grid()

fig2, ax2 = plt.subplots()
ax2.plot(L, recurrent_mean_h)
ax2.set_xlabel('System Size, L')
ax2.set_ylabel('Recurrent System Average Height')
ax2.grid()

fig3, ax3 = plt.subplots()
ax3.plot(L, sd_h, linestyle='', marker='.')
ax3.set_xlabel('System Size, L')
ax3.set_ylabel('Standard Deviation of Height')
ax3.grid()

plt.show()
