# -*- coding: utf-8 -*-
"""Metronomic licking behavior-related functions.

This module includes a set of functions that isolate behaviorally relevant events (e.g. ILIs, IRIs, timestamps of
rewarded licks, etc.) for analysis.

"""

import numpy as np

# TODO(annie-taylor): ouptut ts w/behav vectors for signal sync

def behaviorevents_todict(eventlog):
    """More for reference than actual functionality... Isolates unique behavioral events from eventlog as separate variables.
    TODO(annie-taylor): update documentation? maybe remove function after creating effective data object

    Args:
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.

    Returns:
        event_dict
    """
    event_dict = {}
    event_dict['lick_start'] = eventlog[eventlog[:, 0] == 5]
    event_dict['lick_end'] = eventlog[eventlog[:, 0] == 6]
    event_dict['fake_cs'] = eventlog[eventlog[:, 0] == 15]
    event_dict['solenoid_open'] = eventlog[eventlog[:, 0] == 10]
    event_dict['solenoid_close'] = eventlog[eventlog[:, 0] == 14]
    event_dict['session_end'] = eventlog[eventlog[:, 0] == 0]
    return event_dict


def findilis(lick_events):
    """Given a list of all lick timestamps, calculate the interlick interval for all events.

    Arguments:
        lick_events (np array): Array of lick onset timestamps.

    Returns:
        ILIs (np array): Array with interlick intervals (column 1) and timestamp of second lick for each ILI (column 2).
    """
    n_licks = len(lick_events)
    ILIs = np.full([n_licks-1, 2], None)
    for idx in range(n_licks - 1):
        t1 = lick_events[idx, 1]
        t2 = lick_events[idx+1, 1]
        dt = t2 - t1
        ILIs[idx, 0] = dt
        ILIs[idx, 1] = t1
    assert all(ILIs[:, 0] > 0), 'ILIs should not be negative'
    return ILIs


def findiris(event_dict, solenoidthreshold, rampduration, gamma, max_solenoid_opentime):
    """Find the interreward interval for all reward events (where solenoid open time crosses threshold).
    #TODO(annie-taylor): add behav_params to input, reduce number of arguments

    Arguments:
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
        solenoidthreshold (int): Minimum solenoid open time that results in reward delivery.
        rampduration (int): Window of time during which reward magnitude is increasing (between 0 and max).
        gamma (float): Parameter indicating the steepness of the reward magnitude ramp.
        max_solenoid_opentime (int): Determines the peak reward magnitude.

    Returns: TODO(annie-taylor): documentation is incorrect
        rewardtime (np array): Lists timestamps for all (sufficiently large) rewards.
    """
    # Isolate timestamps of relevant behavioral events
    fake_cs = event_dict['fake_cs']
    solenoid_open = event_dict['solenoid_open']
    rewardtime_candidates = solenoid_open[:, 1]
    solenoid_duration = solenoidduration(solenoid_open, fake_cs, rampduration, gamma, max_solenoid_opentime)
    rewardtime = rewardtime_candidates[solenoid_duration >= solenoidthreshold]
    n_rewards = len(rewardtime)
    IRIs = np.full([n_rewards - 1, 2], None)
    for idx in range(n_rewards - 1):
        t1 = rewardtime[idx]
        t2 = rewardtime[idx + 1]
        dt = t2 - t1
        IRIs[idx, 0] = dt
        IRIs[idx, 1] = t1
    assert all(IRIs[:, 0] > 0), 'IRIs should not be negative'
    return IRIs


def findibis(ILIs, lickbout_threshold):
    """From given set of ILIs, determine the IBI.

    Args:
        ILIs (np array): Set of all ILI durations (column 0) and timestamps (column 1).
        lickbout_threshold (int): Minimum time (in ms) between licks that indicates a separate bout.

    Returns:
        IBIs (np array): Array containing duration of IBI (column 0) and timestamps of IBI (column 1).
    """
    ibi_idxs = ILIs[:, 0] > lickbout_threshold
    interbout_duration = ILIs[ibi_idxs, 0]
    interbout_ts = ILIs[ibi_idxs, 1]
    IBIs = np.full((len(interbout_duration), 2), None)
    IBIs[:, 0] = interbout_duration
    IBIs[:, 1] = interbout_ts
    return IBIs


