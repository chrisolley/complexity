In this report, the Oslo model is used to investigate the emergence of scale free invariance in self-organised, critical systems. The system height around the crossover time $t_c$ is shown to scale across system sizes through a data collapse, which is motivated by theoretical arguments. Corrections to scaling are explored and shown to be present in the numerical data for the average steady state height $\langle{h}\rangle$. Probability distributions for the steady state height and avalanche sizes are examined and also shown to collapse to scaling functions, with corrections to scaling for smaller systems. In the case of the avalanche size probability distribution, the critical exponents for the scaling function are estimated using both a data collapse and moment analysis methods which are shown to give similar results.


This report implemented the oslo model in two ways: 
1) as an object oriented Python model 
2) as a c++ model that is used for a significant speed up in simulation time. 
It should be noted that the c++ model was fairly buggy and might only work after multiple attempts and restarting the kernel. Furthermore there may be some compatibility issues as the C++ model failed to run on certain systems, and was most effective when run using the ipython console. However, the Python model has no known bugs. 

The number of iterations run for in the report was usually 10^7, however this takes 2-3 mins using the c++ script and 10^6 took around 10s.
However using the python model is much slower and would typically take around 2 hours to carry out all of the plots in main.py.

main.py is the script to run to produce the main simulations/plots of the project. Hence this is the script that is primarily explained in this file, as comments in the code for the other scripts should make their function clear.

Variables used: mode: 'cpp' or 'python', N: number of iterations, L: array of system sizes for which to run the model, p: probabilty of setting threshold gradients to 1.

run_oslo(mode, N, L, P): Runs the oslo model for a single run.

run_oslo_multi(mode, M, N, L, P): Runs the oslo model M times.

Avalanche_Probability_Analysis: Creates an object for avalanche probability distribution analysis.
Avalanche_Probability_Analysis.log_binned_pdf(): plots log binned avalanche probability distribution.
Avalanche_Probability_Analysis.plot_pdf(): plots unbinned avalanche size probability distribution.
Avalanche_Probability_Analysis.plot_moments(): plots moments of avalanche size pdf and carries out moment analysis/critical exponent estimation.

Avalanche_Probability_Analysis_Multi: Creates an object for avalanche probability distribution analysis over multiple runs.
Avalanche_Probability_Analysis_Multi.exponents_multi(): carries out critical exponent estimation to find mean t_s, D and std.

Height_Analysis: Creates an object for height corrections to scaling/probability distribution analysis. 
Height_Analysis.plot_sd(): plots relation between height std and system size.
Height_Analysis.plot_scaling_correction(): carries out scaling correction analysis and plots results.
Height_Analysis.plot_height_probability(): plots system height pdfs and data collapse.

Height_Analysis_Multi: Creates an object for height corrections to scaling/probability distribution analysis over multiple runs.
Height_Analysis_Multi.plot_mean_multi(): plots relation between average height and system size.
Height_Analysis_Multi.plot_sd_multi(): plots relation between average height std and system size.
Height_Analysis_Multi.plot_scaling_correction_multi(): carries out scaling correction analysis and plots results.

Crossover_Analysis: Creates an object for analysing the crossover time and plotting basic time series of system height.
Crossover_Analysis.plot_heights(): plots time series of heights.
Crossover_Analysis.plot_t_c(): plots t_c for different system sizes.

Crossover_Analysis_Multi: Creates an object for analysing the crossover time and plotting basic time series of system height over multiple runs.
Crossover_Analysis_Multi.plot_t_c_multi(): plots mean t_c for different system sizes and std.

