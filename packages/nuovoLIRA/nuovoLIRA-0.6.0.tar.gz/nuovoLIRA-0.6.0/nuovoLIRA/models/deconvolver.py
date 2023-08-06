""" 
This file contains classes that sample from the conditional distributions of the NuovoLIRA model.

Their attritubes are the data, the priors, and the parameters necessary to sample from the conditional
distributions. 

"""
from turtle import shape, xcor
from xmlrpc.client import Boolean
import numpy as np
import pandas as pd 
import scipy 
import matplotlib.pyplot as plt 
import scipy.stats as stats
import seaborn as sns
from nuovoLIRA.data.Ising_simulator import * 


class Sample_beta():

    def __init__(
        self,
        random_state : np.random.RandomState, 
        Z: np.ndarray,
        beale_data: np.ndarray, 
        initial_beta: float = 2,
        jumping_std: float = 0.01,
        num_samples: int = 100,
        shape_hyperprior : float = 2,
        rate_hyperprior : float = 2
    ) -> None:
        """ 
        Parameters
        ----------
        random_state : np.random.RandomState
            Random State object. The seed value is set by the user upon instantiation of the Random State object. 

        Z: np.ndarray
            Sample from Ising distribution 

        beale_data: np.ndarray
            Array with two columns: the energy level of the Z-microstate and the log of the number of microstates at this energy

        initial_beta: float 
            Starting value of the Markov Chain

        jumping_std: float
            Standard deviation of the gamma jumping distribution used in the Metropolis-Hastings update 

        num_samples: int
            number of samples of the Markov Chain

        shape_hyperprior : float 
            Beta has a gamma prior: this its shape 

        rate_hyperprior : float 
            Beta has a gamma prior: this its rate

        """

        self.random_state = random_state 
        self.Z = Z 
        self.beale_data = beale_data
        self.initial_beta=initial_beta 
        self.jumping_std = jumping_std
        self.num_samples=num_samples
        self.shape_hyperprior = shape_hyperprior
        self.rate_hyperprior = rate_hyperprior

    def __str__(self) -> str:
        message=(f"random_state={self.random_state}, "
                f"Sample_beta(Z.shape={self.Z.shape}, "
                f"beale_data={self.beale_data}, "
                f"initial_beta={self.initial_beta}, "
                f"jumping_std={self.jumping_std}, "
                f"num_samples={self.num_samples}, "
                f"shape={self.shape_hyperprior}, "
                f"rate_hyperprior={self.rate_hyperprior} ")
        return message 

    @property
    def lattice_length(self) -> int: 
        """ 
        Get the length of the square Z lattice.
        """
        return len(self.Z) 

    def hamiltonian(self) -> float:
        """
        Get the energy of lattice self.Z
        Parameters
        ----------
        Z : 2D square numpy array of size (L,L) 

        Returns
        -------
        energy : float 
            the energy of the configuration Z 
        """ 

        energy = 0 

        L = len(self.Z) #lattice length 
        for i in range(L):
            for j in range(L):
                spin = self.Z[i,j] 
                neighbours = self.Z[(i+1)%L,j] + self.Z[i,(j+1)%L] + self.Z[(i-1)%L,j] + self.Z[i,(j-1)%L] #PBC's 
                energy += spin*neighbours 
        
        energy = energy/2 #account for over-couting 
        return energy 

    def hamiltonian_simulated_Z(self, Z : np.ndarray) -> float:
        """
        Get the energy of input lattice Z
        Parameters
        ----------
        Z : 2D square numpy array of size (L,L) 

        Returns
        -------
        energy : float 
            the energy of the configuration Z 
        """ 

        energy = 0 

        L = len(Z) #lattice length 
        for i in range(L):
            for j in range(L):
                spin = Z[i,j] 
                neighbours = Z[(i+1)%L,j] + Z[i,(j+1)%L] + Z[(i-1)%L,j] + Z[i,(j-1)%L] #PBC's 
                energy += spin*neighbours 
        
        energy = energy/2 #account for over-couting 
        return energy 

    def ising_numerator(self,beta: float) -> float:
        """Get p(Z|beta) - (not normalised by partition function)
        parameters
        ----------
        Z : 2D square numpy array of size (N,N) 

        beta : float 
            inverse temperature 

        Returns
        -------
        score : float 
            A 'score' that is proportional to p(Z|beta) 
        """ 

        energy = self.hamiltonian() 
        score = np.exp(beta*energy) 
        return score 

    def get_partition_exponents(self, beta : float) -> np.ndarray :
        """ 
        Take in your beale data (energy levels and log(counts)) and calculate the exponent for each term in 
        Beale's series expansion 

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        exponents : np.ndarray 
        """
        energy_levels = self.beale_data[:,0] 
        counts = self.beale_data[:,1]    
        exponents = counts + beta*energy_levels 
        return exponents 

    def log_partition(self,beta : float) -> float : 
        """ 
        Use the log-sum-exp trick to calculate log(Z(beta)) 

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        log_partition : float
        
        """
        max_exponent = np.max(self.get_partition_exponents(beta)) 
        log_partition = 0 
        scaled_exponents = self.get_partition_exponents(beta) - max_exponent 
        log_partition = max_exponent + np.log(sum(np.exp(scaled_exponents))) 
        return log_partition 

    def partition_function(self,beta: float) -> float: 
        """ 
        Calculate the partition function of the Ising model for a given input beta (inverse temperature).

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        total_partition : float 
            The partition function value at the input beta 

        """
        beale_array = self.beale_data #dataframe containing energy levels and the number of states at that level
        energy_levels = beale_array[:,0] 
        counts = beale_array[:,1] 
        partition_per_energy = counts*np.exp(energy_levels*beta)
        total_partition = np.sum(partition_per_energy) 
        return total_partition 

    def log_likelihood(self,beta: float) -> float:
        """ 
        Calculate log(p(Z|beta)) 

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        log_lik : float 
            log(p(Z|beta)) 
        """
        # partition = self.partition_function(beta) 
        log_partition = self.log_partition(beta) 
        numerator = beta*self.hamiltonian() 
        log_lik = numerator - log_partition
        return log_lik 

    def gamma_prior(self,beta: float) -> float:
        """ 
        Calculate p(beta) for a gamma distribution 
        
        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        prior : float 
            p(beta) 
        """
        prior = scipy.stats.gamma.pdf(beta,a=self.shape_hyperprior,scale=1/self.rate_hyperprior) 
        return prior 

    def gamma_log_prior(self,beta: float) -> float:
        """ 
        Calculate log(p(beta)) for a gamma distribution 

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        log_prior : float 
            log(p(beta)) 
        """
        log_prior = scipy.stats.gamma.logpdf(beta,a=self.shape_hyperprior,scale=1/self.rate_hyperprior) 
        return log_prior 

    def gamma_log_pobability(self,beta : float) -> float:
        """ 
        Calculate log(p(beta|Z)) (up to the constatant log(p(Z)) term) for a gamma prior on beta

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        log_p : float 
            log(p(Z|beta)) + log(p(beta)) 
        """
        log_p = self.log_likelihood(beta) + self.gamma_log_prior(beta) 
        return log_p 


    def log_jumping_dist(self,beta: float) -> float:
        """
        Draw sample from the log of the gamma distribution with 
        shape = (beta*2)/(jumping_std**2)
        rate = beta/(jumping_std**2)

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        log_density : float 
            sample draw from gamma distribution
        """
        shape , rate = (beta**2)/(self.jumping_std**2) , beta/(self.jumping_std**2) 
        scale = 1/rate 
        log_density = scipy.stats.gamma.logpdf(beta,a=shape,scale=scale) 
        return log_density 

    def gamma_generator(self, beta : float, tolerance : float = 0.001) -> float: 
        """
        Generate samples from Gamma(shape,rate). If the random sampler returns a value less than 
        tolerance, return the tolerance value instead.

        parameters
        ----------
        beta : float 
            inverse temperature 

        tolerance : float 
            lowest possible return value

        Returns
        -------
        proposal_beta : float 
            random draw from Gamma(shape,rate) 
        """
        shape , rate = (beta**2)/(self.jumping_std**2) , beta/(self.jumping_std**2) 
        scale = 1/rate 
        proposal_beta = self.random_state.gamma(shape,scale) 
        if proposal_beta < tolerance:
            return tolerance

        else: 
            return proposal_beta 
    
    def next_beta(self,beta: float) -> float: 
        """ 
        Get the next beta in the markov chain using a gamma distribution as the proposal distibution.

        parameters
        ----------
        beta : float 
            inverse temperature 

        Returns
        -------
        beta : float
            the next value in the markov chain {beta_0 , beta_1 , ...} 
        """
        proposal_beta = self.gamma_generator(beta) 
        initial_likelihood = self.log_likelihood(beta) 
        proposal_likelihood = self.log_likelihood(proposal_beta) 
        initial_jump_log_dist = self.log_jumping_dist(proposal_beta) 
        proposal_jump_log_dist = self.log_jumping_dist(beta) 
        log_ratio = proposal_likelihood + self.gamma_log_prior(proposal_beta) - proposal_jump_log_dist - initial_likelihood - self.gamma_log_prior(beta) + initial_jump_log_dist  #ratio of log(p(beta|Z))/jumping_dist (Metropolis Hastings) 
        if np.log(self.random_state.uniform(0,1)) < min(0,log_ratio):  
            return proposal_beta
        else: 
            return beta 

    def gibbs_sample(self) -> list:
        """ 
        Starting from self.initial_beta, obtain self.num_samples samples from the 
        conditional distribution p(beta|Z) using metropolis-hastings sampling. 

        parameters
        ----------

        Returns
        -------
        beta_list : list 
            the Markov chain of beta samples
        """
        beta_list = [] 
        beta_t1 = self.initial_beta 
        for _ in range(self.num_samples):   
            next_beta = self.next_beta(beta_t1) 
            beta_list.append(next_beta)
            beta_t1 = next_beta 

        return beta_list 

    def simulated_Z(self, beta : float, numsweeps : int = 1) -> list: 
        """ 
        Get Simulated data Z ~ p(Z|beta) 

        parameters
        ----------
        beta : float 
            inverse temperature 

        numsweeps : int
            the number of samples to generate from p(Z|beta)

        Returns
        -------
        Z : np.ndarray
            a sample from p(Z|beta)
        """
        Z = ising_point_estimate(self.random_state,self.lattice_length,numsweeps,RELAX_SWEEPS=10,beta=beta)
        return Z 

    def SVE_next_beta(self, beta : float, numsweeps : int = 1) -> list: 
        """ 
        Get the next beta in the markov chain using a gamma distribution as the proposal distibution
        and using Single Variable Exchange (SVE).

        parameters
        ----------
        beta : float 
            inverse temperature 

        numsweeps : int
            For each SVE ratio calculation, simulate numsweeps fake data Z ~ p(Z|beta^{*})
            and use the final value of Z in the ratio calculation

        Returns
        -------
        beta : float
            the next value in the markov chain {beta_0 , beta_1 , ...}  
        """
        proposal_beta = self.gamma_generator(beta) 
        simulated_Z = self.simulated_Z(proposal_beta) 
        H_simulation = self.hamiltonian_simulated_Z(simulated_Z)
        initial_jump_log_dist = self.log_jumping_dist(proposal_beta) 
        proposal_jump_log_dist = self.log_jumping_dist(beta) 
        log_ratio = (proposal_beta - beta)*self.hamiltonian() +(beta - proposal_beta)*H_simulation + self.gamma_log_prior(proposal_beta) - proposal_jump_log_dist - self.gamma_log_prior(beta) + initial_jump_log_dist  #SVE ratio 
        if np.log(self.random_state.uniform(0,1)) < min(0,log_ratio):  
            return proposal_beta
        else: 
            return beta 

    def SVE_samples(self, numsweeps : int = 1) -> list: 
        """ 
        Starting from self.initial_beta, obtain self.num_samples samples from the 
        conditional distribution p(beta|Z) using Single Variable Exchange. 

        parameters
        ----------
        numsweeps : int
            For each SVE ratio calculation, simulate numsweeps fake data Z ~ p(Z|beta^{*})
            and use the final value of Z in the ratio calculation

        Returns
        -------
        beta_list : list 
            the Markov chain of beta samples
        """
        beta_list = [] 
        beta_t1 = self.initial_beta 
        for _ in range(self.num_samples):   
            next_beta = self.SVE_next_beta(beta_t1) 
            beta_list.append(next_beta)
            beta_t1 = next_beta 

        return beta_list

    def hist_plot(self, beta_list : list, num_bins : int = 50) -> plt.axes:
        """
        Return a histogram of the sampled betas along with a line plot of the (normalized)
        probability density function.

        parameters
        ----------
        beta_list : list 
            the Markov chain of beta samples

        num_bins : float 
            number of bins in histogram

        Returns
        -------
        plot

        """
        count, bins, ignored = plt.hist(beta_list, num_bins, density=True, align='mid') #histogram of pixel samples
        bin_width = bins[-1]-bins[-2]
        x_plus_half = [bins[k] + bin_width/2 for k in range(len(bins))]  
        H = self.hamiltonian()
        prob_x = np.array([np.exp(x*H - self.log_partition(x)) for x in x_plus_half])
        normalising_constant = 1/(bin_width*np.sum(prob_x))
        normalized_prob_x = normalising_constant*prob_x 
        plot = plt.plot(x_plus_half, normalized_prob_x, linewidth=2, color='g')
        plt.title('Sampling of p(beta|Z)') 
        plt.ylabel('p(beta|Z)') 
        return plot