def findcrdelays(rewardtimes, cstimes):
    """Given a set of reward times and CS times, returns an array of cue/reward delays. Used to estimate reward magnitude.
    TODO(annie-taylor): revise documentation, should be cue-solenoid delay, not necessarily reward delays, can't give actual reward times as inputs b/c this function is needed to determine reward time
    TODO(annie-taylor): alternatively, could frame this as a namlab_analysis function that finds delays between two arbitrary pairs of stimuli??

    Args:
        rewardtimes (np array): Array of reward timestamps. Reward timestamp must be calculated based on solenoid open
        time, not simply solenoid open timestamp.
        cstimes (np array): Array of cue onset timestamps. These are timestamps for the 'fake' trial onset cue.

    Returns:
        cuerewarddelays (np array): Array with cue-reward delay for each reward instance.
    """
    cuerewarddelays = np.full(len(rewardtimes), None)
    for idx, reward in enumerate(rewardtimes):
        diff = reward - cstimes
        delay = min(diff[diff >= 0])
        cuerewarddelays[idx] = delay
    return cuerewarddelays


def solenoidduration(solenoid_open, fake_cs, rampduration, gamma, max_solenoid_opentime):
    """Estimates the reward magnitude of a 'solenoid open' event based on how long the...
    TODO(annie-taylor): update documentation
    Arguments:
        solenoid_open (np array):
        fake_cs (np array):
        rampduration (int): Window of time during which reward magnitude is increasing (between 0 and max).
        gamma (float): Parameter indicating the steepness of the reward magnitude ramp.
        max_solenoid_opentime (int): Determines the peak reward magnitude.

    Returns:
        solenoid_duration (np array) TODO(annie-taylor): this reflects a magnitude more generally, not a true duration
    """
    cuerewdelay = findcrdelays(solenoid_open[:, 1], fake_cs[:, 1])
    scaled_solenoidopentime = cuerewdelay / rampduration
    scaled_solenoidopentime[scaled_solenoidopentime >= 1] = 1
    solenoid_duration = (scaled_solenoidopentime ** gamma) * max_solenoid_opentime
    return solenoid_duration


def findrewardtimes(solenoidopentime, solenoidduration, solenoidthreshold, fixed_mag=True):
    """Using solenoid open timestamps and calculated durations, determine when sufficiently large reward is delivered
    and return timestamps of rewards that meet criteria.

    Args:
        solenoidopentime (np array): Array of timestamps for all solenoid open onset.
        solenoidduration (np array): Array with the scaled duration of solenoid open time (prop. to reward magnitude).
        solenoidthreshold (float): Minimum value of solenoid duration at which reward is 'sufficient' or 'noticeable.'
        fixed_mag (boolean): If true (default), use a fixed reward magnitude (max reward). Else, use threshold.

    Return:
        rewardtimes (np array): Timestamps for delivery of rewards (either fixed magnitude or above specified threshold).
    """
    if fixed_mag:
        # If fixed_mag is true, then only return timestamps of maximal rewards
        max_rew = max(solenoidduration)  # Determine maximum possible reward
        rewardtimes = solenoidopentime[solenoidduration == max_rew]
    else:
        # Otherwise, return timestamps of rewards that exceed threshold of open time for viable reward delivery
        rewardtimes = solenoidopentime[solenoidduration >= solenoidthreshold]
    return rewardtimes


