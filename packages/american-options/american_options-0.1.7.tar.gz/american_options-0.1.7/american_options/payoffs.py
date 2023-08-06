import numpy as np
import warnings
import pandas as pd
from tqdm import tqdm


# --------------- One dimensional payoffs ----------------
def payoff_creator_1d(paths, payoff, path_dependent=False, pd_type='asian', barrier=False, barrier_level=0,
                      barrier_type='up-and-out', *args, **kwargs):
    """
    Creates various payoffs for one dimensional derivatives, depending on specified type of option and payoff function.\n
    By choosing 'path_dependent=True' you can create path dependent payoffs - that are functions of all past asset values.\n

    Parameter 'pd_type' is responsible for kind of path-dependency, possible choices:
        - 'asian', mean of asset price,
        - 'asian_geom', geometric mean,
        - 'asian_strike', strike is a mean of underlying,
        - 'asian_strike_geom', strike is a (geometric) mean,
        - 'lookback_min', min value,
        - 'lookback_max': max value,

    By setting 'barrier=True' you activate the barrier, you then need to specify it's level by setting parameter 'barrier_level'.
    Aditionally, you need to specify the type with setting 'barrier_type' to either of:
        - 'up-and-out',
        - 'down-and-out',
        - 'up-and-in',
        - 'down-and-in'.

    You might specify any additional parameters that should be passed to 'payoff_func' with *args, **kwargs. \n

    Parameters:
    -----------
    paths : array
        Generated trajectories for which we want to create a payoff in each timestep, each row of n array is a new trajectory
    payoff_func : function
        Function we want to use as payoff, taking paths as an argument and possibly other arguments
    path_dependent : bool
        If option is path dependent, it means that payoff depends on the whole (or some part) of the underlying price process
    pd_type : str
        What kind of path dependency
    barrier : bool
        If option has a barrier
    barrier_level : float
        Level of a barrier
    barrier_type : str
        Type of barrier

    Returns:
    -------
    payoffs : numpy.ndarray
        Payoffs for an option type
    """

    if type(paths) != np.ndarray:
        paths = paths.to_numpy()

    if barrier:
        if barrier_level == 0:
            raise Exception('Please specify barrier level')

        if barrier_type[:2] == 'up':
            arr = paths >= barrier_level
        elif barrier_type[:4] == 'down':
            arr = paths <= barrier_level

        # if there is no true value(path wont touch the barrier) argmax will return first false index -->0
        # as we cannot start being out of barrier I will take zeros as paths when we havent touched the barrier

        indexes = np.argmax(arr, axis=1)
        affected = np.where(indexes != 0)

    if path_dependent:
        if pd_type == 'asian':
            paths = np.cumsum(paths, axis=1) / np.arange(1, len(paths[0]) + 1)
        elif pd_type == 'asian_geom':
            paths = np.cumprod(paths, axis=1) ** (1 / np.arange(1, len(paths[0]) + 1))
        elif pd_type == 'asian_strike':
            K = np.cumsum(paths, axis=1) / np.arange(1, len(paths[0]) + 1)
        elif pd_type == 'asian_strike_geom':
            K = np.cumprod(paths, axis=1) ** (1 / np.arange(1, len(paths[0]) + 1))
        # look-back options - min/max of path
        elif pd_type == 'lookback_max':
            paths = np.maximum.accumulate(paths, axis=1)
        elif pd_type == 'lookback_min':
            paths = np.minimum.accumulate(paths, axis=1)

    payoffs = payoff(paths, *args, **kwargs)

    if barrier:
        if barrier_type[-3:] == 'out':
            for i in affected[0]:
                # print(i)
                # print(indexes[i])
                payoffs[i, indexes[i]:] = 0
            # payoffs[affected[0], indexes[affected[0]]:] = 0
            # print(affected[0][0])

        elif barrier_type[-2:] == 'in':
            payoffs_c = np.zeros(payoffs.shape)
            for i in affected[0]:
                # print(i)
                # print(indexes[i])
                payoffs_c[i, indexes[i]:] = payoffs[i, indexes[i]:]
            # payoffs[affected, :indexes[affected]] = 0
            # payoffs[-affected, :] = 0
            payoffs = payoffs_c

    return payoffs

