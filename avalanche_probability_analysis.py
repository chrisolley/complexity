# -*- coding: utf-8 -*-
import oslo as oslo
import matplotlib.pyplot as plt

L = [4, 8, 16, 32, 64, 128]#    , 256]

systems = [oslo.System(l) for l in L]

systemiterators = [oslo.SystemIterator(s) for s in systems]

prob_dist = [s.s_prob_dist_log_bin for s in systemiterators]

fig1, ax1 = plt.subplots()

for i, p in enumerate(prob_dist):
    ax1.loglog(prob_dist[i][0], prob_dist[i][1], label='L: {}'.format(L[i]))
    
ax1.grid()
ax1.legend(loc='best')
plt.show()