def findrewardlicks(licktimes, rewardtimes, solenoidopentime, solenoidthreshold):
    """Find the timestamps of licks that occur after a sufficiently large reward has been delivered.

    Args:
        lick_ts (np array): Timestamps for all lick instances.
        solenoidopentime (np array): Array of timestamps for all solenoid open onset.
        solenoidduration (np array): Array with the scaled duration of solenoid open time (prop. to reward magnitude).
        solenoidthreshold (float): Minimum value of solenoid duration at which reward is 'sufficient' or 'noticeable.'

    Returns:
        rewardlicks (np array): Contains timestamps of all rewarded licks.
    """

    rewardlicks = np.full(len(solenoidopentime), None)
    rewardtimes = findrewardtimes(rewardtimes, solenoidopentime, solenoidthreshold) #TODO(annie-taylor) since you just immediately call this function, should probably just have a rewardtimes input
    for idx, reward in enumerate(rewardtimes):
        rewardlick_delays = licktimes - reward
        rewardlicks[idx] = min(licktimes[rewardlick_delays >= 0])
    return rewardlicks


def ixinearevent(ixis, ixi_ts, event_ts, order ='following'):
    """Finds the IXI (duration) that immediately precedes reward delivery. X may be L (lick), B (bout), or R (reward).
    TODO(annie-taylor) update documentation
    Args:
        ixis (np array): All IXI durations.
        ixi_ts (np array): Timestamps of the 'start' lick for an IXI.
        event_ts (np array): Timestamps of rewards (only instances where solenoid is open for a sufficiently long time).

    Returns:
        ixi_preceding_rew (np array): ILI duration immediately preceding reward delivery for all substantial rewards.
    """
    ceiling = max(ixi_ts)
    event_ts = event_ts.astype(object)
    ixi_near_event = np.full(len(event_ts), None)
    if order == 'following': #TODO(annie-taylor): remove duplicates
        for idx, ts in enumerate(event_ts):
            candidate_ixi_idxs = (ixi_ts - ts) < 0
            following_ts_idx = np.where(candidate_ixi_idxs)[0]
            if len(following_ts_idx) > 0:
                ixi_near_event[idx] = ixis[following_ts_idx[-1]]  # Make sure there is a event_ts after event
            if idx > 0:  # Remove duplicates, use closest event only
                if ixi_near_event[idx] == ixi_near_event[idx-1]:
                    ixi_near_event[idx] = None
                    event_ts[idx] = None
    elif order == 'preceding':
        for idx, ts in enumerate(event_ts):
            ixi_ts[(ixi_ts - ts) <= 0] = ceiling * 2  # Set ts to high value s.t. argmin ignores event_ts that precede ili_ts
            preceding_ts_idx = np.argmin(ixi_ts)
            ixi_near_event[idx] = ixis[preceding_ts_idx]
            if idx > 0:  # Remove duplicates, use closest event only
                if ixi_near_event[idx] == ixi_near_event[idx-1]:
                    ixi_near_event[idx-1] = None
                    event_ts[idx - 1] = None
    if None in ixi_near_event:
        event_ts = event_ts[ixi_near_event != None]
        ixi_near_event = ixi_near_event[ixi_near_event != None]
    return ixi_near_event, event_ts


def nlicksbeforereward(lick_ts, solenoidopentimes, solenoidduration, solenoidthreshold):
    """For each substantial reward, count the number of licks that preceded reward.

    Args:
        lick_ts (np array): Timestamps for all lick instances.
        solenoidopentime (np array): Array of timestamps for all solenoid open onset.
        solenoidduration (np array): Array with the scaled duration of solenoid open time (prop. to reward magnitude).
        solenoidthreshold (float): Minimum value of solenoid duration at which reward is 'sufficient' or 'noticeable.'

    Returns:
        nlicks_prereward
    """
    rewardtimes = findrewardtimes(solenoidopentimes, solenoidduration, solenoidthreshold) #TODO(annie-taylor) since you just immediately call this function, should probably just have a rewardtimes input
    nlicks_prereward = np.full(len(rewardtimes), None)
    for idx, rt in enumerate(rewardtimes):
        nlicks = len(lick_ts < rt)  # Count licks that precede reward
        nlicks_prereward[idx] = nlicks  # Keep track of nlicks per reward
        lick_ts[lick_ts < rt] = []  # Remove licks from array that have already been counted
    return nlicks_prereward

