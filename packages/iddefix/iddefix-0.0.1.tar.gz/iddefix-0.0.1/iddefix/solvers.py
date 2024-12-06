#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:33:41 2020

@author: sjoly
"""
import sys
import numpy as np
from scipy.optimize import differential_evolution

def progress_bar_gui(total, progress, extra=""):
    """Displays or updates a console progress bar.

    Args:
        total (int): The total number of steps in the algorithm.
        progress (int): The current progress (number of completed steps).
        extra (str, optional): An extra string to append to the progress bar. Defaults to "".

    Original source: https://stackoverflow.com/a/15860757/1391441
    """

    bar_length = 20  # Set constant bar length
    completed_blocks = int(round(bar_length * progress / total))
    remaining_blocks = bar_length - completed_blocks
    progress_percentage = round(progress / total * 100, 0)
    progress_percentage = int(progress / total * 100)

    # Build the progress bar string with different symbols
    symbols = ['#', '-']  # Define progress and remaining symbols
    progress_bar = "[" + ''.join(completed_blocks * symbols[0] + remaining_blocks * symbols[1]) + "]"
    status = f"\rProgress: {progress_bar} {progress_percentage}% {extra}"

    # Update the progress bar with a newline when reaching 100%
    if progress_percentage >= 100:
        status = f"\rProgress: {progress_bar} {100}% {extra}" + "\n"

    sys.stdout.write(status)
    sys.stdout.flush()
    
def show_progress_bar(x, convergence, *karg):
    """
    Callback function to display a progress bar with scipy.
    """
    progress_bar_gui(1, convergence, extra="")
    
def stop_criterion(solver):
    '''
    Based on the criterion used in scipy.optimize.differential_evolution 
    (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html)
    Check that the ratio of the spread of the population fitness compared to its average.
    In other words, if most of the population individuals converge to the same solution indicating
    an optimal solution has been found.
    '''
    population_cost = np.vstack(solver)[:,1]
    population_mean, population_std = np.mean(population_cost), np.std(population_cost)
    criterion = population_std / np.abs(population_mean)
    return criterion

class Solvers:
    def run_scipy_solver(parameterBounds, 
                        minimization_function,
                        maxiter=2000, 
                        popsize=150, 
                        mutation=(0.1, 0.5), 
                        crossover_rate=0.8,
                        tol=0.01,
                        **kwargs):
        """
        Runs the SciPy differential_evolution solver to minimize a given function.
        
        All the arguments are detailed on this page :
        (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html)
        Setting workers= -1 means all CPUs available will be used for the computation.
        Default parameters used for the DE algorithm taken from https://www.mdpi.com/2227-7390/9/4/427

        Args:
            parameterBounds: A list of tuples representing the upper and lower bounds for each parameter.
            minimization_function: The function to be minimized.
            maxiter: The maximum number of iterations to run the solver for.
            popsize: The population size for the differential evolution algorithm.
            mutation: A tuple of two floats representing the mutation factors.
            crossover_rate: The crossover rate for the differential evolution algorithm.
            tol: The tolerance for convergence.

        Returns:
            A tuple containing:
                - The solution found by the solver.
                - A message indicating the solver's status.
        """    
        result = differential_evolution(minimization_function, 
                                        parameterBounds, 
                                        popsize=popsize, 
                                        tol=tol, 
                                        maxiter=maxiter,
                                        mutation=mutation, 
                                        recombination=crossover_rate, 
                                        polish=False, 
                                        init='latinhypercube',
                                        strategy='rand1bin',
                                        callback=show_progress_bar,
                                        updating='deferred', 
                                        workers=-1, #vectorized=vectorized
                                    )
        
        # Need to be reworked to use the last population as the new initial population to speed up convergence
        """while ((result.message == 'Maximum number of iterations has been exceeded.') and (iteration_convergence)):
            warning = 'Increased number of iterations by 10% to reach convergence. \n'
            maxiter = int(1.1*maxiter)
            result = differential_evolution(minimization_function,parameterBounds, 
                                            popsize=popsize, tol=tol, maxiter=maxiter,
                                            mutation=mutation, recombination=crossover_rate, polish=False, 
                                            init='latinhypercube',
                                            callback=show_progress_bar,
                                            updating='deferred', workers=-1, #vectorized=vectorized
                                        )

        else:
            warning = ''
        """
        
        solution, message = result.x, result.message

        return solution, message


    def run_pyfde_solver(parameterBounds, 
                        minimization_function,
                        maxiter=2000, 
                        popsize=150, 
                        mutation=(0.45), 
                        crossover_rate=0.8,
                        tol=0.01,
                        **kwargs):
        """
        Runs the pyfde ClassicDE solver to minimize a given function.

        Args:
            parameterBounds: A list of tuples representing the bounds for each parameter.
            minimization_function: The function to be minimized.
            maxiter: The maximum number of iterations to run the solver for.
            popsize: The population size for the differential evolution algorithm.
            mutation: A tuple of two floats representing the mutation factors.
            crossover_rate: The crossover rate for the differential evolution algorithm.
            tol: The tolerance for convergence.

        Returns:
            A tuple containing:
                - The solution found by the solver.
                - A message indicating the solver's status.
        """
        try:
            from pyfde import ClassicDE
        except:
            raise ImportError("Please install the pyfde package to use the pyfde solvers.")
        
        solver = ClassicDE(
            minimization_function,
            n_dim=len(parameterBounds),
            n_pop=popsize * len(parameterBounds),
            limits=parameterBounds,
            minimize=True,
        )    
        solver.cr, solver.f = crossover_rate, np.mean(np.atleast_1d(mutation))

        for i in range(maxiter):
            best, _ = solver.run(n_it=1)
            progress_bar_gui(1, np.max((tol / stop_criterion(solver), i / maxiter)))
            if stop_criterion(solver) < tol:
                break

        solution, message = best, "Convergence achieved" if i < maxiter else "Maximum iterations reached"

        return solution, message

    def run_pyfde_jade_solver(parameterBounds, 
                            minimization_function,
                            maxiter=2000, 
                            popsize=150, 
                            tol=0.01,
                            **kwargs):
        """
        Runs the pyfde JADE solver to minimize a given function.

        Args:
            parameterBounds: A list of tuples representing the bounds for each parameter.
            minimization_function: The function to be minimized.
            maxiter: The maximum number of iterations to run the solver for.
            popsize: The population size for the differential evolution algorithm.
            tol: The tolerance for convergence.

        Returns:
            A tuple containing:
                - The solution found by the solver.
                - A message indicating the solver's status.
        """

        try:
            from pyfde import JADE
        except:
            raise ImportError("Please install the pyfde package to use the pyfde solvers.")
        
        solver = JADE(
            minimization_function,
            n_dim=len(parameterBounds),
            n_pop=popsize * len(parameterBounds),
            limits=parameterBounds,
            minimize=True,
        )

        for i in range(maxiter):
            best, _ = solver.run(n_it=1)
            progress_bar_gui(1, np.max((tol / stop_criterion(solver), i / maxiter)))
            if stop_criterion(solver) < tol:
                break

        solution, message = best, "Convergence achieved" if i < maxiter else "Maximum iterations reached"

        return solution, message