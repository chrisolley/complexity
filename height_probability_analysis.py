# -*- coding: utf-8 -*-
import oslo as oslo
import matplotlib.pyplot as plt

L = [32, 64, 128]

# array of system objects for different sizes
systems = [oslo.System(l) for l in L]
# array of system iterators for each of the system objects
systemiterators = [oslo.SystemIterator(s) for s in systems]

prob_dist = [s.height_prob_dist for s in systemiterators]

fig1, ax1 = plt.subplots()

for i, p in enumerate(prob_dist): 
    ax1.plot(range(int(min(systemiterators[i].recurrent_h)), int(max(systemiterators[i].recurrent_h))), 
             p, label='L: {}'.format(L[i]))

ax1.grid()
ax1.legend(loc='best')
plt.show()