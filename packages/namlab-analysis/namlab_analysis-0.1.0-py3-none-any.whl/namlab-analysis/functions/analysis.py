# -*- coding: utf-8 -*-
"""Metronomic licking analysis functions module.

This module includes a set of functions that analyze behavioral and neural data (beyond simple preprocessing).
"""

import behavior as beh
from scipy import stats
import numpy as np
import pickle as p


def corr_mice(eventlogs, photometryfiles, analysis_params, behav_params_all):
    """TODO(annie-taylor): update documentation"""
    mouselist = list(eventlogs.keys())

    rhos = dict.fromkeys(mouselist)
    pvals = dict.fromkeys(mouselist)

    for mouse in mouselist:
        rhos[mouse], pvals[mouse] = corr_sessions(eventlogs[mouse], photometryfiles[mouse], analysis_params,
                                                 behav_params_all[mouse])
    return rhos, pvals


def corr_sessions(eventlog_mouse, photometryfiles_mouse, analysis_params, behav_params_mouse):
    """TODO(annie-taylor): update documentation"""
    daylist = eventlog_mouse.keys()
    rhos_mouse = dict.fromkeys(daylist)
    pvals_mouse = dict.fromkeys(daylist)

    for day in daylist:
        with open(photometryfiles_mouse[day][0], 'rb') as photometrypicklefile:
            photometrydata = p.load(photometrypicklefile)
            dff_signal = photometrydata['dff']
            dff_time = photometrydata['time']
            eventlog = eventlog_mouse[day]
            behav_params = behav_params_mouse[day]
            event_dict = beh.behaviorevents_todict(eventlog)
            day = day.replace('Day', '')  # Make keys for rho/pvals simply the session number (exclude word day)
            rhos_mouse[day], pvals_mouse[day] = ixi_corr(event_dict, dff_signal, dff_time, analysis_params,
                                                         behav_params)
    return rhos_mouse, pvals_mouse


def ixi_near_event(event_dict, analysis_params, behav_params):
    """TODO(annie-taylor): update documentation

        Args:
            eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
            dff_signal (np array): Photometry (df/f) signal to be analyzed.
            dff_time (np array): Timestamps corresponding to dff_signal (matched indices).
            response_window (int or float): Specifies the window size over which the average dopamine response is calculated.
            corr_function (string or list): Indicates which type of correlation should be used ('pearson', 'spearman', or 'kendall'; Default is 'pearson')

        Returns:

        """
    # relevant behavioral events
    lick_start = event_dict['lick_start']
    fake_cs = event_dict['fake_cs']
    solenoid_open = event_dict['solenoid_open']

    # analysis parameters
    response_type = analysis_params['response_type']
    interval_type = analysis_params['interval_type']
    order = analysis_params['order']
    lickbout_threshold = analysis_params['lickbout_threshold']  # If interlick interval is >500ms, marks start of a "bout"

    # behavior parameters
    rampduration = behav_params['rampduration']
    gamma = behav_params['gamma']
    max_solenoid_opentime = behav_params['max_solenoid_opentime']  # Solenoid open time in ms
    solenoidthreshold = 1 * max_solenoid_opentime

    if interval_type == 'ibi':
        # Calculate all ILIs
        ILIs = beh.findilis(lick_start)
        # Find all IBIs (ILIs that are separated by at least lickbout_threshold
        IBIs = beh.findibis(ILIs, lickbout_threshold)
        interx_duration = IBIs[:, 0]  # length of the interval of interest
        interx_ts = IBIs[:, 1]  # first timestamp of the interval
    elif interval_type == 'iri':
        # Calculate all IRIs
        IRIs = beh.findiris(event_dict, solenoidthreshold, rampduration, gamma, max_solenoid_opentime)
        interx_duration = IRIs[:, 0]  # length of the interval of interest
        interx_ts = IRIs[:, 1]  # first timestamp of the interval

    if response_type == 'reward':
        solenoid_open_ts = solenoid_open[:, 1]
        # Determine length of solenoid open times
        solenoid_duration = beh.solenoidduration(solenoid_open, fake_cs, rampduration, gamma, max_solenoid_opentime)
        # Find reward times i.e. timestamps of solenoid openings where a sufficiently large reward was delivered
        responsetimes = beh.findrewardtimes(solenoid_open_ts, solenoid_duration, solenoidthreshold)
    elif response_type == 'ibi_lick':
        if interval_type == 'ibi':
            # If IBIs have already been calculated, copy ts into new variable
            responsetimes = interx_ts
        else:
            # Otherwise, must calculate all ILIs
            ILIs = beh.findilis(lick_start)
            # Find all IBIs (ILIs that are separated by at least lickbout_threshold
            IBIs = beh.findibis(ILIs, lickbout_threshold)
            responsetimes = IBIs[:, 1]

    # Isolate the IXIs closest to determined event time
    ixi_event, event_ts = beh.ixinearevent(interx_duration, interx_ts, responsetimes, order=order)
    return ixi_event, event_ts


