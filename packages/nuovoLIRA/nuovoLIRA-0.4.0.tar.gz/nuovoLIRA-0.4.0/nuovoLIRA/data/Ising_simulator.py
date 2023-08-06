""" 
Generate samples from Ising(beta) for given input beta (inverse temperature) using Metropolis-Hastings.
"""

import numpy as np 
from scipy import stats 

def find_NN(lattice : np.ndarray, row : int, col : int) -> list:
    """ 
    Find the neighbouring spins to lattice[row,col]. Returns a list of 4 values \in {-1,1}.
    """
    L = len(lattice) 
    left = lattice[row, (col - 1) % L]
    down = lattice[(row + 1) % L, col]
    up = lattice[(row - 1) % L, col]
    right = lattice[row, (col + 1) % L]

    return [up,down,left,right]

def lattice_update(random_state,lattice : np.ndarray, beta : int) -> np.ndarray:
    """
    Randomly flip one spin in the input lattice. If this flip causes the new lattice to have 
    lower energy, then return the new lattice. Else return the new lattice with probability 
    p = exp(-deltaE*beta). Return the input lattice with probability 1-p. 

    Parameters
    ----------

    random_state : np.random.RandomState
            Random State object. The seed value is set by the user upon instantiation of the Random State object. 

    
    """
    L = len(lattice) 
    row = random_state.integers(0, L)
    col = random_state.integers(0, L) 
    spin = lattice[row, col]


    neighbours = find_NN(lattice,row,col)

    up = neighbours[0]
    down = neighbours[1]
    left = neighbours[2]
    right = neighbours[3]

    e_surrounding = (up + down + right + left)
    delta_E = 2 * spin * e_surrounding

    # check Glauber conditions for the spin -- negative delta_E or prob exp(-delta_E*beta)
    if delta_E <= 0 or np.exp(-delta_E * beta) > random_state.uniform(0,1): 
        spin *= -1

    # replace value in the lattice
    lattice[row, col] = spin       

    return lattice

def one_sweep(random_state,lattice : np.ndarray, beta : int) -> np.ndarray: 
    """
    Do L*L lattice updates. Return the new lattice
    """

    L = len(lattice) 
    N = L*L 

    for _ in range(N): 
        lattice = lattice_update(random_state,lattice,beta) 

    return lattice 


def ising_mcmc(random_state,L : int, numsweeps : int, RELAX_SWEEPS : int, beta : float) -> np.ndarray:
    """
    Run the metropolis-hastings sampling of Ising(beta).
    """

    lattice = 2 * np.random.randint(2, size=(L,L)) -1 #initialise lattice with 1s and -1s

    lattice_storage = np.zeros(shape=(numsweeps,L,L)) #numpy array that will store the microstates

    #a sweep involves changing a random spin and deciding whether to keep the resulting microstate, L*L times
    for sweep in range(numsweeps+RELAX_SWEEPS):
        '''perform the lattice update, which involves testing N randomly selected spins'''

        lattice = one_sweep(random_state,lattice,beta) 

        #only store the lattice if thermal equilibrium has been reached
        if sweep>=RELAX_SWEEPS:
            lattice_storage[sweep-RELAX_SWEEPS,:,:] = lattice

    return lattice_storage 

def ising_MAP(random_state,L : int, numsweeps : int, RELAX_SWEEPS : int, beta : float) -> np.ndarray: 
    """ 
    Find the MAP estimate of a chain of MCMC Ising samples. 
    """

    samples = ising_mcmc(random_state,L,numsweeps,RELAX_SWEEPS,beta) 
    map_estimate = stats.mode(samples,axis=0)
    return map_estimate[0][0]

def ising_mean(random_state,L : int, numsweeps : int, RELAX_SWEEPS : int, beta : float) -> np.ndarray: 
    """ 
    Find the mean estimate of a chain of MCMC Ising samples. 
    """

    samples = ising_mcmc(random_state,L,numsweeps,RELAX_SWEEPS,beta) 
    mean_estimate = np.mean(samples,axis=0)
    return mean_estimate

def ising_point_estimate(random_state,L : int, numsweeps : int, RELAX_SWEEPS : int, beta : float) -> np.ndarray:
    """ 
    Return the last of a chain of MCMC Ising samples. 
    """

    samples = ising_mcmc(random_state,L,numsweeps,RELAX_SWEEPS,beta) 
    return samples[-1]  