class Sample_Z():
    def __init__(
        self,
        random_state : np.random.RandomState, 
        initial_Z : np.ndarray,
        beta : float, 
        lam_b : float,
        lam_e : float,
        y : np.ndarray,
        penalty_probability : float = 0.01,
        source_prior_shape : float = 20,
        source_prior_rate : float = 1,
        background_prior_shape : float = 1,
        background_prior_rate : float = 1,
        num_samples: int = 100
    ) -> None:
        """
        Parameters
        ----------
        random_state : np.random.RandomState
            Random State object. The seed value is set by the user upon instantiation of the Random State object. 

        initial_Z : np.ndarray
            Starting value of the Markov Chain for Z

        beta : float
            The inverse temperature of the Ising distribution from which Z is sampled 

        lam_b : float
            The expected counts (Poisson rate) in the background region (z==-1)

        lam_e : float
            The expected counts (Poisson rate) in the extended source region (z==1)

        y : np.ndarray
            The counts in the IDEAL image. If the PSF is taken into account, this is NOT the data. 

        source_prior_shape : float 
            The expected counts (Poisson rate) in the extended source region has a gamma prior. This is its shape.

        source_prior_rate : float 
            The expected counts (Poisson rate) in the extended source region has a gamma prior. This is its rate.

        background_prior_shape : float 
            The expected counts (Poisson rate) in the background region has a gamma prior. This is its shape.

        background_prior_rate : float 
            The expected counts (Poisson rate) in the background region has a gamma prior. This is its rate.

        num_samples: int 
            Length of the Markov Chain for Z 
        """

        self.random_state = random_state 
        self.initial_Z = initial_Z 
        self.beta = beta 
        self.lam_b = lam_b
        self.lam_e = lam_e 
        self.y = y 
        self.penalty_probability = penalty_probability
        self.source_prior_shape = source_prior_shape 
        self.source_prior_rate = source_prior_rate
        self.background_prior_shape = background_prior_shape
        self.background_prior_rate = background_prior_rate
        self.num_samples=num_samples 
        self.source_prior_scale = 1/source_prior_rate 
        self.background_prior_scale = 1/background_prior_rate
        self.L = len(initial_Z)   


    def __str__(self) -> str:
        message=(f"random_state={self.random_state}, "
                f"Sample_Z(initial_Z.shape={self.initial_Z.shape}, "
                f"beta={self.beta}, "
                f"lam_e={self.lam_e}, "
                f"lam_b={self.lam_b}, "
                f"penalty_probability={self.penalty_probability}, "
                f"source_prior_shape={self.source_prior_shape}, "
                f"source_prior_rate={self.source_prior_rate}, "
                f"background_prior_shape={self.background_prior_shape}, "
                f"background_prior_rate={self.background_prior_rate}, "
                f"num_samples={self.num_samples})" )
        return message 

    def am_I_bonded(self,Z : np.ndarray, site1 : tuple, site2 : tuple) -> Boolean:
        """
        Determine if two neighbouring lattice sites have a bond between them 

        Parameters
        ----------
        Z : numpy array 
            a sample from p(Z|beta) 
        site1 : tuple 
            coordinates (i.j) of a site on Z 
        site2 : tuple 
            one of site1's nearest neighbours 

        Returns:
        --------
        True/False : boolean
        """
        if Z[site1]==Z[site2] and (1-np.exp(- self.beta)) > self.random_state.uniform(0,1): 
            return True
        else:
            return False 

    def get_island(self,Z : np.ndarray ,i : int, j : int, visited : np.ndarray) -> np.ndarray:
        """
        Starting from a given lattice site (root=(i,j)), find all other sites that form a bond cluster/island with root,
        and return their locations in a list.

        Parameters
        ----------
        Z : numpy array 
            sample from p(Z|beta)  
        i : int
            x-coordinate on Z of starting site
        j : int
            y-coordinate on Z of starting site 
        visited: numpy array 
            a mask of shape Z.shape with 0's corresponding to lattice sites that have not been added to a bond cluster yet

        Returns:
        --------
        island_mask : numpy array 
            a mask where 1's represent one cluster of bonded sites 
        """
        L = len(Z) #lattice length 
        visited[i,j] = 1
        island_mask = np.zeros((L,L))
        island_mask[i,j] = 1 
        neighbours = [((i+1)%L,j) , (i,(j+1)%L) , ((i-1)%L,j) , (i,(j-1)%L)] 

        for index in neighbours: 
            if visited[index] == 1:
                continue 
            else:
                truth_val = self.am_I_bonded(Z,(i,j),index) 
                if truth_val:  
                    island_mask += self.get_island(Z,index[0],index[1],visited)
                else: 
                    continue 

        return island_mask  

    
    def prob_island_is_ones(self, island_mask : np.ndarray) -> float:
        """
        Get the probability that a given island flips to/remains as all 1's in the next Gibbs sample.

        Parameters
        ---------- 

        island_mask : numpy array 
            a mask where 1's represent one cluster of bonded sites 

        Returns:
        --------
        p_plus : float 
            the probability of the Z-island being 1's. 
        """
        num_sites_in_cluster = np.sum(island_mask)
        sum_cluster_data = np.sum(np.where(island_mask==1,self.y,0)) 
        log_lam_ratio_term = sum_cluster_data *np.log((self.lam_b/self.lam_e))
        log_exponential_term = num_sites_in_cluster*(self.lam_e-self.lam_b)
        log_p_ratio = log_lam_ratio_term + log_exponential_term
        p_ratio = np.exp(log_p_ratio)
        penalty = 1/self.penalty_probability -1 
        p_ratio = penalty*p_ratio 
        # penalty_term = (1/((self.penalty_probability)*(1-self.penalty_probability)))**(num_sites_in_cluster)
        # p_ratio = (np.prod((self.lam_b/self.lam_e)**(np.where(island_mask==1,self.y,0))))*np.exp(num_sites_in_cluster*(self.lam_e-self.lam_b))*penalty_term #p_minus/p_plus in Katy McKeough's paper
        p_plus = 1/(1+p_ratio) 
        # p_plus = p_plus*self.penalty_probability

        return p_plus 

    def log_prob_island_is_ones(self, island_mask : np.ndarray) -> float:
        """
        Get the log probability that a given island flips to/remains as all 1's in the next Gibbs sample.

        Parameters
        ---------- 

        island_mask : numpy array 
            a mask where 1's represent one cluster of bonded sites 

        Returns:
        --------
        log_p_plus : float 
            the log probability of the Z-island being 1's. 
        """
        num_sites_in_cluster = np.sum(island_mask)
        log_p_plus = np.log(self.prob_island_is_ones(island_mask)) + np.log(self.penalty_probability) 
        return log_p_plus 





    def flip_island(self, Z : np.ndarray, island_mask : np.ndarray) -> np.ndarray:
        """
        Change the Z values in the island_mask to +1 with probability given by prob_island_is_ones(). 

        Parameters
        ----------
        Z : numpy array 
            sample from p(Z|beta)

        island_mask : numpy array 
            a mask where 1's represent one cluster of bonded sites 

        Returns:
        --------
        new_Z : numpy array 
            The sites in Z corresponding to island_mask are changed with a certain probability. 
            All values outside of island_mask remain the same
        """
        # log_prob_ones = self.log_prob_island_is_ones(island_mask) 
        prob_ones = self.prob_island_is_ones(island_mask) 
        if prob_ones > self.random_state.uniform(0,1): 
            new_Z = np.where(island_mask==1,1,Z) 
            return new_Z
        else:
            new_Z = np.where(island_mask==1,-1,Z) 
            return new_Z 


    def Z_update(self, Z : np.ndarray) -> np.ndarray:
        """
        Do a single update of an input Z following a modified Swendsen-Wang update procedure. 

        Parameters
        ----------
        Z : numpy array 
            sample from p(Z|beta)

        Returns
        -------
        Z_new : numpy array 
            The updated Z array - shape is still (L,L) 
        """
        L = len(Z) #lattice length 
        visited = np.zeros((L,L)) #array to track sites that haven't been assigned an island yet. 1 corresponds to sites that have been visited 
        Z_new = Z 
        for ix in range(L):
            for iy in range(L): 
                if visited[ix,iy]==0:
                    island = self.get_island(Z_new,ix,iy,visited)
                    updated_Z = self.flip_island(Z_new,island) 
                    Z_new = updated_Z
                    visited = np.where(island==1,1,visited) 

        return Z_new

    def Z_chain(self) -> np.ndarray:
        """
        Do num_samples Swendsen-Wang updates to Z_initial, store each update, 
        and return the samples.

        Parameters
        ---------- 

        Returns : np.ndarray
            array of size (self.numsamples,L,L) 
        """

        store_of_samples = np.zeros((self.num_samples,self.L,self.L)) 
        current_Z = self.initial_Z
        store_of_samples[0,:,:] = current_Z
        for k in range(self.num_samples - 1): 
            next_Z = self.Z_update(current_Z)
            store_of_samples[k+1,:,:] = next_Z 
            current_Z = next_Z 

        return store_of_samples 

    def plot_array(input_array:np.ndarray, title:str) -> plt.axes:
        """
        get heatmap of input array
        """
        ax = sns.heatmap(input_array, annot=False) 
        ax.set_title(title)
        return ax 




