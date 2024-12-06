from typing import Tuple
import logging

import numpy as np

from commonroad_raceline_planner.planner.ftm_planner.ftm_dto import DtoFTM

# Own code base
from commonroad_raceline_planner.planner.ftm_planner.track_processing.track_processing import (
    interp_track,
    calc_min_bound_dists,
)


def check_traj(
    reftrack: DtoFTM,
    reftrack_normvec_normalized: np.ndarray,
    trajectory: np.ndarray,
    ggv: np.ndarray,
    ax_max_machines: np.ndarray,
    v_max: float,
    length_veh: float,
    width_veh: float,
    debug: bool,
    dragcoeff: float,
    mass_veh: float,
    curvlim: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    This function checks the generated trajectory in regards of minimum distance to the boundaries and maximum
    curvature and accelerations.

    reftrack:           track [x_m, y_m, w_tr_right_m, w_tr_left_m]
    reftrack_normvec_normalized: normalized normal vectors on the reference line [x_m, y_m]
    trajectory:         trajectory to be checked [s_m, x_m, y_m, psi_rad, kappa_radpm, vx_mps, ax_mps2]
    ggv:                ggv-diagram to be applied: [vx, ax_max, ay_max]. Velocity in m/s, accelerations in m/s2.
    ax_max_machines:    longitudinal acceleration limits by the electrical motors: [vx, ax_max_machines]. Velocity
                        in m/s, accelerations in m/s2. They should be handed in without considering drag resistance.
    v_max:              Maximum longitudinal speed in m/s.
    length_veh:         vehicle length in m
    width_veh:          vehicle width in m
    debug:              boolean showing if debug messages should be printed
    dragcoeff:          [m2*kg/m3] drag coefficient containing c_w_A * rho_air * 0.5
    mass_veh:           [kg] mass
    curvlim:            [rad/m] maximum drivable curvature

    Outputs:
    bound_r:            right track boundary [x_m, y_m]
    bound_l:            left track boundary [x_m, y_m]
    """

    # ------------------------------------------------------------------------------------------------------------------
    # CHECK VEHICLE EDGES FOR MINIMUM DISTANCE TO TRACK BOUNDARIES -----------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    logger = logging.getLogger("FTMPlanner.TrajCheck")

    # calculate boundaries and interpolate them to small stepsizes (currently linear interpolation)
    bound_r = reftrack.to_2d_np_array() + reftrack_normvec_normalized * np.expand_dims(
        reftrack.w_tr_right_m, axis=1
    )
    bound_l = reftrack.to_2d_np_array() - reftrack_normvec_normalized * np.expand_dims(
        reftrack.w_tr_left_m, axis=1
    )

    # TODO: they are reusing an interpolation function for other dim here -> do own function
    # check boundaries for vehicle edges
    bound_r_tmp = np.column_stack((bound_r, np.zeros((bound_r.shape[0], 2))))
    bound_l_tmp = np.column_stack((bound_l, np.zeros((bound_l.shape[0], 2))))

    bound_r_interp = interp_track(reftrack=bound_r_tmp, stepsize_approx=1.0)[0]
    bound_l_interp = interp_track(reftrack=bound_l_tmp, stepsize_approx=1.0)[0]

    # calculate minimum distances of every trajectory point to the boundaries
    min_dists = calc_min_bound_dists(
        trajectory=trajectory,
        bound1=bound_r_interp,
        bound2=bound_l_interp,
        length_veh=length_veh,
        width_veh=width_veh,
    )

    # calculate overall minimum distance
    min_dist = np.amin(min_dists)

    # warn if distance falls below a safety margin of 1.0 m
    if min_dist < 1.0:
        logger.warning(
            "Minimum distance to boundaries is estimated to %.2fm. Keep in mind that the distance can also"
            " lie on the outside of the track!" % min_dist
        )
    elif debug:
        logger.info(
            "Minimum distance to boundaries is estimated to %.2fm. Keep in mind that the distance can also lie"
            " on the outside of the track!" % min_dist
        )

    # ------------------------------------------------------------------------------------------------------------------
    # CHECK FINAL TRAJECTORY FOR MAXIMUM CURVATURE ---------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # check maximum (absolute) curvature
    if np.amax(np.abs(trajectory[:, 4])) > curvlim:
        logger.warning(
            "Curvature limit is exceeded: %.3frad/m" % np.amax(np.abs(trajectory[:, 4]))
        )

    # ------------------------------------------------------------------------------------------------------------------
    # CHECK FINAL TRAJECTORY FOR MAXIMUM ACCELERATIONS -----------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    if ggv is not None:
        # transform curvature kappa into corresponding radii (abs because curvature has a sign in our convention)
        radii = np.abs(
            np.divide(
                1.0,
                trajectory[:, 4],
                out=np.full(trajectory.shape[0], np.inf),
                where=trajectory[:, 4] != 0,
            )
        )

        # check max. lateral accelerations
        ay_profile = np.divide(np.power(trajectory[:, 5], 2), radii)

        if np.any(ay_profile > np.amax(ggv[:, 2]) + 0.1):
            logger.warning(
                "Lateral ggv acceleration limit is exceeded: %.2fm/s2"
                % np.amax(ay_profile)
            )

        # check max. longitudinal accelerations (consider that drag is included in the velocity profile!)
        ax_drag = -np.power(trajectory[:, 5], 2) * dragcoeff / mass_veh
        ax_wo_drag = trajectory[:, 6] - ax_drag

        if np.any(ax_wo_drag > np.amax(ggv[:, 1]) + 0.1):
            logger.warning(
                "Longitudinal ggv acceleration limit (positive) is exceeded: %.2fm/s2"
                % np.amax(ax_wo_drag)
            )

        if np.any(ax_wo_drag < np.amin(-ggv[:, 1]) - 0.1):
            logger.warning(
                "Longitudinal ggv acceleration limit (negative) is exceeded: %.2fm/s2"
                % np.amin(ax_wo_drag)
            )

        # check total acceleration
        a_tot = np.sqrt(np.power(ax_wo_drag, 2) + np.power(ay_profile, 2))

        if np.any(a_tot > np.amax(ggv[:, 1:]) + 0.1):
            logger.warning(
                "Total ggv acceleration limit is exceeded: %.2fm/s2" % np.amax(a_tot)
            )

    else:
        logger.warning(
            "Since ggv-diagram was not given the according checks cannot be performed!"
        )

    if ax_max_machines is not None:
        # check max. longitudinal accelerations (consider that drag is included in the velocity profile!)
        ax_drag = -np.power(trajectory[:, 5], 2) * dragcoeff / mass_veh
        ax_wo_drag = trajectory[:, 6] - ax_drag

        if np.any(ax_wo_drag > np.amax(ax_max_machines[:, 1]) + 0.1):
            logger.warning(
                "Longitudinal acceleration machine limits are exceeded: %.2fm/s2"
                % np.amax(ax_wo_drag)
            )

    # ------------------------------------------------------------------------------------------------------------------
    # CHECK FINAL TRAJECTORY FOR MAXIMUM VELOCITY ----------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    if np.any(trajectory[:, 5] > v_max + 0.1):
        logger.warning(
            "Maximum velocity of final trajectory exceeds the maximal velocity of the vehicle: %.2fm/s!"
            % np.amax(trajectory[:, 5])
        )

    return bound_r, bound_l


# testing --------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
