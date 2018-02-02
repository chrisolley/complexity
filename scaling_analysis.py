# -*- coding: utf-8 -*-
import oslo as oslo
import matplotlib.pyplot as plt

#N = 6000
L = [8, 16, 32, 64, 128]

# array of system objects for different sizes
systems = [oslo.System(l) for l in L]
# array of system iterators for each of the system objects
systemiterators = [oslo.SystemIterator(s) for s in systems]

fig1, ax1 = plt.subplots()
ax1.plot(range(systems[1].N), systemiterators[1].avalanche_sizes_scaled)
ax1.set_xlabel('t')
ax1.set_ylabel('s/s_max')
ax1.grid()

fig2, ax2 = plt.subplots()
ax2.grid()
fig3, ax3 = plt.subplots()
ax3.grid()
fig4, ax4 = plt.subplots()
ax4.grid()

for i, s in enumerate(systemiterators):
    ax2.plot(range(len(s.processed_height)), s.processed_height, label=L[i])
    ax2.set_xlabel('t')
    ax2.set_ylabel('h')
    ax2.legend(loc='best')
    
    ax3.plot(range(len(s.processed_height)), s.height_hist_scaled, label=L[i])
    ax3.set_xlabel('t')
    ax3.set_ylabel('h/L')
    ax3.legend(loc='best')
    
    ax4.plot(s.N_scaled, s.height_hist_scaled, label=L[i])
    ax4.set_ylabel('h/L')
    ax4.set_xlabel('t/L^2')
    ax4.legend(loc='best')
    ax4.set_xlim(0,5)

plt.show()