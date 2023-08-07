"""
Representation of ordinary differential equations (ODE)s.

This module contains numerical integration methods that simplify the implementation of ODEs with respect to their use in
an optimization context.
"""

from typing import Any, Dict, Protocol, final, overload, Union

from casadi import casadi
from pandas import DatetimeIndex
from pydantic import root_validator
from typing_extensions import TypeAlias

from optool.conversions import any_to_intervals
from optool.core import BaseModel
from optool.fields.callables import concallable
from optool.fields.misc import NonEmptyStr
from optool.fields.quantities import QuantityLike
from optool.fields.symbolic import CasadiColumn
from optool.fields.util import validate
from optool.logging import LOGGER
from optool.math import num_elements
from optool.optimization.constraints import Equation
from optool.uom import UNITS, Quantity

OdeFunction: TypeAlias = concallable(num_params=2)  # type: ignore[valid-type]
"""A callable with two input parameters."""


class OrdinaryDifferentialEquation(BaseModel, frozen=True):
    r"""
    Representation of an ordinary differential equation (ODE).

    An ODE is described by the mathematical formula of the following form,

    $$ \dot{x} = f(x, u), $$

    where $x$ represents the state variable and $u$ the input variable that includes both controlled signals and
    disturbances.

    The corresponding implementation requires the definition of the state variable, the input variable, and the function
    $f$. The transcription then follows a multiple shooting approach, where the continuity is ensured via so-called gap
    closing constraints. In order to use the associated vector-based formulation, both $x$ and $u$ should be specified
    as column vectors, where $u$ has one element less than $x$.
    """

    name: NonEmptyStr
    """The name of the ordinary differential equation."""
    state_variable: QuantityLike[Any, CasadiColumn]
    """The array of state variables of the ordinary differential equation."""
    input_variable: QuantityLike[Any, CasadiColumn]
    """The array of input variables of the ordinary differential equation."""
    function: OdeFunction
    """The function of the ordinary differential equation."""

    @final
    @root_validator
    def _is_consistent(cls, values: Dict) -> Dict:
        name = values['name']
        function = values['function']
        state_variable = values['state_variable']
        input_variable = values['input_variable']
        num_state_variables = num_elements(state_variable)
        num_input_variables = num_elements(input_variable)

        if num_state_variables != num_input_variables + 1:
            raise ValueError(f"The vector of state variables for the ODE function {name} must have one element more "
                             f"than the vector of input variables, but have {num_state_variables=} and "
                             f"{num_input_variables=}.")

        try:
            time_derivative = function(state_variable[1:], input_variable)
        except Exception as e:
            raise ValueError(f"The given ODE function {name} failed with given state and input variables.") from e
        else:
            validate(time_derivative, [lambda x: isinstance(x, Quantity), lambda x: isinstance(x.magnitude, casadi.SX)],
                     "Result of the ODE, i.e., time-derivative")

            validate(
                time_derivative, lambda x: x.units.is_compatible_with(state_variable.units / UNITS.second),
                f"The time-derivative for the ODE function {name} has units {time_derivative.units}, which "
                f"is not compatible with the units of the state variables, i.e., '{state_variable.units}'.")

            validate(
                time_derivative, lambda x: x.size() == (num_input_variables, 1),
                f"The vector of time-derivatives for the ODE function {name} must have the same number of "
                f"elements than the vector of input variables, but have {time_derivative.numel()} and "
                f"{num_input_variables}.")

        return values