def Call_Payoff(traj, K):
    '''
    Creates classical call payoff.

    :param traj: array of underlying values
    :type traj: numpy.ndarray
    :param K: Strike price
    :type K: float
    :return: Payoff of call option.
    :rtype: numpy.ndarray
    '''
    return np.maximum(traj-K,0)

def Put_Payoff(traj, K):
    '''
    Creates classical put payoff.

    :param traj: array of underlying values
    :type traj: numpy.ndarray
    :param K: Strike price
    :type K: float
    :return: Payoff of call option.
    :rtype: numpy.ndarray
    '''
    return np.maximum(K-traj,0)


def square_call(traj, K):
    """
    max(S^2-K, 0)

    :param traj: array of underlying values
    :type traj: numpy.ndarray
    :param K: Strike price
    :type K: float
    :return: Payoff
    :rtype: numpy.ndarray
    """
    return np.maximum(traj**2-K,0)


def straddle_payoff(traj, strike):
    """
    Calculate the payoff of a long straddle options strategy.

    The long straddle strategy involves buying a call option and a put option with the same strike price and expiration date.
    This strategy benefits from significant price movement in either direction. The call option profits when the spot price
    is above the strike price, while the put option profits when the spot price is below the strike price. The total payoff
    of the long straddle strategy is the combined payoff of the call and put options.

    Args:
        traj (numpy.ndarray): Underlying values.
        strike (float): The strike price of the call and put options.

    Returns:
        numpy.ndarray: Payoffs of the long straddle strategy.

    """
    call_payoff = Call_Payoff(traj, strike)
    put_payoff = Put_Payoff(traj, strike)
    total_payoff = call_payoff + put_payoff
    return total_payoff



def bear_put_payoff(traj, strike_long, strike_short):
    """
    Calculate the payoff of a bear put options strategy.

    The bear put strategy involves buying a put option with a higher strike price (long put) and simultaneously selling a put option with
    a lower strike price (short put). This strategy profits from a decrease in the price of the underlying asset.

    Args:
        traj (numpy.ndarray): Underlying asset.
        strike_long (float): The strike price of the long put option.
        strike_short (float): The strike price of the short put option.

    Returns:
        numpy.ndarray: The payoff of the bear put strategy.

    """
    if strike_long < strike_short:
        warnings.warn('Bear strategy assumes, that long strike is greater than short strike.')

    long_put = Put_Payoff(traj, strike_long)
    short_put = Put_Payoff(traj, strike_short)
    payoff = long_put - short_put
    return payoff


def bull_call_payoff(traj, strike_long, strike_short):
    """
    Calculate the payoff of a bull call options strategy.

    The bull call strategy involves buying a call option with a lower strike price (long call)
    and simultaneously selling a call option with a higher strike price (short call).
    This strategy profits from an increase in the spot price of the underlying asset.

    Args:
        traj (numpy.ndarray): Underlying asset.
        strike_long (float): The strike price of the long put option.
        strike_short (float): The strike price of the short put option.

    Returns:
        numpy.ndarray: The payoff of the bull call strategy.

    """
    if strike_long > strike_short:
        warnings.warn('Bull strategy assumes, that long strike is smaller than short strike')

    long_call = Call_Payoff(traj, strike_long)
    short_call = Call_Payoff(traj, strike_short)
    payoff = long_call - short_call
    return payoff



# ---------------- Two dimensional ------------------------

def spread_payoff(traj_list):
    """
    Calculate the spread payoff for two assets.

    The spread payoff is maximum of the difference between the prices of the two assets and 0.

    Args:
        traj (list): List of trajectories

    Returns:
        numpy.ndarray: The spread payoff.

    """
    if len(traj_list) != 2:
        raise Exception("This payoff is created for two dimensional options!")
    return np.maximum(traj_list[0]-traj_list[1], 0)


def ratio_spread_payoff(traj_list, asset1_weight=1,asset2_weight=1):
    """
    Calculate the ratio spread payoff for two assets.

    The ratio spread payoff is similar to the spread payoff but involves a different number of positions in each asset.

    Args:
        traj_list (list): Underlying assets.
        asset1_weight (float): Number of asset1 to include.
        asset2_weight (float): Number of asset2 to include.

    Returns:
        numpy.ndarray: The ratio spread payoff.

    """
    if len(traj_list) != 2:
        raise Exception("This payoff is created for two dimensional options!")
    return np.maximum(asset1_weight*traj_list[0] - asset2_weight* traj_list[1], 0)


