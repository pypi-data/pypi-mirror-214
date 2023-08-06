from underlying import Underlying
from AMoption import Option
import numpy as np
from payoffs import *
n_bins = 100
T = 1
n_sims=10000

asset = Underlying(spot_price=100, r=0.06)
asset.calibrate_GBM(0.3,50)
option = Option(asset, payoff_func = lambda traj: payoff_creator_1d(traj, Call_Payoff, K=100, barrier=True, barrier_type='up-and-in',barrier_level=110), T = 1)
paths = asset.simulate(mode='GBM', size=10000, T=T).to_numpy()

if mode == "GBM":
    values_per_year = asset.values_per_year_GBM
elif mode == "Bootstrap":
    values_per_year = asset.values_per_year_Bootstrap
elif mode == "JD":
    values_per_year = asset.values_per_year_JD
else:
    raise Exception(
        'Longstaff-Schwartz method (LS) is supported only for GBM, JD and Boostrapping at this moment')

ti = round(values_per_year * T)
disc = np.exp(- asset.r * T / ti)

exercise = np.zeros((n_sims, ti+1))
# n of paths in a bin
n_paths = int(n_sims / n_bins)
sorted_steps = np.argsort(paths, axis=0)

all_payoffs = option.payoff_func(paths)
# all_payoffs = self.payoff_func(paths)

if not asset.ssp_calibrated:
    probs_matrix = np.zeros((n_bins, n_bins, ti))

for i in tqdm(range(ti + 1)):
    i=0
    cur_bins = sorted_steps[:, ti - i]
    hi = all_payoffs[cur_bins, ti - i]
    #hi = np.mean(hi.reshape(-1, n_paths), axis=1)  # payoffy w danym kroku

    if i == 0:
        V_i = hi

    else:
        V_i1 = V_i
        next_bins = sorted_steps[:, ti - i + 1]

        if asset.ssp_calibrated:
            probs = asset.probs_matrix[:, :, ti - i]
        else:
            probs = np.zeros((n_bins, n_bins))
            for j in range(n_bins):
                list1 = cur_bins[(j * n_paths): ((j + 1) * n_paths)]
                s = 0
                for k in range(n_bins):

                    list2 = next_bins[(k * n_paths): ((k + 1) * n_paths)]
                    # print(list2)
                    res = np.intersect1d(list1, list2)
                    # res = [x == y for x, y in zip(list1, list2)]
                    # print(len(res))
                    probs[j, k] = len(res) / n_paths
                    # print(res)
                    s += len(res)
                    if s == n_paths:
                        break
            probs_matrix[:, :, ti - i] = probs

        # print(probs)
        V_i = np.maximum(hi, probs @ V_i1 * disc)
        print(V_i.shape)
        print()
    exercise[:, ti - i] = V_i <= hi
if not asset.ssp_calibrated:
    asset.probs_matrix = probs_matrix
    asset.ssp_calibrated = True

Yt = hi * np.exp(- np.tile(np.arange(0, ti + 1), (n_sims, 1)) * (T/values_per_year) * asset.r)
exercise_time = np.argmax(exercise, axis=1)
res = np.mean(Yt[np.arange(len(Yt)), exercise_time])
self.upper_bound_price_ssp = np.mean(V_i)
self.ET_ssp = exercise.astype(int)