class IntegrationMethod(Protocol):
    """
    A protocol that defines the contract for methods that implement numerical integration.

    Any class that provides an implementation for this method is considered as an integration method. It will be capable
    of solving an ordinary differential equation (ODE) by numerical integration over a time horizon specified as
    timestamps.

    This protocol can be used as a type hint for functions or methods that require an integration method.
    """

    @overload
    def integrate(self, ode: OrdinaryDifferentialEquation, time_intervals: Quantity) -> Equation:
        """
        Integrate the ordinary differential equation (ODE) over a specified horizon given as a sequence of timestamps.

        :param ode: The ODE that represents the differential equation to be integrated.
        :param time_intervals: The time intervals between the samples over which to perform the integration.
        :return: The solution of the ODE after performing the numerical integration.
        """
        pass

    @overload
    def integrate(self, ode: OrdinaryDifferentialEquation, time_steps: Quantity) -> Equation:
        """
        Integrate the ordinary differential equation (ODE) over a specified horizon given as a sequence of timestamps.

        :param ode: The ODE that represents the differential equation to be integrated.
        :param time_steps: The time steps over which to perform the integration.
        :return: The solution of the ODE after performing the numerical integration.
        """
        pass

    @overload
    def integrate(self, ode: OrdinaryDifferentialEquation, timestamps: DatetimeIndex) -> Equation:
        """
        Integrate the ordinary differential equation (ODE) over a specified horizon given as a sequence of timestamps.

        :param ode: The ODE that represents the differential equation to be integrated.
        :param timestamps: The timestamps over which to perform the integration.
        :return: The solution of the ODE after performing the numerical integration.
        """
        pass

    def integrate(self, ode, time):
        pass


class ForwardEuler:
    r"""
    The Euler method for numerical integration.

    The forward Euler method, also simply referred to as the Euler method, is the most basic explicit method for
    numerical integration of ODEs and is the simplest Runge–Kutta method.

    One step of the Euler method from $i$ to $i+1$ is given by

    $$ x[i+1] = x[i] + T_s[i] \cdot f \left( x[i], u[i] \right), $$

    where $T_s[i]$ is the time between index $i$ and $i+1$.

    :::{seealso}
    [Wikipedia: Euler method](wiki:Euler_method)
    :::
    """

    @classmethod
    def integrate(cls, ode: OrdinaryDifferentialEquation, time: Union[Quantity, DatetimeIndex]) -> Equation:
        LOGGER.debug("Integrating {} with {}.", ode.name, cls.__name__)

        time_intervals = any_to_intervals(time)
        time_derivative = ode.function(ode.state_variable[1:], ode.input_variable)
        next_state = ode.state_variable[:-1] + time_intervals * time_derivative
        return Equation(name=ode.name, lhs=ode.state_variable[1:], rhs=next_state)


class RungeKutta4:
    r"""
    Fourth-order method of the Runge–Kutta for numerical integration.

    Runge-Kutta 4 is the fourth-order method of the Runge–Kutta family, which is the most widely used Runge-Kutta method
    and thus also referred to as the classic Runge–Kutta method or simply the Runge–Kutta method.

    One step of the Runge-Kutta method from $i$ to $i + 1$ is given by


    $$ x[i+1] = x[i] + \frac{1}{6}\, T_s[i] \big( k_1 + 2k_2 + 2k_3 + k_4 \big), $$

    where the parameters $k_1, \ldots, k_4$ are recursively defined as follows:

    $$
        k_1 &= f \big( x[i], u[i] \big), \\
        k_2 &= f \big( x[i] + k_1 \tfrac{T_s[i]}{2}, u[i] \big), \\
        k_3 &= f \big( x[i] + k_2 \tfrac{T_s[i]}{2}, u[i] \big), \\
        k_4 &= f \big( x[i] + k_3 T_s[i], u[i] \big).
    $$

    Note that, if the time-derivative of $x$ is not dependent on $x$ itself, i.e., $f(x,u) = f(u)$,
    all parameters above are equal, i.e., $k_1 = k_2 = k_3 = k_4$. Hence, the Runge-Kutta method is equal to the
    Euler method.

    :::{seealso}
    [Wikipedia: Runge–Kutta methods](wiki:Runge–Kutta_methods)
    :::
    """

    @classmethod
    def integrate(cls, ode: OrdinaryDifferentialEquation, time: Union[Quantity, DatetimeIndex]) -> Equation:
        LOGGER.debug("Integrating {} with {}.", ode.name, cls.__name__)

        time_intervals = any_to_intervals(time)
        k1 = ode.function(ode.state_variable[1:], ode.input_variable)
        k2 = ode.function(ode.state_variable[1:] + time_intervals / 2 * k1, ode.input_variable)
        k3 = ode.function(ode.state_variable[1:] + time_intervals / 2 * k2, ode.input_variable)
        k4 = ode.function(ode.state_variable[1:] + time_intervals * k3, ode.input_variable)
        next_state = ode.state_variable[1:] + time_intervals / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

        return Equation(name=ode.name, lhs=ode.state_variable[1:], rhs=next_state)
