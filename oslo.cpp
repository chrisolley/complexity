#include "stdafx.h"
#include <stdlib.h>     /* srand, rand */
#include <iostream>
#include <time.h>
#include <math.h>
using namespace std;

int set_thr(double p){
	double r = (float)rand() / (float)RAND_MAX;
	if (r < p){
		return 1;
	}
	else{
		return 2;
	}
}


extern "C" __declspec(dllexport) void oslo(int N, int L, double p, int *t_c, double *t_c_theory, int *h, int *zth, int *heights, int *avalanche_sizes)
{
	bool recurrent = false;
	srand(time(NULL));
	for (int i = 0; i < L; i++){
		zth[i] = set_thr(p);
	}

	for (int i = 0; i < N; i++){
		h[0] += 1; //drive phase
		bool relax = true; //relaxation phase 
		int s = 0;
		while (relax == true){
			relax = false;
			for (int j = 0; j < L; j++){
				int z = h[j] - h[j + 1];
				if (z > zth[j]){
					if (j < L - 1){
						h[j] -= 1;
						h[j + 1] += 1;
					}
					else{
						h[j] -= 1;
						if (recurrent == false){
							t_c[0] = i;
							recurrent = true;
						}
					}
					s += 1;
					zth[j] = set_thr(p);
					relax = true;
				}
			}
		}
		avalanche_sizes[i] = s;
		heights[i] = h[0];
	}
	double z_mean = (double)h[0] / (double)L;
	t_c_theory[0] = (z_mean / 2) * pow(L, 2.0) * (1.0 + (1.0 / L));

}