class Sample_lambda(): 

    def __init__(
        self, 
        random_state,
        data: np.ndarray,
        Z : np.ndarray,
        source_prior_shape : float = 20,
        source_prior_rate : float = 1,
        background_prior_shape : float = 1,
        background_prior_rate : float = 1,
        num_samples: int = 100
    ) -> None:

        self.random_state = random_state 
        self.data = data 
        self.Z = Z
        self.source_prior_shape = source_prior_shape 
        self.source_prior_rate = source_prior_rate
        self.background_prior_shape = background_prior_shape
        self.background_prior_rate = background_prior_rate
        self.num_samples=num_samples 
        self.source_prior_scale = 1/source_prior_rate 
        self.background_prior_scale = 1/background_prior_rate
        self.L = len(data)


    def __str__(self) -> str:
        message=(f"random_state={self.random_state}, "
                f"Sample_lambda(data.shape={self.data.shape}, "
                f"Z.shape={self.Z.shape}, "
                f"source_prior_shape={self.source_prior_shape}, "
                f"source_prior_rate={self.source_prior_rate}, "
                f"background_prior_shape={self.background_prior_shape}, "
                f"background_prior_rate={self.background_prior_rate}, "
                f"num_samples={self.num_samples})" )
        return message 

    @property 
    def n1(self) -> int:
        """ 
        Return the number of ones in self.Z
        """
        n1 = (self.Z == 1).sum() 
        return n1 

    @property 
    def n_minus1(self) -> int:
        """ 
        Return the number of -1 in self.Z
        """
        n_minus1 = (self.Z == -1).sum() 
        return n_minus1 

    @property
    def sum_data_plus(self) -> int: 
        """ 
        Return the sum of all data with corresponding Z = 1.
        """
        count = self.data[self.Z == 1].sum() 
        return count 

    @property
    def sum_data_minus(self) -> int: 
        """ 
        Return the sum of all data with corresponding Z = -1.
        """
        count = self.data[self.Z == -1].sum() 
        return count

    def lambda_b_sample(self) -> np.ndarray: 
        """ 
        Draw self.num_samples from p(lambda_b|data,Z)
        """

        background_posterior = self.random_state.gamma(self.sum_data_minus+self.background_prior_shape,1/(self.n_minus1 + self.background_prior_rate),(self.num_samples)) 

        return background_posterior 

    def lambda_e_sample(self) -> np.ndarray: 
        """ 
        Draw self.num_samples from p(lambda_e|data,Z)
        """

        source_posterior = self.random_state.gamma(self.sum_data_plus+self.source_prior_shape,1/(self.n1 + self.source_prior_rate),(self.num_samples)) 


        return source_posterior