def avgdanearevent(DA, DA_ts, event_ts, analysis_params):
    """Finds the magnitude of the dopamine response closest to event time (specific event depends on list of timestamps
    provided including rewards, licks, or any other relevant behavioral events).
    TODO(annie-taylor) consider moving this from behavior_functions to new module? does it belong here?

    Args:
        DA (np array): DA df/f for entire session (idxs shared with DA_ts).
        DA_ts (np array): Timestamps of recordings for DA (above), shared idxs.
        event_ts (np array): Timestamps for all relevant events.
        response_window (float):
        norm_window (float): Window of time over which DA response is averaged and used for baseline subtraction.

    Returns:
        event_response (np array): All DA responses at (i.e. closest to) event time.
    """
    # analysis parameters
    response_window = analysis_params['response_window']
    norm_window = analysis_params['norm_window']

    # For elements of DA data that are NaN/have negative timestamps, set to arbitrarily large value s.t. are ignored
    ceiling = max(DA_ts)
    DA_ts[DA_ts < 0] = ceiling * 2
    event_response = np.full(len(event_ts), None)  # Initialize event_response matrix
    for idx, ts in enumerate(event_ts):
        closest_ts_idx_center = np.argmin(abs(DA_ts - ts))  # Find idx closest to the event timestamp
        if norm_window is not None:
            closest_ts_idx_norm = np.argmin(abs(DA_ts - (ts + norm_window)))  # Find idx left of the event ts
            baseline = np.mean(DA[closest_ts_idx_norm:closest_ts_idx_center])
        else:
            baseline = 0
        closest_ts_idx_right = np.argmin(abs(DA_ts - (ts + response_window)))  # Find idx right of the event ts
        # Use window preceding event as baseline for DA response
        if DA_ts[closest_ts_idx_right] - DA_ts[closest_ts_idx_center] < (response_window - response_window*0.05):
            # If this happens, too close to end of recording to average over last 500ms, so must omit last trial
            event_response[idx] = None
        else:
            response = np.mean(DA[closest_ts_idx_center:closest_ts_idx_right])  # Window after event == actual response
            event_response[idx] = response - baseline  # Reported response is (actual - baseline)
    response_idxs = event_response != None
    event_response = event_response[event_response != None]
    return event_response, response_idxs


def ixi_corr(event_dict, dff_signal, dff_time, analysis_params, behav_params):
    """Perform correlation analysis (spearman, pearson, and kendall) between ,XI and reward response. IXI may be
    interlick or interbout intervals.

        Args:
            eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
            dff_signal (np array): Photometry (df/f) signal to be analyzed.
            dff_time (np array): Timestamps corresponding to dff_signal (matched indices).
         response_window= (int or float): Specifies the window size over which the average dopamine response is calculated.
            corr_function (string or list): Indicates which type of correlation should be used ('pearson', 'spearman', or 'kendall'; Default is 'pearson')

        Returns:
            rho, pval
        """

    # analysis parameters
    corr_function = analysis_params['corr_function']

    #TODO(annie-taylor): do per session correlation first! do not concatenate data
    ixi_event, event_ts = ixi_near_event(event_dict, analysis_params, behav_params)
    event_response, response_idxs = avgdanearevent(dff_signal, dff_time, event_ts, analysis_params)
    ixi_event = ixi_event[response_idxs]  #If da response for any events was not calculated, omit these events
    # Calculate correlation between the reward response and length of the IBI
    if not isinstance(corr_function, list):
        rho, pval = responsecorr(ixi_event, event_response, corr_function=corr_function)
    # If a list of correlation functions are given, return rho and pval as dictionaries w/functions as keys
    else:
        rho = {}
        pval = {}
        for fn in corr_function:
            rho[fn], pval[fn] = responsecorr(ixi_event, event_response, corr_function=fn)
    return rho, pval


def responsecorr(correlate, response, corr_function='pearson'):
    """General function for spearman, pearson, and kendall correlations with DA reward response.
    TODO(annie-taylor): update documentation

    Args:
        correlate (np array): Unspecified array of behavioral data for correlation analysis.
        rewardresponse (np array):
        corr_function (string): Indicates which type of correlation should be used ('pearson', 'spearman', or 'kendall';
         Default is 'pearson')

    Returns:
        rho, pval
    """
    # If a DA value of nan is returned, remove
    nan_idx = np.isnan(list(response))
    response = np.delete(response, nan_idx)
    correlate = np.delete(correlate, nan_idx)
    if corr_function == 'spearman':
        rho, pval = stats.spearmanr(response, correlate)
    elif corr_function == 'pearson':
        rho, pval = stats.pearsonr(response, correlate)
    elif corr_function == 'kendall':
        rho, pval = stats.kendalltau(response, correlate)
    return rho, pval


