from typing import Tuple

import numpy as np
from commonroad_raceline_planner.planner.ftm_planner.trajectory_planning.calc_spline_lengths import (
    calc_spline_lengths,
)
from commonroad_raceline_planner.planner.ftm_planner.trajectory_planning.interp_splines import (
    interp_splines,
)
from commonroad_raceline_planner.planner.ftm_planner.trajectory_planning.calc_splines import (
    calc_splines,
)


def create_raceline(
    refline: np.ndarray,
    normvectors: np.ndarray,
    alpha: np.ndarray,
    stepsize_interp: float,
) -> Tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """
    This function includes the algorithm part connected to the interpolation of the raceline after the optimization.

    :param refline:         array containing the track reference line [x, y] (unit is meter, must be unclosed!)
    :param normvectors:     normalized normal vectors for every point of the reference line [x_component, y_component]
                            (unit is meter, must be unclosed!)
    :param alpha:           solution vector of the optimization problem containing the lateral shift in m for every point.
    :param stepsize_interp: stepsize in meters which is used for the interpolation after the raceline creation.
    :return raceline_interp:                interpolated raceline [x, y] in m.
    :return A_raceline:                     linear equation system matrix of the splines on the raceline.
    :return coeffs_x_raceline:              spline coefficients of the x-component.
    :return coeffs_y_raceline:              spline coefficients of the y-component.
    :return spline_inds_raceline_interp:    contains the indices of the splines that hold the interpolated points.
    :return t_values_raceline_interp:       containts the relative spline coordinate values (t) of every point on the
                                            splines.
    :return s_raceline_interp:              total distance in m (i.e. s coordinate) up to every interpolation point.
    :return spline_lengths_raceline:        lengths of the splines on the raceline in m.
    :return el_lengths_raceline_interp_cl:  distance between every two points on interpolated raceline in m (closed!).

    """

    # TODO: here we need an open race track again

    # calculate raceline on the basis of the optimized alpha values
    raceline = refline + np.expand_dims(alpha, 1) * normvectors

    # calculate new splines on the basis of the raceline
    raceline_cl = np.vstack((raceline, raceline[0]))

    coeffs_x_raceline, coeffs_y_raceline, A_raceline, normvectors_raceline = (
        calc_splines(path=raceline_cl, use_dist_scaling=False)
    )

    # calculate new spline lengths
    spline_lengths_raceline = calc_spline_lengths(
        coeffs_x=coeffs_x_raceline, coeffs_y=coeffs_y_raceline
    )

    # interpolate splines for evenly spaced raceline points
    (
        raceline_interp,
        spline_inds_raceline_interp,
        t_values_raceline_interp,
        s_raceline_interp,
    ) = interp_splines(
        spline_lengths=spline_lengths_raceline,
        coeffs_x=coeffs_x_raceline,
        coeffs_y=coeffs_y_raceline,
        incl_last_point=False,
        stepsize_approx=stepsize_interp,
    )

    # calculate element lengths
    s_tot_raceline = float(np.sum(spline_lengths_raceline))
    el_lengths_raceline_interp = np.diff(s_raceline_interp)
    el_lengths_raceline_interp_cl = np.append(
        el_lengths_raceline_interp, s_tot_raceline - s_raceline_interp[-1]
    )

    return (
        raceline_interp,
        A_raceline,
        coeffs_x_raceline,
        coeffs_y_raceline,
        spline_inds_raceline_interp,
        t_values_raceline_interp,
        s_raceline_interp,
        spline_lengths_raceline,
        el_lengths_raceline_interp_cl,
    )


# testing --------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
