import numpy as np
import matplotlib.pyplot as plt
from AMoption import Option
from underlying import Underlying
from payoffs import *


n = 10000
T = 0.5
sigma1 = 0.4
sigma2 = 0.3
r = 0.06
N = 250
spot1 = 100
spot2 = 110
K1 = 100
K2 = 110

Aktywo = Underlying(spot_price=spot1, r=r)  # Aktywo = Underlying(100)
Aktywo.calibrate_GBM(sigma=sigma1, values_per_year_GBM=N)  # Aktywo.calibrate_GBM(0.3,0.07)

Aktywo2 = Underlying(spot_price=spot2, r=r)  # Aktywo = Underlying(100)
Aktywo2.calibrate_GBM(sigma=sigma2, values_per_year_GBM=N)  # Aktywo.calibrate_GBM(0.3,0.07)

Opcja = Option(underlyings=(Aktywo, Aktywo2), payoff_func=lambda traj: Double_Call_Payoff(traj, K1,K2), T=T)
Opcja2 = Option(underlyings=(Aktywo,Aktywo2), payoff_func=lambda traj: multiple_call_payoff(traj, [K1, K2]), T=T)
Opcja3 = Option(underlyings=Aktywo,  payoff_func=lambda traj: payoff_creator_1d(traj, Call_Payoff, path_dependent=True,
                                                                                pd_type='asian', K=K1), T=T)
Opcja4 = Option(underlyings=(Aktywo,Aktywo2), payoff_func=lambda traj: multiple_mixed_payoff(traj, [K1, K2],
                                                                                             ['call', 'put']), T=T)
#Options = [Opcja, Opcja2, Opcja3, Opcja4, Opcja5, Opcja6, Opcja7, Opcja8, Opcja9, Opcja10, Opcja11, Opcja12, Opcja13, Opcja14]
    #types = ['call', 'put', 'asian call', 'geometric asian', 'asian strike call', 'geometric asian strike call', 'lookback minimum call',
    #         'lookback max call', 'up-and-out call (140)', 'up and in call(140)', ]


def price_compare(option, n):
    print(option.payoff_func.__name__)
    print('State stace partitioning price:')
    print(option.ssp(n_sims=n))
    print('Upper estimate ssp:')
    print(option.upper_bound_price_ssp)
    print('LS price:')
    print(option.LS(n))
    print('European price:')
    print(option.european())


price_compare(Opcja, n)

price_compare(Opcja2, n)
Opcja2.ssp(n)
Opcja2.LS(n)
Opcja2.european()


asset1 = Underlying(spot_price=100, r=0.07)
asset1.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)
asset1.calibrate_JD(sigma=0.4, jump_intensity=1 / 3)
asset2 = Underlying(spot_price=120, r=0.07)
asset2.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)
asset2.calibrate_JD(sigma=0.2, jump_intensity=1 / 2)

option_3dim = Option((asset1, asset2, Aktywo), payoff_func=lambda traj: multiple_mixed_payoff(traj, 100,payoff_type=['put','put','put'], which ='min'), T=1)
option_4dim = Option((asset1, asset2, Aktywo, Aktywo2), payoff_func=lambda traj: multiple_put_payoff(traj, 100), T=1)



option_3dim.ssp(n)

option = Option(underlyings=asset1,
                payoff_func=lambda trajectory: payoff_creator_1d(trajectory, Call_Payoff, K=100, barrier=True,
                                                                 barrier_level=140), T=1)
print(option.ssp(10000, mode='JD'))
# 20.33463726670842 z permutacją 11s, 20.536608834016505
print(option.LS(10000, mode='JD'))


# 20.92430225200415 15s, 20.65867517809142

option = Option(underlyings=(asset1, asset2), payoff_func=lambda trajectories: double_max_put(trajectories, 100), T=1)
option.european(10000)
option.ssp(10000, 'JD')
option.LS(10000, 'JD')





# Calculate the median along each axis
#median_axis0 = np.quantile(arr, [0.25, 0.5, 0.75], axis=0)
#median_axis1 = np.quantile(arr, [0.25, 0.5, 0.75], axis=1)

# Create scatter plot
##x = np.arange(arr.shape[1])
#y = np.arange(arr.shape[0])

#fig, ax = plt.subplots()
#ax.scatter(x, median_axis0, label='Median along Axis 0')
#ax.scatter(median_axis1, y, label='Median along Axis 1')
#ax.legend()
#ax.set_xlabel('Index')
#x.set_ylabel('Value')
#ax.set_title('Quantiles in 2-Dimensional Array')
#plt.show()
