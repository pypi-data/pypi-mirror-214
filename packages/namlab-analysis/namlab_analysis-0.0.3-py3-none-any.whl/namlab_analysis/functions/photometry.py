# -*- coding: utf-8 -*-
"""Data IO functions module.

This module contains a set of functions for preprocessing photometry data.
"""

import numpy as np


def calculate_dff(data_405, data_470, time, window, binsize_interpolation):
    """Calculate df/f and interpolate the data, if needed. First, linearly transform data_405 to fit to data_470. Then,
    df/f is calculated as (data_470-fitted data_405)/(fitted data_405).

        Args:
            data_405 (float list): Time series of isosbestic fluorescence data.
            data_470 (float list): Time series of fluorescence data.
            time (float list): Timestamps.
            window (int list): Window of data being analyzed.
            binsize_interpolation (int): The final binsize of your data (unit:ms). If 0, no interpolation.

        Returns:
            dff (float list): Calculated df/f
    """

    # Use the data within window (task time) for calculating coefficient. This is to cut out some initial part
    # where fluorescence drops in a non-linear manner. Also, exclude data points whose values are nan.
    inwindow = [x and y and z for x,y,z in zip(np.array([x>=window[0] and x<=window[1] for x in time]),
                                               ~np.isnan(data_470),~np.isnan(data_405))]

    # fit 405 signal to 470, and find coefficients
    coef = np.polyfit(np.array(data_405)[inwindow], np.array(data_470)[inwindow], 1)
    # calculated fitted 405
    fitted_405 = np.polyval(coef, data_405)
    # subtract fitted 405 from 470 and then divide it by fitted 405 - this is dff
    dff = (data_470 - fitted_405) * 100 / fitted_405

    # if binsize_interpolation is larger than 0, interpolate dff with desired bin size
    if binsize_interpolation > 0:
        import scipy.interpolate as interpolate
        f = interpolate.interp1d(time, dff)
        newtime = np.arange(time[0], time[-1], binsize_interpolation)
        newdata = f(newtime)
        dff = newdata
        time = newtime

    dff = dff.tolist()
    time = time.tolist()
    return dff, time


def synchronize_timestamps(photometryfile, matfile, ttl2matindex):
    """Synchronize photometry timestamps to matlab timestamps.

        Args:
            photometryfile (str): Full path of photometry file.
            matfile (str): Full path of behavior file.
            ttl2matindex (int): Event code of ttl2. In randomrewards task mode, this is background reward, while in
            other tasks, this is cue (any auditory or light cues)

        Returns:
            newtime (float list): New photometry timestamps that is synced to matlab timestamps.
            mat_endtime (float): Session end time or last TTL2 time.
    """

    # find photometry window - only use timepoints during the session on
    start_pf = [i + 1 for i, v in enumerate(np.diff(photometryfile['ttl1'])) if v == 1]
    end_pf = [i for i, v in enumerate(np.diff(photometryfile['ttl1'])) if v == -1]
    window_mat = [0, matfile['eventlog'][matfile['eventlog'][:, 0] == 0, 1][0]]

    # when there's some error...
    # like photometry file doesn't have onset and offset of session in ttl1 or session end time is missing in mat file
    # use ttl2 to sync timestamps
    if len(end_pf) != 1 or len(start_pf) != 1 or np.diff(window_mat) == 0:
        ref_doric = [i + 1 for i, v in enumerate(np.diff(photometryfile['ttl2'])) if v == 1]
        ref_mat = matfile['eventlog'][np.isin(matfile['eventlog'][:, 0],ttl2matindex), 1]
        if len(ref_doric) < len(ref_mat):
            if len(start_pf) == 0:
                ref_mat = ref_mat[-len(ref_doric):]
            elif len(end_pf) == 0:
                ref_mat = ref_mat[:len(ref_doric)]
        window_pf = [ref_doric[0], ref_doric[-1]]
        window_pf = [photometryfile['time'][x] for x in window_pf]
        window_mat = [ref_mat[0], ref_mat[-1]]
    else:
        window_pf = [photometryfile['time'][start_pf[0]],photometryfile['time'][end_pf[0]]]

    # this is new synchronized timestamps of photometry file
    newtime = [(x-window_pf[0])*np.diff(window_mat)[0]/np.diff(window_pf)[0]+window_mat[0] for x in photometryfile['time']]

    # session end time according to matlab time
    mat_endtime = window_mat[1]

    return newtime, mat_endtime


def preprocessing(photometryfile, matfile, binsize_interpolation, ttl2matindex):
    """this function synchronize timestamps and calculate dff session end time recorded in mat file.

        Args:
            photometryfile (str): Full path of photometry file.
            matfile (str): Full path of behavior file.
            binsize_interpolation (int): The final binsize of your data (unit:ms). If 0, no interpolation.
            ttl2matindex (int): Event code of ttl2. In randomrewards task mode, this is background reward, while in
            other tasks, this is cue (any auditory or light cues)

        Returns:
            dff (float list): Calculated df/f.
            time (float list): New photometry timestamps that is synced to matlab timestamps.
    """

    # save synchronized timestamps of photometry file
    photometryfile['time'],mat_endtime = synchronize_timestamps(photometryfile, matfile, ttl2matindex)

    # calculate dff
    dff, time = calculate_dff(photometryfile['405'], photometryfile['470'], photometryfile['time'], [0, mat_endtime],
                              binsize_interpolation)
    return dff, time
