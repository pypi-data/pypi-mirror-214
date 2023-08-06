import pandas
from scipy.stats import norm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from american_options.underlying import Underlying
from scipy import interpolate, stats
from itertools import product
from operator import itemgetter
from sklearn import linear_model
import warnings
import chaospy
#from payoffs import *

class Option:
    """
    Obtain value for options using various pricing methods.

    Parameters
    ----------
    :param underlyings: Single Underlying or tuple of Underlying-s
    :param payoff_func: Payoff function that handles passed underlying/s
    :type payoff_func: function
    :param T: Time to maturity of the option
    :type T: float


    Examples
    --------
    Creation of one dimensional Option
    >>> import numpy as np
    >>> asset = Underlying(spot_price=100, r=0.06)
    >>> asset.calibrate_GBM(sigma=0.6,values_per_year_GBM=255)
    >>> option = Option(underlyings=asset, payoff_func=lambda trajectory: np.maximum(100-trajectory,0), T=1)

    Two dimensional maximum put option, based on two underlyings modelled with GBM:
    >>> irr = 0.06
    >>> N = 255
    >>> asset1 = Underlying(spot_price=100, r=irr)
    >>> asset1.calibrate_GBM(sigma=0.6, values_per_year_GBM=N)
    >>> asset2 = Underlying(spot_price=120, r=irr)
    >>> asset2.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)

    >>> def double_max_put(sims_list, K):
    >>>    return np.maximum(np.maximum(K - sims_list[0], K - sims_list[1]), 0)

    >>> option = Option(underlyings=(asset1, asset2), payoff_func=lambda trajectories: double_max_put(trajectories, 100), T=1)
    """

    def __init__(self, underlyings, payoff_func, T):
        self.ssp_representative = None
        if isinstance(underlyings, tuple):
            self.underlyings = underlyings
        else:
            self.underlyings = (underlyings,)
        self.payoff_func = payoff_func
        self.T = T

    def european(self, n_sims=100000, mode='GBM'):
        """
        Get a price of European option using Monte Carlo simulations.

        Parameters
        ----------
        :param n_sims: How many simulations for calculations, default: 100000
        :type n_sims: int

        Returns
        -------
        :return: Price of European option.
        :rtype: float

        Examples
        --------
        Price one dimensional put option, based on underlying asset modelled with geometric Brownian motion:
        >>> import numpy as np
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_GBM(sigma=0.6,values_per_year_GBM=255)
        >>> option = Option(underlyings=asset, payoff_func=lambda trajectory: np.maximum(100-trajectory,0), T=1)
        >>> option.european()
        20.079249595333774

        Price two dimensional maximum put option, based on two underlyings modelled with GBM:
        >>> irr = 0.06
        >>> N = 255
        >>> asset1 = Underlying(spot_price=100, r=irr)
        >>> asset1.calibrate_GBM(sigma=0.6, values_per_year_GBM=N)
        >>> asset2 = Underlying(spot_price=120, r=irr)
        >>> asset2.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)

        >>> def double_max_put(sims_list, K):
        >>>    return np.maximum(np.maximum(K - sims_list[0], K - sims_list[1]), 0)

        >>> option = Option(underlyings=(asset1, asset2), payoff_func=lambda trajectories: double_max_put(trajectories, 100), T=1)
        >>> option.european()
        23.875632302306844
        """

        r = self.underlyings[0].r
        l = []
        T = self.T

        for a in self.underlyings:
            sims = a.simulate(mode=mode, size=n_sims, T=T).to_numpy()
            l.append(sims)
        if len(self.underlyings) == 1:
            res = np.mean(self.payoff_func(l[0])[:, -1] * np.exp(-r * T))
        else:
            res = np.mean(self.payoff_func(l)[:, -1] * np.exp(-r * T))
        return res


    def LS(self, n_sims=10000, mode='GBM'):
        """
        Calculate american option value using Longstaff-Schwarts method. \n
        In case of one underlying, interpolation in algorithm steps tries to fit 5-th degree spline which gives the best results.
        Since spline fit might sometimes cause errors, in such steps algorithm will fit 3-rd degree polynomial instead. \n
        In case of n > 1 underlyings, algorithm will always fit 3rd degree (n+1)-dimentional surface.

        Parameters
        ----------
        :param n_sims: Number of simulations for pricing
        :type n_sims: int
        :param mode: mode of underlying(s) that is desired to be used for simulations. Only 'LS' and 'BT' are supported.
        :param mode: str

        Returns
        -------
        :return: Value of specified option calculated using LS method
        :rtype: float

        Examples
        --------
        Price one dimensional put option, based on underlying asset modelled with geometric Brownian motion:
        >>> import numpy as np
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_GBM(sigma=0.6,values_per_year_GBM=255)
        >>> option = Option(underlyings=asset, payoff_func=lambda trajectory: np.maximum(100-trajectory,0), T=1)
        >>> option.LS(10000,'GBM')
        20.87750951209692

        Price two dimensional maximum put option, based on two underlyings modelled with GBM:
        >>> irr = 0.06
        >>> N = 255
        >>> asset1 = Underlying(spot_price=100, r=irr)
        >>> asset1.calibrate_GBM(sigma=0.6, values_per_year_GBM=N)
        >>> asset2 = Underlying(spot_price=120, r=irr)
        >>> asset2.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)

        >>> def double_max_put(sims_list, K):
        >>>    return np.maximum(np.maximum(K - sims_list[0], K - sims_list[1]), 0)

        >>> option = Option(underlyings=(asset1, asset2), payoff_func=lambda trajectories: double_max_put(trajectories, 100), T=1)
        >>> option.LS(10000)
        23.933460885060565
        """

        if len(self.underlyings) == 1:
            Simulations = self.underlyings[0].simulate(mode=mode, size=n_sims, T=self.T)
            self.LS_price_trajectories = Simulations
            if mode == "GBM":
                values_per_year = self.underlyings[0].values_per_year_GBM
            elif mode == "Bootstrap":
                values_per_year = self.underlyings[0].values_per_year_Bootstrap
            elif mode == "JD":
                values_per_year = self.underlyings[0].values_per_year_JD
            else:
                raise Exception(
                    'Longstaff-Schwartz method (LS) is supported only for GBM, JD and Boostrapping at this moment')

            Sim_Payoffs = self.payoff_func(Simulations)

            if type(Sim_Payoffs) != pd.DataFrame:
                Sim_Payoffs = pd.DataFrame(Sim_Payoffs)
            TF = Sim_Payoffs > 0
            indices = np.arange(0, n_sims)

            Final_Results = pd.DataFrame(data=0, index=range(n_sims),
                                         columns=range(round(values_per_year * self.T) + 1))
            Final_Results[round(values_per_year * self.T)] = Sim_Payoffs.iloc[:, -1]

            Exercise_Times = pd.DataFrame(data=0, index=range(n_sims),
                                           columns=range(round(values_per_year * self.T) + 1))
            Exercise_Times[round(values_per_year * self.T)] = 1 * (Sim_Payoffs.iloc[:, -1] > 0)

            for j in tqdm(np.arange(2, round(self.T * values_per_year) + 1)):
                TF_j = indices[TF.iloc[:, -j]]
                if len(TF_j) >= 3:
                    try:
                        def f_j(S_t):
                            H = pd.DataFrame({'S_t': Simulations.iloc[TF_j, -j], 'PO_t': (
                                    np.exp(-self.underlyings[0].r * np.arange(1, j) / round(
                                        values_per_year * self.T)) * Final_Results.iloc[TF_j,
                                                                     (-j + 1):]).sum(axis=1)})
                            H = H.sort_values(by=H.columns[0])
                            h = interpolate.UnivariateSpline(H['S_t'] / self.underlyings[0].spot_price,
                                                             H['PO_t'] / self.underlyings[0].spot_price, k=5)
                            return (self.underlyings[0].spot_price * h(S_t / self.underlyings[0].spot_price))

                        estimations_j = f_j(Simulations.iloc[TF_j, -j])
                    except:
                        X_j = pd.concat([Simulations.iloc[TF_j, -j]] * 3, axis=1) ** (3, 2, 1)
                        Y_j = (np.exp(
                            -self.underlyings[0].r * np.arange(1, j) / round(values_per_year * self.T)) * Final_Results.iloc[TF_j,
                                                                                              (-j + 1):]).sum(
                            axis=1)

                        model_j = linear_model.LinearRegression()
                        model_j.fit(X_j, Y_j)
                        estimations_j = model_j.predict(X_j)

                    choose_to_exercise_indices = TF_j[estimations_j < Sim_Payoffs.iloc[TF_j, -j]]

                    Final_Results.iloc[choose_to_exercise_indices, -j] = Sim_Payoffs.iloc[
                        choose_to_exercise_indices, -j]
                    Exercise_Times.iloc[choose_to_exercise_indices, -j] = 1
                    Final_Results.iloc[choose_to_exercise_indices, (-j + 1):] = 0

                elif len(TF_j) == 2 or len(TF_j) == 1:
                    estimations_j = (np.exp(
                        -self.underlyings[0].r * np.arange(1, j) / round(values_per_year * self.T)) * Final_Results.iloc[TF_j,
                                                                                          (-j + 1):]).sum(axis=1)
                    choose_to_exercise_indices = TF_j[estimations_j < Sim_Payoffs.iloc[TF_j, -j]]
                    Final_Results.iloc[choose_to_exercise_indices, -j] = Sim_Payoffs.iloc[
                        choose_to_exercise_indices, -j]
                    Exercise_Times.iloc[choose_to_exercise_indices, -j] = 1
                    Final_Results.iloc[choose_to_exercise_indices, (-j + 1):] = 0

            self.ET_LS = Exercise_Times.to_numpy()

            if mode == "GBM":
                self.price_GBM_LS = np.mean(
                    (np.exp(-self.underlyings[0].r * np.arange(0, round(
                        values_per_year * self.T) + 1) / round(
                        values_per_year * self.T)) * Final_Results).sum(axis=1))
                return self.price_GBM_LS
            elif mode == "Bootstrap":
                self.price_Bootstrap_LS = np.mean(
                    (np.exp(-self.underlyings[0].r * np.arange(0, round(
                        values_per_year * self.T) + 1) / round(
                        values_per_year * self.T)) * Final_Results).sum(axis=1))
                return self.price_Bootstrap_LS
            elif mode == 'JD':
                self.price_JD_LS = np.mean(
                    (np.exp(-self.underlyings[0].r * np.arange(0, round(
                        values_per_year * self.T) + 1) / round(
                        values_per_year * self.T)) * Final_Results).sum(axis=1))

                return self.price_JD_LS
        else:
            if mode == "GBM":
                if all(u.values_per_year_GBM == self.underlyings[0].values_per_year_GBM for u in self.underlyings):
                    values_per_year = self.underlyings[0].values_per_year_GBM
                else:
                    raise Exception('Underlyings are calibrated for different values_per_year_GBM.')
            elif mode == "Bootstrap":
                if all(u.values_per_year_Bootstrap == self.underlyings[0].values_per_year_Bootstrap for u in
                       self.underlyings):
                    values_per_year = self.underlyings[0].values_per_year_Bootstrap
                else:
                    raise Exception('Underlyings are calibrated for different values_per_year_Bootstrap.')
            elif mode == "JD":
                if all(u.values_per_year_JD == self.underlyings[0].values_per_year_JD for u in self.underlyings):
                    values_per_year = self.underlyings[0].values_per_year_JD
                else:
                    raise Exception('Underlyings are calibrated for different values_per_year_JD.')

            else:
                raise Exception(
                    'Longstaff-Schwartz method (LS) is supported only for GBM, JD and Boostrapping at this moment')

            if any(u.r != self.underlyings[0].r for u in self.underlyings):
                warnings.warn(
                    'Underlyings assume different interest rates! Interest rate from the first underlying will be used')

            sims_list = []
            for u in self.underlyings:
                sims_list.append(u.simulate(mode=mode, size=n_sims, T=self.T))

            self.LS_price_trajectories = sims_list

            Sim_Payoffs = self.payoff_func(sims_list)

            if type(Sim_Payoffs) != pd.DataFrame:
                Sim_Payoffs = pd.DataFrame(Sim_Payoffs)

            TF = Sim_Payoffs > 0
            indices = np.arange(0, n_sims)

            Final_Results = pd.DataFrame(data=0, index=range(n_sims),
                                         columns=range(round(values_per_year * self.T) + 1))
            Final_Results[round(values_per_year * self.T)] = Sim_Payoffs.iloc[:, -1]

            Exercise_Times = pd.DataFrame(data=0, index=range(n_sims),
                                         columns=range(round(values_per_year * self.T) + 1))
            Exercise_Times[round(values_per_year * self.T)] = 1 * (Sim_Payoffs.iloc[:, -1] > 0)

            m = len(self.underlyings)
            powers = set(product(range(4), repeat=m)) - set([tuple(np.zeros(m)), tuple(3 * np.ones(m))])

            for j in tqdm(np.arange(2, round(self.T * values_per_year) + 1)):
                TF_j = indices[TF.iloc[:, -j]]
                if len(TF_j) >= 3:
                    Sims_j = np.column_stack(list(map(itemgetter(int(values_per_year*self.T) - j + 1), sims_list)))

                    X_j = np.transpose(np.array([np.sum(Sims_j[TF_j, :] ** p, axis=1) for p in powers]))
                    Y_j = (np.exp(-self.underlyings[0].r * np.arange(1, j) / round(255 * self.T)) * Final_Results.iloc[
                                                                                                    TF_j,
                                                                                                    (-j + 1):]).sum(
                        axis=1)

                    model_j = linear_model.LinearRegression()
                    model_j.fit(X_j, Y_j)

                    estimations_j = model_j.predict(X_j)
                    choose_to_exercise_indices = TF_j[estimations_j < Sim_Payoffs.iloc[TF_j, -j]]

                    Final_Results.iloc[choose_to_exercise_indices, -j] = Sim_Payoffs.iloc[
                        choose_to_exercise_indices, -j]
                    Exercise_Times.iloc[choose_to_exercise_indices, -j] = 1
                    Final_Results.iloc[choose_to_exercise_indices, (-j + 1):] = 0

                elif len(TF_j) == 2 or len(TF_j) == 1:
                    estimations_j = (np.exp(
                        -self.underlyings[0].r * np.arange(1, j) / round(255 * self.T)) * Final_Results.iloc[TF_j,
                                                                                          (-j + 1):]).sum(axis=1)
                    choose_to_exercise_indices = TF_j[estimations_j < Sim_Payoffs.iloc[TF_j, -j]]
                    Final_Results.iloc[choose_to_exercise_indices, -j] = Sim_Payoffs.iloc[
                        choose_to_exercise_indices, -j]
                    Exercise_Times.iloc[choose_to_exercise_indices, -j] = 1
                    Final_Results.iloc[choose_to_exercise_indices, (-j + 1):] = 0

            self.ET_LS = Exercise_Times.to_numpy()

            if mode == "GBM":
                self.price_GBM_LS = np.mean(
                    (np.exp(-self.underlyings[0].r * np.arange(0, round(
                        values_per_year * self.T) + 1) / round(
                        values_per_year * self.T)) * Final_Results).sum(axis=1))
                return self.price_GBM_LS
            elif mode == "Bootstrap":
                self.price_Bootstrap_LS = np.mean(
                    (np.exp(-self.underlyings[0].r * np.arange(0, round(
                        values_per_year * self.T) + 1) / round(
                        values_per_year * self.T)) * Final_Results).sum(axis=1))
                return self.price_Bootstrap_LS
            elif mode == "JD":
                self.price_JD_LS = np.mean(
                    (np.exp(-self.underlyings[0].r * np.arange(0, round(
                        values_per_year * self.T) + 1) / round(
                        values_per_year * self.T)) * Final_Results).sum(axis=1))
                return self.price_JD_LS

    def ssp(self, n_sims, mode='GBM', approach='sobol_sequence'):
        """
        Calculate american option value using state space partitioning method. In each timestep (depending on simulations)
        this method parts all attainable asset values (from simulations) into n_bins parts.
        Then it calculates average payoff for each bin.
        In each timestep it calculates probabilities of moving from one bin to another by counting how many paths moved
        between two bins in consecutive timesteps.
        It assigns the option value for each bin by choosing maximum from average payoff and
        discounted average of payoffs from next timestep weighted by probabilities of moving to them.
        Calling this method for the first time on the Option on specific Underlying, takes a bit longer as we create
        3-dimensional transition probabilities matrix for the underlying.
        Calling the other options on the same Underlying is then much faster as we recycle once calculated probabilities.

        Method supports path-dependent options.

        Parameters:
        ----------
        n_sims : int
            number of simulations for pricing
        mode : str
            mode of underlying(s) that is desired to be used for simulations. Only 'GBM', 'JD' and 'Bootstrapping' are supported.
        approach : str
            which algorithm of pricing to use. Default: 'sobol_sequence' can calucale all types of options,
            while 'basic_1d' can calculate only one-dimensional options,
            although after calling it first time, next calls are much faster.

        Returns:
        -------
        float : Value of specified option calculated using ssp method

        Examples:
        --------
        Price one dimensional put option, based on underlying asset modelled with geometric Brownian motion:

        >>> import numpy as np
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_GBM(sigma=0.6,values_per_year_GBM=255)
        >>> option = Option(underlyings=asset, payoff_func=lambda trajectory: np.maximum(100-trajectory,0), T=1)
        >>> option.ssp(10000)
        20.290910236944484

        Price two dimensional maximum put option, based on two underlyings modelled with GBM:
        >>> irr = 0.06
        >>> N = 255
        >>> asset1 = Underlying(spot_price=100, r=irr)
        >>> asset1.calibrate_GBM(sigma=0.6, values_per_year_GBM=N)
        >>> asset2 = Underlying(spot_price=120, r=irr)
        >>> asset2.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)

        >>> def double_max_put(sims_list, K):
        >>>    return np.maximum(np.maximum(K - sims_list[0], K - sims_list[1]), 0)

        >>> option = Option(underlyings=(asset1, asset2), payoff_func=lambda trajectories: double_max_put(trajectories, 100), T=1)
        >>> option.ssp(10000)
        23.921360869625904
        """

        n_bins = int(np.sqrt(n_sims))
        T = self.T

        if approach == 'basic_1d':  # len(self.underlyings) == 1:
            asset = self.underlyings[0]
            paths = asset.simulate(mode=mode, size=n_sims, T=T).to_numpy()
            self.ssp_price_trajectories = paths

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

            #exercise = np.zeros((n_bins, ti+1))
            #H = np.zeros((n_bins, ti+1))
            # n of paths in a bin
            n_paths = int(n_sims / n_bins)
            sorted_steps = np.argsort(paths, axis=0)

            all_payoffs = self.payoff_func(paths)
            # all_payoffs = self.payoff_func(paths)

            if not asset.ssp_calibrated:
                probs_matrix = np.zeros((n_bins, n_bins, ti))

            for i in tqdm(range(ti + 1)):
                cur_bins = sorted_steps[:, ti - i]
                hi = all_payoffs[cur_bins, ti - i]
                hi_bins = np.mean(hi.reshape(-1, n_paths), axis=1)  # payoffy w danym kroku

                if i == 0:
                    V_i = hi_bins

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
                    V_i = np.maximum(hi_bins, probs @ V_i1 * disc)

                #exercise[:, ti - i] = V_i <= hi_bins
                #H[:,ti-i] = hi_bins
            if not asset.ssp_calibrated:
                asset.probs_matrix = probs_matrix
                asset.ssp_calibrated = True

            #Yt = H * np.exp(- np.tile(np.arange(0, ti + 1), (n_bins, 1)) * (T/values_per_year) * asset.r)
            #exercise_time = np.argmax(exercise, axis=1)
            #res = np.mean(Yt[np.arange(len(Yt)), exercise_time])
            #self.upper_bound_price_ssp = np.mean(V_i)
            #self.ET_ssp = exercise.astype(int)
            res = np.mean(V_i)
            self.ET_ssp = res
        else:
            # trying the approach as for one asset, but instead of creating bins for simulated paths of the underlying,
            # TODO: introduce possibility of simulating correlated assets

            if mode == "GBM":
                if all(u.values_per_year_GBM == self.underlyings[0].values_per_year_GBM for u in self.underlyings):
                    values_per_year = self.underlyings[0].values_per_year_GBM
                else:
                    raise Exception('Underlyings are calibrated for different values_per_year_GBM.')
            elif mode == "Bootstrap":
                if all(u.values_per_year_Bootstrap == self.underlyings[0].values_per_year_Bootstrap for u in
                       self.underlyings):
                    values_per_year = self.underlyings[0].values_per_year_Bootstrap
                else:
                    raise Exception('Underlyings are calibrated for different values_per_year_Bootstrap.')
            elif mode == "JD":
                if all(u.values_per_year_JD == self.underlyings[0].values_per_year_JD for u in self.underlyings):
                    values_per_year = self.underlyings[0].values_per_year_JD
                else:
                    raise Exception('Underlyings are calibrated for different values_per_year_JD.')
            else:
                raise Exception(
                    'State space partitioning method method (ssp) is supported only for GBM, JD and Boostrapping at this moment')

            if any(u.r != self.underlyings[0].r for u in self.underlyings):
                warnings.warn(
                    'Underlyings assume different interest rates! Interest rate from the first underlying will be used')

            n_assets = len(self.underlyings)
            ti = round(values_per_year * T)
            r = self.underlyings[0].r
            dt = T / ti
            disc = np.exp(- r * dt)

            # generating Sobol sequence
            # uniform
            np.random.seed(1)
            sobol_sequence = chaospy.create_sobol_samples(n_bins * ti, n_assets)
            representative_paths = np.zeros((n_bins, ti + 1, n_assets))
            # representative paths
            for a in range(n_assets):
                sobol_inv_norm = stats.norm.ppf(sobol_sequence[a, :])
                sobol_inv_norm = np.random.permutation(sobol_inv_norm)
                sigma = self.underlyings[a].sigma
                sobol_increments = np.hstack((np.zeros((int(n_bins), 1)),
                                              (r - sigma ** 2 / 2) * dt + sigma * np.sqrt(dt) * np.reshape(
                                                  sobol_inv_norm, (int(n_bins), ti))))
                # print(sobol_increments)
                representative_paths[:, :, a] = self.underlyings[a].spot_price * np.exp(
                    np.cumsum(sobol_increments, axis=1))

            self.ssp_representative = representative_paths
            # print(representative_paths)
            paths = np.zeros((n_sims, ti + 1, n_assets))

            for a in range(n_assets):
                paths[:, :, a] = self.underlyings[a].simulate(mode=mode, size=n_sims, T=self.T).to_numpy()

            sim_list = [paths[:, :, a] for a in range(n_assets)]

            if n_assets == 1:
                all_payoffs = self.payoff_func(sim_list[0])
            else:
                all_payoffs = self.payoff_func(sim_list)

            self.ssp_price_trajectories = paths


            Vt = np.zeros((n_sims, ti + 1))  # macierz wartości
            Ht = np.zeros((n_sims, ti))  # continuation values
            discounts = np.exp(- np.tile(np.arange(0, ti + 1), (n_sims, 1)) * dt * r)
            Yt = discounts * all_payoffs  # zdyskontowane payoffy w każdej chwili
            Vt[:, ti] = all_payoffs[:, ti]

            ###wartości kontynuacji
            ######znajdujemy punkt który jest najbliżej każdej obserwacji w każdym kroku
            all_bins = np.zeros((n_sims, ti + 1))
            for i in tqdm(range(n_sims)):
                distances = np.zeros((n_bins, ti + 1))
                for k in range(n_bins):
                    distances[k, :] = np.sum((paths[i, :, :] - representative_paths[k, :, :]) ** 2,
                                             axis=1)  # odległość itej obs od k-tego bina w każdej chwili
                all_bins[i, :] = np.argmin(distances, axis=0)

            # print(all_bins) # macierz przynależności do danego bina w każdym kroku

            for i in range(1, ti + 1):
                #### wartość kontynuacji - średnia z wartości opcji w kolenym kroku z trajektorii w tm samym binie
                df = pd.DataFrame({'cur_bin': all_bins[:, ti - i],
                                   'next_bin': all_bins[:, ti - i + 1],
                                   'next_val': Vt[:, ti - i + 1]})
                df['continue'] = df.groupby('cur_bin')['next_val'].transform('mean')
                Ht[:, ti - i] = df['continue'] * disc
                Vt[:, ti - i] = np.maximum(all_payoffs[:, ti - i], Ht[:, ti - i])
            Ht = np.hstack((Ht, np.zeros((n_sims, 1))))
            # print(Vt[0,:])
            # print(np.mean(Vt[:,0]))

            ###stopping times
            stop = all_payoffs > Ht
            exercise_time = np.argmax(stop, axis=1)

            res = np.mean(Yt[np.arange(len(Yt)), exercise_time])

            self.ET_ssp = stop.astype(int)
            self.upper_bound_price_ssp = np.mean(Vt[:,0])

        if mode == "GBM":
            self.price_GBM_ssp = res
        elif mode == "Bootstrap":
            self.price_Bootstrap_ssp = res
        elif mode == "JD":
            self.price_JD_ssp = res
        return res

    def RTM(self, n_sims=10000, mode='RT_GBM'):
        """
        Creating an interval that contains the value of an American option using the Random Tree Method. \n
        The interval is formed by combining the confidence intervals of two estimators - the high and low estimators.\n
        This method only works for options with a single underlying asset. \n
        By increasing the "successors" parameter during calibration and the number of simulations,
        the interval will become smaller. The computational complexity increases exponentially with the increase
        of the "time_steps" parameter (provided during the calibration of the underlying asset).


        Parameters
        ----------
        :param n_sims: Number of simulations for pricing
        :type n_sims: int
        :param mode: mode of underlying that is desired to be used for simulations. Only 'RT_GBM' is supported.
        :type mode: str

        Returns
        -------
        :return: interval that contains value of specified option calculated using Random Tree method
        :rtype: pd.DataFrame

        Examples
        --------
        Price one dimensional put option, based on underlying asset modelled with random tree:

        >>> import numpy as np
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_RT_GBM(sigma=0.6,time_steps=5)
        >>> option = Option(underlyings=asset, payoff_func=lambda trajectory: np.maximum(100-trajectory,0), T=1)
        >>> option.RTM(10000)
            low est   left low  right low  high est  left high  righ high
        0  19.879359  19.772672  19.986046   23.6832  23.566003  23.800396
        """
        Simulations = self.underlyings[0].simulate(mode=mode, size=n_sims, T=self.T)
        high_estimators = []
        low_estimators = []
        for simulation in tqdm(Simulations):
            payoff_df = simulation.apply(self.payoff_func)
            high = pd.DataFrame(np.zeros(simulation.shape))
            high.iloc[:, -1] = payoff_df.iloc[:, -1]
            low = pd.DataFrame(np.zeros(simulation.shape))
            low.iloc[:, -1] = payoff_df.iloc[:, -1]
            b = self.underlyings[0].successors
            m = self.underlyings[0].time_steps
            for i in range(self.underlyings[0].time_steps - 1, -1, -1):
                # high estimator
                cont_value = high.iloc[:, i + 1].groupby(np.arange(0, b ** m) // b).mean()
                high.iloc[:, i] = np.maximum(cont_value, payoff_df.iloc[:, i])
                # low estimator
                W = np.identity(b)
                M = np.ones(b) - W
                ind = np.repeat(np.arange(1, b ** (i + 1) + 1), b)
                indeksy = np.tile(M, b ** i).flatten() * ind
                indeksy2 = ind - indeksy
                srednie = pd.concat([low.iloc[:b ** (i + 1), i + 1]] * b).groupby(indeksy).mean()[1:]
                wart_poz = pd.concat([low.iloc[:b ** (i + 1), i + 1]] * b).groupby(indeksy2).mean()[1:]
                payoff_now = pd.concat([payoff_df.iloc[:b ** i, i]] * b)
                wart_poz[np.array(srednie) < np.array(payoff_now)] = payoff_now[
                    np.array(srednie) < np.array(payoff_now)]
                low.iloc[:b ** (i), i] = pd.DataFrame(
                    wart_poz.groupby(np.arange(0, b ** (i + 1)) % b ** i).mean()).iloc[:, 0]
            high_estimators.append(high.iloc[0, 0])
            low_estimators.append(low.iloc[0, 0])
            results = pd.DataFrame({'low est': [np.mean(low_estimators)],
                                    'left low': [np.mean(low_estimators) - np.std(low_estimators) / np.sqrt(
                                        n_sims) * stats.norm.ppf(0.95)],
                                    'right low': [np.mean(low_estimators) + np.std(low_estimators) / np.sqrt(
                                        n_sims) * stats.norm.ppf(0.95)],
                                    'high est': [np.mean(high_estimators)],
                                    'left high': [np.mean(high_estimators) - np.std(high_estimators) / np.sqrt(
                                        n_sims) * stats.norm.ppf(0.95)],
                                    'righ high': [np.mean(high_estimators) + np.std(high_estimators) / np.sqrt(
                                        n_sims) * stats.norm.ppf(0.95)]})
        return results

    def plot_exercise_times(self, method, plot_trajectories_ratio = 0.02, alpha_exercise_moments=0.5, alpha_trajectories = 0.3, show = True):
        if len(self.underlyings) == 1:
            if method == 'RTM':
                raise Exception('plot of RTM exercise times is not supported')
            elif not hasattr(self, 'ET_' + method):
                raise Exception('''You haven't calculated price with .''' + method + ''' yet or chosen pricing method doesn't exist''')

            if method == 'LS':
                time_moments = np.argwhere(self.ET_LS == 1)[:, 1]
                asset_prices = self.LS_price_trajectories.to_numpy()[self.ET_LS.astype(bool)]
                price_traj = self.LS_price_trajectories.to_numpy()
            elif method == 'ssp':
                time_moments = np.argwhere(self.ET_ssp == 1)[:, 1]
                asset_prices = self.ssp_price_trajectories[self.ET_ssp.astype(bool)]
                price_traj = self.ssp_price_trajectories

            plt.scatter(time_moments, asset_prices, alpha = alpha_exercise_moments)
            plt.title("Exercise moments", fontsize=20)
            plt.xlabel("Time", fontsize=16)
            plt.ylabel("Asset price", fontsize=16, labelpad=10)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)

            if plot_trajectories_ratio == 0:
                pass
            else:
                for k in np.arange(0, np.shape(price_traj)[0], int(plot_trajectories_ratio*np.shape(price_traj)[0])):
                    plt.plot(np.arange(0, np.shape(price_traj)[1] , 1), price_traj[k, :], alpha=alpha_trajectories)
            if show:
                plt.show()

        elif len(self.underlyings) == 2:
            if method == 'RTM':
                raise Exception('plot of RTM exercise times is not supported')
            elif not hasattr(self, 'ET_' + method):
                raise Exception('''You haven't calculated price with .''' + method + ''' yet or chosen pricing method doesn't exist''')

            if method == 'LS':
                rows, cols = np.shape(self.LS_price_trajectories)[1:3]
                ET_TF = self.ET_LS.astype(bool)
                t = np.reshape(np.tile(np.arange(0, cols), rows), (rows, cols))[ET_TF]
                X = self.LS_price_trajectories[0].to_numpy()[ET_TF]
                Y = self.LS_price_trajectories[1].to_numpy()[ET_TF]
                price_traj = self.LS_price_trajectories
            elif method == 'ssp':

                rows, cols = np.shape(self.ssp_price_trajectories)[0:2]
                ET_TF = self.ET_ssp.astype(bool)
                t = np.reshape(np.tile(np.arange(0, cols), rows), (rows, cols))[ET_TF]
                X = self.ssp_price_trajectories[:,:,0][ET_TF]
                Y = self.ssp_price_trajectories[:,:,1][ET_TF]
                price_traj = self.ssp_price_trajectories

            fig1 = plt.figure(1)
            ax1 = fig1.add_subplot(111, projection='3d')
            ax1.scatter(t, X, Y, color='green', alpha=alpha_exercise_moments)

            ax1.set_title("Exercise moments", fontsize=20)

            # Set x, y, and z labels with adjusted size
            ax1.set_xlabel("Time", fontsize=15, labelpad= 10)
            ax1.set_ylabel("1st asset price", fontsize=15, labelpad= 10)
            ax1.set_zlabel("2nd asset price", fontsize=15, labelpad= 10)

            # Increase the size of tick labels on all axes
            ax1.tick_params(axis='x', labelsize=12)
            ax1.tick_params(axis='y', labelsize=12)
            ax1.tick_params(axis='z', labelsize=12)

            #Plot trajectories
            if plot_trajectories_ratio == 0:
                pass
            else:
                if method == 'LS':
                    for k in np.arange(0, np.shape(price_traj)[1], int(plot_trajectories_ratio*np.shape(price_traj)[1])):
                        plt.plot(np.arange(0, cols, 1), price_traj[0].to_numpy()[k, :],price_traj[1].to_numpy()[k, :], alpha=alpha_trajectories)
                elif method == 'ssp':
                    for k in np.arange(0, np.shape(price_traj)[0], int(plot_trajectories_ratio*np.shape(price_traj)[1])):
                        plt.plot(np.arange(0, cols, 1), price_traj[k,:,0],price_traj[k,:,1], alpha=alpha_trajectories)
            if show:
                plt.show()
        else:
            raise Exception('Exercise times for options based on 3 or more assets cannot be visualized')

    def hist_optimal_exercise(self, method, show = True):
        if method == 'RTM':
            raise Exception('plot of RTM exercise times is not supported')
        elif not hasattr(self, 'ET_' + method):
            raise Exception(
                '''You haven't calculated price with .''' + method + ''' yet or chosen pricing method doesn't exist''')

        if len(self.underlyings) == 1:
            if method == 'LS':
                price_traj = self.LS_price_trajectories
            elif method == 'ssp':
                price_traj = self.ssp_price_trajectories
        else:
            if method == 'LS':
                price_traj = self.LS_price_trajectories[0]
            elif method == 'ssp':
                price_traj = self.ssp_price_trajectories[0]

        if method == 'LS':
            v = np.argmax(self.ET_LS, axis=1)
            pe = str(100 * np.round(np.mean(v != 0), 3))
            v = v[v != 0]
        elif method == 'ssp':
            v = np.argmax(self.ET_ssp, axis=1)
            pe = str(100 * np.round(np.mean(v != 0), 3))
            v = v[v != 0]

        plt.hist(v, bins=np.arange(0, np.shape(price_traj)[1]))
        plt.title(pe + "% of options have been exercised", fontsize=17)
        plt.text(0.5, 1.05, "Optimal exercise moments", fontsize=20, ha='center', transform=plt.gca().transAxes)
        plt.xlabel("Time", fontsize=16)
        plt.ylabel("Density", fontsize=16, labelpad=10)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)

        if show:
            plt.show()