# ------------ Any number of assets ------------
def multiple_call_payoff(traj_list, K):
    """
    Calculate the call payoff for multiple assets.

    The multiple call payoff is calculated as the maximum of the call payoffs for each asset,
    you can specify different strike for every asset (pass as list) or same strike for all.

    Args:
        traj_list (list): Underlyings trajectories.
        K (list or float): The strike price or list of strike prices for each asset.

    Returns:
        numpy.ndarray: Payoffs

    """
    n_assets = len(traj_list)
    if isinstance(K, (int, float)):
        K = [K] * n_assets
    if len(K) != n_assets:
        raise Exception("Please specify one strike for each asset!")
    payoff = np.zeros(traj_list[0].shape)
    for a in range(n_assets):
        payoff = np.maximum(payoff, Call_Payoff(traj_list[a] , K[a]))
    return payoff

def multiple_put_payoff(traj_list, K):
    """
    Calculate the put payoff for multiple assets.

    The multiple put payoff is calculated as the maximum of the put payoffs for each asset,
    you can specify different strike for every asset (pass as list) or same strike for all.

    Args:
        trajs (list): Underlyings trajectories.
        K (list or float): The strike price or list of strike prices for each asset.

    Returns:
        numpy.ndarray: Payoffs

    """
    n_assets = len(traj_list)
    if isinstance(K, (int, float)):
        K  = [K] * n_assets
    if len(K) != n_assets:
        raise Exception("Please specify one strike for each asset!")
    payoff = np.zeros(traj_list[0].shape)
    for a in range(n_assets):
        payoff = np.maximum(payoff, Put_Payoff(traj_list[a], K[a]))
    return payoff


def multiple_mixed_payoff(traj_list, K, payoff_type, which='max', barrier = False, barrier_level=0, barrier_type='up-and-out'):
    """
    Calculate the payoff for multidimensional mixed payoff option.

    The multiple mixed payoff is calculated as the maximum (minimum) of the call or put payoffs for each asset,
    you can specify different strike for every asset (pass as list) or same strike for all.

    You have to specify the type of option for each asset by passing a list of strings
    'call', 'put' to the 'payoff_type' argument.

    By setting parameter which='min' you will take the minimum of all payoffs.
    The default is which='max', that is maximum of all payoffs.

    Args:
        trajs (list): Underlyings trajectories.
        K (list or float): The strike price or list of strike prices for each asset.
        payoff_type (list): The list of strings 'call', 'put' to specify the type for each asset.
        which (string): Default 'max' - we choose maximal payoff of all, 'min' - minimal payoff.

    Returns:
        numpy.ndarray: Payoffs

    """
    n_assets = len(traj_list)
    if isinstance(K, (int, float)):
        K = [K] * n_assets
    if len(payoff_type) != n_assets:
        raise Exception("Please specify one payoff type for each asset!")
    if len(K) != n_assets:
        raise Exception("Please specify one strike for each asset!")
    if which not in ['max', 'min']:
        raise Exception("Only possible values for which argument are 'max' or 'min'!")

    payoff = np.zeros(traj_list[0].shape)
    for a in range(n_assets):
        if payoff_type[a] == 'put':
            p = Put_Payoff(traj_list[a], K[a])
        elif payoff_type[a] == 'call':
            p = Call_Payoff(traj_list[a], K[a])
        else:
            raise Exception("The only supported values for payoff type are 'call' and 'put'!")

        if which == 'max':
            payoff = np.maximum(payoff, p)
        elif which == 'min':
            if a == 0:
                payoff = p
            else:
                payoff = np.minimum(payoff, p)

    return payoff

multiple_call_payoff.__str__ = lambda: 'multiple call payoff'

def Double_Call_Payoff(sims_list, K1, K2):
    return (np.maximum(sims_list[0] - K1, 0) + np.maximum(sims_list[1] - K2, 0))

#def double_max_put(sims_list, K):
#    return np.maximum(np.maximum(K - sims_list[0], K - sims_list[1]), 0)