def subtract_psf4(random_state,y:np.ndarray,psf:np.ndarray,Z:np.ndarray,lam_b:float,lam_e:float,**kwargs)->np.ndarray:
    """ 
    Remove the blurring due to the PSF from the data, y. 

    Parameters
    ----------
    random_state : np.random.RandomState
            Random State object. The seed value is set by the user upon instantiation of the Random State object. 

    y:np.ndarray 
        data 

    psf:np.ndarray 
        normalised point spread function. Not necessarily the same size as y - it can be smaller but not larger than y.shape 

    Z:np.ndarray
        Sample from the Ising distribution 

    lam_b:float
        Expected counts in the Background region

    lam_e:float
        Expected counts in the extended source region

    lam_ps:float 
        Expected additional counts in the point source pixel due to the point source 

    ps_loc : tuple 
        location of the point source in the data

    Returns
    -------
    X_ideal : np.dnarray 
        Matrix of counts in the ideal image 
    
    """ 
    L = len(y) 
    L_psf = len(psf)  
    lam_array = np.where(Z==1,lam_e,lam_b) 

    if 'lam_ps' and 'ps_loc' in kwargs: 
        lam_ps = kwargs['lam_ps']
        ps_loc = kwargs['ps_loc'] 
        lam_array[ps_loc] += lam_ps 

    psf_centre_length = int(L_psf/2) 

    X_ideal = np.zeros((L,L)) 


    for row in range(L):
        for col in range(L):
            psf_inv = np.zeros((L_psf,L_psf)) #inverse psf: psf_inv[k][l] is the probability that a photon that landed at (i,j) came from (k,l) 
            for k in range(L_psf):
                for l in range(L_psf):
                    psf_inv[k][l] +=lam_array[(row - psf_centre_length +k)%L,(col-psf_centre_length+l)%L]*psf[L_psf-1-k,L_psf-1-l] 
            normalisation = np.sum(psf_inv)
            psf_inv = psf_inv/normalisation
            flat_psf_inv = np.reshape(psf_inv,(L_psf**2)) 
            redistributed_counts = random_state.multinomial(y[row][col],flat_psf_inv)
            redistributed_counts_2D = np.reshape(redistributed_counts,(L_psf,L_psf)) 
            redistributed_counts_2D_padded = np.pad(redistributed_counts_2D,((0,L-L_psf),(0,L-L_psf))) 
            redistributed_counts_2D_padded_rolled = np.roll(redistributed_counts_2D_padded,((col-psf_centre_length),(row-psf_centre_length)),axis=(1,0))            
            X_ideal+= redistributed_counts_2D_padded_rolled


    return X_ideal 

            
