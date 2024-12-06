# -*- coding: utf-8 -*-
# Copyright 2024 - Michaël Baudin.
"""
References
----------
Adaptive numerical differentiation
R. S. Stepleman and N. D. Winarsky
Journal: Math. Comp. 33 (1979), 1257-1264 
"""

import numpy as np
from .NumericalDerivative import NumericalDerivative
from .FiniteDifferenceFormula import FiniteDifferenceFormula


class SteplemanWinarsky(NumericalDerivative):
    def __init__(
        self, function, x, relative_precision=1.0e-16, args=None, verbose=False
    ):
        """
        Use Stepleman & Winarsky method to compute the optimum step size for the first derivative.

        Uses centered finite difference to compute an approximate value of f'(x).
        The approximate optimal step for f'(x) is computed using a monotony property.

        The central F.D. is:

        f'(x) ~ (f(x + h) - f(x - h)) / (2 * h)

        Parameters
        ----------
        function : function
            The function to differentiate.
        x : float
            The point where the derivative is to be evaluated.
        relative_precision : float, > 0, optional
            The relative precision of evaluation of f. The default is 1.0e-16.
        args : list
            A list of optional arguments that the function takes as inputs.
            By default, there is no extra argument and calling sequence of
            the function must be y = function(x).
            If there are extra arguments, then the calling sequence of
            the function must be y = function(x, arg1, arg2, ...) where
            arg1, arg2, ..., are the items in the args list.
        verbose : bool, optional
            Set to True to print intermediate messages. The default is False.

        Returns
        -------
        None.

        """
        if relative_precision <= 0.0:
            raise ValueError(
                f"The absolute precision must be > 0. "
                f"here precision = {relative_precision}"
            )
        self.relative_precision = relative_precision
        self.verbose = verbose
        self.finite_difference = FiniteDifferenceFormula(function, x, args)
        super().__init__(function, x, args)
        return

    def compute_step(self, initial_step=None, iteration_maximum=53, beta=4.0):
        """
        Compute an approximate optimum step for central derivative using monotony properties.

        This function computes an approximate optimal step h for the central
        finite difference.

        Parameters
        ----------
        initial_step : float, > 0.0
            The initial value of the differentiation step.
            The default initial step is beta * relative_error**(1/3) * abs(x)
        iteration_maximum : int, optional
            The number of iterations. The default is 53.
        beta : float, > 1.0
            The reduction factor of h at each iteration.

        Returns
        -------
        estim_step : float
            A step size which is near to optimal.
        number_of_iterations : int
            The number of iterations required to reach that optimum.

        """
        if self.verbose:
            print("+ search_step_using_motony()")
        if beta <= 1.0:
            raise ValueError(f"beta must be greater than 1. Here beta = {beta}.")
        if initial_step is None:
            # eq. 3.9 page 1261
            initial_step = beta * self.relative_precision ** (1.0 / 3.0) * abs(self.x)
        if initial_step <= 0.0:
            raise ValueError(
                f"initial_step must be greater than 0. Here initial_step = {initial_step}."
            )
        if iteration_maximum <= 0:
            raise ValueError(
                f"iteration_maximum must be greater than 0. "
                f"Here iteration_maximum = {iteration_maximum}."
            )
        if self.verbose:
            print(f"initial_step={initial_step:.3e}")
        h_previous = initial_step
        f_prime_approx_previous = (
            self.finite_difference.compute_first_derivative_central(h_previous)
        )
        diff_previous = np.inf
        estim_step = 0.0
        found_monotony_break = False
        for number_of_iterations in range(iteration_maximum):
            h_current = h_previous / beta
            f_prime_approx_current = (
                self.finite_difference.compute_first_derivative_central(h_current)
            )
            # eq. 2.3
            diff_current = abs(f_prime_approx_current - f_prime_approx_previous)
            if self.verbose:
                print(
                    "number_of_iterations=%d, h=%.4e, |FD(h_current) - FD(h_previous)|=%.4e"
                    % (number_of_iterations, h_current, diff_current)
                )
            if diff_current == 0.0:
                if self.verbose:
                    print("Stop because zero difference.")
                found_monotony_break = True
                # Zero difference achieved at step h : go back one step
                estim_step = h_current * beta
                break

            if diff_previous < diff_current:
                if self.verbose:
                    print("Stop because no monotony anymore.")
                found_monotony_break = True
                # Monotony breaked at step h : go back one step
                estim_step = h_current * beta
                break

            f_prime_approx_previous = f_prime_approx_current
            h_previous = h_current
            diff_previous = diff_current

        if not found_monotony_break:
            raise ValueError(
                "No monotony break was found after %d iterations." % (iteration_maximum)
            )
        return estim_step, number_of_iterations

    def number_of_lost_digits(self, h):
        """
        Compute the number of (base 10) lost digits.

        Parameters
        ----------
        h : float
            Differentiation step.

        Returns
        -------
        number_of_digits : float
            The number of digits lost by cancellation.

        """
        d = self.finite_difference.compute_first_derivative_central(h)
        function_value = self.function_eval(self.x)
        # eq. 3.10
        if function_value == 0.0:
            delta = abs(2 * h * d)
        else:
            delta = abs(2 * h * d / function_value)
        # eq. 3.11
        number_of_digits = -np.log10(delta)
        return number_of_digits

    def search_step_with_bisection(
        self,
        bracket_initial_step,
        maximum_bisection=53,
        beta=4.0,
        log_scale=True,
    ):
        """
        Compute the initial step using bisection.

        The initial step initial_step is chosen so that:

            0 < N(initial_step) < T := log10(precision ** (-1.0 / 3.0) / beta)

        This algorithm can be effective compared to search_step_using_motony()
        in the cases where it is difficult to find an initial step.
        In this case, the step returned by search_step_with_bisection()
        can be used as the initial step for search_step_using_motony().
        This can be costly.

        This algorithm can fail if the required finite difference step is
        so large that the points x+/-h fall beyond the mathematical input
        domain of the function.

        Parameters
        ----------
        bracket_initial_step : [h_min, h_max]
            The bounds to bracket the initial differentiation step.
            We must have N(h_min) > N(h_max) where N is the number of lost digits.
        maximum_bisection : int, optional
            The maximum number of bisection iterations. The default is 53.
        beta : float, > 1, optional
            The reduction of h at each iteration. The default is 4.0.
        log_scale : bool, optional
            Set to True to bisect in log scale. The default is True.

        Returns
        -------
        initial_step : float
            The initial step.
        number_of_iterations : int
            The number of required iterations.

        """
        if self.verbose:
            print("+ search_step_with_bisection()")
        h_min, h_max = bracket_initial_step
        if h_min >= h_max:
            raise ValueError(
                f"h_min  = {h_min} > h_max = {h_max}." "Please change the bounds."
            )
        if beta <= 1.0:
            raise ValueError(f"beta must be greater than 1. Here beta = {beta}.")
        if self.verbose:
            print(f"+ h_min = {h_min:.3e}, h_max = {h_max:.3e}")
        # eq. 3.15
        if self.verbose:
            print(f"+ relative_precision = {self.relative_precision:.3e}")
        # eq. 3.15
        n_treshold = np.log10(self.relative_precision ** (-1.0 / 3.0) / beta)
        if n_treshold <= 0.0:
            raise ValueError(
                f"The upper bound of the number of lost digits is {n_treshold} <= 0.0."
                " Increase absolute precision."
            )
        n_min = self.number_of_lost_digits(h_min)
        if n_min < 0.0:
            raise ValueError(
                f"The number of lost digits for h_min is {n_min} < 0." " Reduce h_min."
            )
        if n_min >= 0.0 and n_min <= n_treshold:
            initial_step = h_min
            number_of_iterations = 0
            return initial_step, number_of_iterations

        n_max = self.number_of_lost_digits(h_max)
        if self.verbose:
            print(
                f"n_min = {n_min:.3f}, "
                f"n_treshold = {n_treshold:.3f}, "
                f"n_max = {n_max:.3f}"
            )
        if n_max > n_treshold:
            raise ValueError(
                f"The number of lost digits for h_max is {n_max} > {n_treshold}."
                " Increase h_max or decrease relative_precision."
            )
        if n_max >= 0.0 and n_max <= n_treshold:
            initial_step = h_max
            number_of_iterations = 0
            return initial_step, number_of_iterations

        if n_min < n_max:
            raise ValueError("N(h_min) < N(h_max)")

        # Now : n_min > n_treshold > 0 > n_max
        found = False
        for number_of_iterations in range(maximum_bisection):
            if self.verbose:
                print(
                    f"+ Iter {number_of_iterations} / {maximum_bisection}, "
                    f"h_min = {h_min:.3e}, "
                    f"h_max = {h_max:.3e}"
                )
            if log_scale:
                initial_step = 10 ** ((np.log10(h_max) + np.log10(h_min)) / 2.0)
            else:
                initial_step = (h_max + h_min) / 2.0
            n_digits = self.number_of_lost_digits(initial_step)
            if self.verbose:
                print(
                    f"  h = {initial_step:.3e}, "
                    f"  Number of lost digits = {n_digits:.3f}"
                )
            if n_digits > 0 and n_digits < n_treshold:
                found = True
                if self.verbose:
                    print("  h is just right : stop !")
                break
            elif n_digits < 0.0:
                if self.verbose:
                    print("  h is too large: reduce it")
                h_max = initial_step
            else:
                if self.verbose:
                    print("  h is small: increase it")
                h_min = initial_step
        if not found:
            raise ValueError(
                "The maximum number of bisection "
                f"iterations {maximum_bisection} has been reached."
            )
        return initial_step, number_of_iterations

    def compute_first_derivative(self, step):
        """
        Compute an approximate value of f'(x) using centered finite difference.

        The denominator is, however, implemented using the equation 3.4
        in Stepleman & Winarsky (1979).

        Parameters
        ----------
        step : float, > 0
            The step size.

        Returns
        -------
        f_prime_approx : float
            The approximation of f'(x).
        """
        f_prime_approx = self.finite_difference.compute_first_derivative_central(step)
        return f_prime_approx

    def get_number_of_function_evaluations(self):
        """
        Returns the number of function evaluations.

        Returns
        ----------
        number_of_function_evaluations : int
            The number of function evaluations.
        """
        finite_difference_feval = (
            self.finite_difference.get_number_of_function_evaluations()
        )
        total_feval = finite_difference_feval + self.number_of_function_evaluations
        return total_feval
