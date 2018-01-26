# -*- coding: utf-8 -*-
import oslo as oslo
import matplotlib.pyplot as plt

N = 6000
L = range(2,33)

# array of system objects for different sizes
systems = [oslo.System(l, N) for l in L]
# array of system iterators for each of the system objects
systemiterators = [oslo.SystemIterator(s) for s in systems]
fig1, ax1 = plt.subplots()
t_c = [s.t_c for s in systems]
t_c_theory = [s.t_c_theory for s in systemiterators]

ax1.plot(L, t_c, label = 'Observed')
ax1.plot(L, t_c_theory, label = 'Theory', color = 'red', linestyle = '--')
ax1.set_xlabel('System Size, L')
ax1.set_ylabel('Cross-over time, t_c')
ax1.legend(loc='best')
ax1.grid()
    
plt.show()
