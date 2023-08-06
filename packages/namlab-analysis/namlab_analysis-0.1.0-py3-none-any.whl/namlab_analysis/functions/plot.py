import numpy as np
import scipy.ndimage as nd
from numpy.linalg import norm
import matplotlib.pyplot as plt
import pickle as p
import behavior as beh


def align_events_to_reference(eventlog, eventlabel, reference, window, binsize, resolution=None):
    """Align instances of one event (eventlabel) to another event (referencelabel) and return PSTH.

    Args:
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
        eventlabel (int): Label specifying the events to be aligned.
        reference (np array OR int): Array with all reference event timestamps OR integer label specifying reference event (i.e. event setting t=0 for alignment of other events).
        window (np array): Time window ([start, stop]) around each instance of reference event (in ms).
        binsize (int): Bin size for histogram (in ms).
        resolution (float or None): If not None (default), sets st. dev. for Gaussian kernel (sigma=resolution*binsize).

    Returns:
        aligned_event, meanpsth, sempsth, psthtime
    """
    eventlabel_series = eventlog[:, 0]  # First column is event labels
    eventtime = eventlog[:, 1]  # Second column of eventlog is timestamps
    if isinstance(reference, int):
        # If reference is given as an integer, use reference label to find timestamps
        reference_times = eventtime[eventlabel_series == reference]
    else:
        # Otherwise, timestamps were given as input, simply change variable name
        reference_times = reference
    event_times = eventtime[eventlabel_series == eventlabel]  # Find timestamps for event of interest
    # Calculate number of bins, reference events
    window_sz = window[-1] - window[0]
    nbins = int(window_sz / binsize)
    nrefs = len(reference_times)
    # Initialize arrays of aligned events (i.e. event time relative to reference event), histogram
    aligned_event = np.full(nrefs, None)
    hist_event = np.zeros(shape=(nrefs, nbins))
    psthtime = np.transpose(range(window[0], window[1], binsize))
    bin_edges = np.hstack((psthtime, window[1]))  # Bin edges to give histogram func (to use same edges for each event)
    for i, ref_ts in enumerate(reference_times):
        # Center events of interest around timestamp of reference event
        shifted_event = event_times[(event_times >= ref_ts + window[0]) & (event_times < ref_ts + window[-1])].tolist() - ref_ts
        aligned_event[i] = np.hstack(shifted_event)  # Save realigned events in array
        # Generate PSTH for each reference
        hist_event[i, :] = np.histogram(shifted_event, bin_edges)[0]  # Only return histogram, not bin edges
    # Generate x-axis for psth
    meanpsth = np.mean(hist_event, 0)  # Average psth values for all reference events
    sempsth = np.std(hist_event, 0) / np.sqrt(hist_event.shape[0])  # Generate s.e.m. for psth around all references
    if resolution is not None:
        # If smoothing w/gaussian kernel, apply gaussian filter to mean and s.e.m. for psth
        # TODO(@HuijeongJeong) does the order of smoothing/averaging matter?
        meanpsth = nd.gaussian_filter1d(meanpsth, resolution)
        sempsth = nd.gaussian_filter1d(sempsth, resolution)
    return aligned_event, meanpsth, sempsth, psthtime


def align_signal_to_reference(signal, timestamp, eventlog, reference, window, resolution, baselinewindow=None):
    """Align continuous signal (with fixed sample rate, e.g. photometry trace) to the other event.

    Args:
        signal (np array): Signal you want to align.
        timestamp (np array): Sample timestamps corresponding to signal.
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
        reference (np array OR int): Array with all reference event timestamps OR integer label specifying reference event (i.e. event setting t=0 for alignment of other events).
        window (np array): Time window ([start, stop]) around each instance of reference event (in ms).
        resolution (float or None): If not None (default), sets st. dev. for Gaussian kernel (sigma=resolution*binsize).
        baselinewindow (np array or None): For 1d array, sets same baseline window for all events. 2d array specifies different window for each reference time. If None, does not normalize.

    Returns:
        aligned_event, meanpsth, sempsth, psthtime

    """
    eventlabel_series = eventlog[:, 0]  # First column is event labels
    eventtime = eventlog[:, 1]  # Second column of eventlog is timestamps
    if isinstance(reference, int):
        # If reference is given as an integer, use reference label to find timestamps
        reference_times = eventtime[eventlabel_series == reference]
    else:
        # Otherwise, timestamps were given as input, simply change variable name
        reference_times = reference

    frameinterval = np.nanmean(np.diff(timestamp))  # Use mean dist. b/t timestamps to estimate a good frame window
    framewindow = [int(i) for i in np.round(window / frameinterval)] # TODO(annie-taylor): add comments!!

    # Calculate number of bins, reference events
    nbins = np.sum(np.abs(framewindow)) + 1
    nrefs = len(reference_times)

    aligned_event = np.full((nrefs, nbins), np.nan)
    for i, ref_ts in enumerate(reference_times):
        closestframe = np.nanargmin(np.abs(timestamp - ref_ts))
        if baselinewindow is not None:  # TODO(annie-taylor): add comments!!
            if len(np.array(baselinewindow).shape) == 1:
                framewindow_bl = [int(i) for i in np.round(baselinewindow / frameinterval)]
                basemean = np.nanmean(signal[np.arange(framewindow_bl[0], framewindow_bl[1] + 1) + closestframe])
            else:
                framewindow_bl = [int(i) for i in np.round(baselinewindow[i] / frameinterval)]
                basemean = np.nanmean(signal[np.arange(framewindow_bl[0], framewindow_bl[1] + 1) + closestframe])
        else:
            basemean = 0
        # TODO(annie-taylor): add comments!!
        if framewindow[0] + closestframe < 0:
            data = signal[np.arange(0, framewindow[1] + 1 + closestframe)]
            aligned_event[i, nbins - len(data):] = data - basemean
        elif framewindow[1] + 1 + closestframe > len(signal):
            data = signal[np.arange(framewindow[0] + closestframe, len(signal))]
            aligned_event[i, :-(nbins - len(data))] = data - basemean
        else:
            data = signal[np.arange(framewindow[0], framewindow[1] + 1) + closestframe]
            aligned_event[i, :] = data - basemean

    nonan = np.sum(np.isnan(aligned_event), 1) == 0  # not sure this is the most efficient way to do this? why sum?
    meanpsth = np.mean(aligned_event[nonan, :], 0)  # Average aligned response...
    sempsth = np.std(aligned_event[nonan, :], 0) / np.sqrt(np.sum(nonan))  # S.e.m of aligned response
    if resolution is not None:
        # If smoothing w/gaussian kernel, apply gaussian filter to mean and s.e.m. for psth
        meanpsth = nd.gaussian_filter1d(meanpsth, resolution)
        sempsth = nd.gaussian_filter1d(sempsth, resolution)
    psthtime = np.arange(framewindow[0], framewindow[1] + 1) * frameinterval  # Generate x-axis for psth

    return aligned_event, meanpsth, sempsth, psthtime


def first_event_time_after_reference(eventlog, eventlabel, reference, window):
    """Return timestamps of first events that occur within a window of time after each incidence of reference event.

    Args:
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
        eventlabel (int): Label specifying the events to be aligned.
        reference (np array OR int): Array with all reference event timestamps OR integer label specifying reference event (i.e. event setting t=0 for alignment of other events).
        window (float): Window (in ms) following reference event. "First" events are only recorded if they fall in this window.
    Returns:
        first_eventtime (np array): Array of all timestamps corresponding to first event incidence.
    """
    eventtime = eventlog[:, 0]  # First column of eventlog is timestamps
    eventlabel_series = eventlog[:, 1]  # Second column is event labels
    if isinstance(reference, int):
        # If reference is given as an integer, use reference label to find timestamps
        reference_times = eventtime[eventlabel_series == reference]
    else:
        # Otherwise, timestamps were given as input, simply change variable name
        reference_times = reference
    event_times = eventtime[eventlabel_series == eventlabel]  # Find timestamps for event of interest
    nrefs = len(reference_times)

    # Initialize array with first event instance timestamp
    first_eventtime = np.full(nrefs, np.nan)
    for i, ref_ts in enumerate(reference_times):
        # Return all events that fall after current reference event and within specified time window
        candidate_events = [t for t in event_times if (t > ref_ts) and (t - ref_ts) <= window]
        if len(candidate_events) > 0:  # If any events occur...
            # Only save first instance of candidate event
            first_eventtime[i] = candidate_events[0]
    return first_eventtime


def calculate_auc(signal, signaltime, reference_times, window):
    """Calculate area under curve of signal during specified window from reference event.

    Args:
        signal (np array): Signal for which AUC is calculated (e.g. photometry df/f).
        signaltime (np array): Sample timestamps corresponding to signal.
        reference_times (np array): Timestamps corresponding to reference events.
        window (np array): Time window ([start, stop]) within which signal AUC is calculated.
    Returns:
        auc (np array): Area under curve for signal within specified window relative to each reference event.
    """
    binsize = np.nanmean(np.diff(signaltime))  # Estimate size of bins
    auc = [np.sum(signal[np.logical_and(signaltime >= ref_ts + window[0], signaltime <= ref_ts + window[1])]) * binsize for ref_ts in
           reference_times]
    n = [np.sum(np.logical_and(signaltime >= ref_ts + window[0], signaltime <= ref_ts + window[1])) for ref_ts in reference_times]
    auc = [np.nan if x == 0 else y for x, y in zip(n, auc)]  # If no photometry data available, auc should be NaN
    return auc


def calculate_numevents(eventlog, eventlabel, reference, window):
    """Calculate number of events (e.g. licks) that occur during specified window following a reference event (e.g.
    rewards).

    Args:
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
        eventlabel (int): Label specifying the events to be aligned.
        reference (np array OR int): Array with all reference event timestamps OR integer label specifying reference event (i.e. event setting t=0 for alignment of other events).
        window (float): Window (in ms) following reference event during which events are counted.
    Returns:
        nevent (np array): Number of events that occur in window after reference, for each reference event.
    """
    eventtime = eventlog[:, 0]  # First column of eventlog is timestamps
    eventlabel_series = eventlog[:, 1]  # Second column is event labels
    if isinstance(reference, int):
        # If reference is given as an integer, use reference label to find timestamps
        reference_times = eventtime[eventlabel_series == reference]
    else:
        # Otherwise, timestamps were given as input, simply change variable name
        reference_times = reference
    event_times = eventtime[eventlabel_series == eventlabel]  # Find timestamps for event of interest
    # Count number of events that occur in window after event
    nevent = [np.sum(np.logical_and(event_times >= i + window[0], event_times < i + window[1])) for i in
              reference_times]
    return nevent

def plot_events_allmice(eventlogs, eventlabel, reference, window, binsize, resolution, clr, ylabels):
    """Plot PSTH for specified events (eventlabel) relative to time of reference event TODO(annie-taylor): documentation

        Args:
            eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
            eventlabel (int): Label specifying the events to be plotted.
            reference (np array): Here, reference should not be an array of timestamps, but an array of labels for reference events OR
            an array of arrays of timestamps for each reference event. (ex: [CS+ label, CS- label] OR [[CS+ timestamps], [CS- timestamps]])
            window (int): Time window around each instance of reference event (in ms).
            binsize:
            resolution (float or None): If not None (default), sets st. dev. for Gaussian kernel (sigma=resolution*binsize).
            clr (np array): Specifies a separate color for each unique event.
            ylabels (list): Y labels for axis 1 (event rasters) and axis 2 (event PSTH).
            fig (subfigure or None): If not None (default), plot scatter in a given subfigure (ex: fig = fig.subfigures(2,1)).

        Returns:
            Plot of event scatter.
        """
    mouselist = list(eventlogs.keys())
    # This assumes that the first mouse instance has the appropriate daylist for all other mice... does not generalize
    daylist = eventlogs[mouselist[0]].keys()

    n_sessions = len(daylist)
    figs = dict.fromkeys(mouselist)
    axeses = dict.fromkeys(mouselist)

    for mouse_idx, mouse in enumerate(mouselist):
        fig, axes = plt.subplots(2, n_sessions)
        for day_idx, day in enumerate(daylist):
            eventlog = eventlogs[mouse][day]
            fig, axes[:, mouse_idx] = plot_events_persession(eventlog, eventlabel, reference, window, binsize, resolution, clr, ylabels,
                                             mouse, axes=axes[:, mouse_idx], fig=fig)
        figs[mouse] = fig
        axeses[mouse] = axes
    return figs, axeses

def plot_signals_allmice(photometryfiles, eventlogs, eventlabel, reference, window, binsize, resolution, clr, ylabels,
                         baselinewindow=None, orderby=None, behav_params_all=None, analysis_params=None):
    """Plot PSTH for specified events (eventlabel) relative to time of reference event TODO(annie-taylor): documentation

        Args:
            eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
            eventlabel (int): Label specifying the events to be plotted.
            reference (np array): Here, reference should not be an array of timestamps, but an array of labels for reference events OR
            an array of arrays of timestamps for each reference event. (ex: [CS+ label, CS- label] OR [[CS+ timestamps], [CS- timestamps]])
            window (int): Time window around each instance of reference event (in ms).
            binsize:
            resolution (float or None): If not None (default), sets st. dev. for Gaussian kernel (sigma=resolution*binsize).
            clr (np array): Specifies a separate color for each unique event.
            ylabels (list): Y labels for axis 1 (event rasters) and axis 2 (event PSTH).
            fig (subfigure or None): If not None (default), plot scatter in a given subfigure (ex: fig = fig.subfigures(2,1)).

        Returns:
            Plot of event scatter.
        """
    mouselist = list(eventlogs.keys())
    # This assumes that the first mouse instance has the appropriate daylist for all other mice... does not generalize
    daylist = eventlogs[mouselist[0]].keys()

    n_sessions = len(daylist)
    figs = dict.fromkeys(mouselist)
    axeses = dict.fromkeys(mouselist)

    for mouse_idx, mouse in enumerate(mouselist):
        fig, axes = plt.subplots(2, n_sessions)
        for day_idx, day in enumerate(daylist):
            with open(photometryfiles[mouse][day][0], 'rb') as photometrypicklefile:
                photometrydata = p.load(photometrypicklefile)
            dff_signal = photometrydata['dff']
            dff_time = photometrydata['time']
            eventlog = eventlogs[mouse][day]
            fig, axes[:, day_idx] = plot_signal_persession(dff_signal, dff_time, eventlog, reference, window,
                                                    resolution, clr, ylabels, mouse, axes=axes[:, day_idx],
                                                    baselinewindow=baselinewindow, fig=fig, orderby=orderby,
                                                    behav_params=behav_params_all[mouse], analysis_params=analysis_params)
            a=1
        figs[mouse] = fig
        axeses[mouse] = axes
    return figs, axeses

def plot_events_persession(eventlog, eventlabel, reference, window, binsize, resolution, clr, ylabels, mousename,
                           axes=None, fig=None):
    """Plot PSTH for specified events (eventlabel) relative to time of reference event TODO(annie-taylor): documentation

    Args:
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
        eventlabel (int): Label specifying the events to be plotted.
        reference (np array): Here, reference should not be an array of timestamps, but an array of labels for reference events OR
        an array of arrays of timestamps for each reference event. (ex: [CS+ label, CS- label] OR [[CS+ timestamps], [CS- timestamps]])
        window (int): Time window around each instance of reference event (in ms).
        binsize:
        resolution (float or None): If not None (default), sets st. dev. for Gaussian kernel (sigma=resolution*binsize).
        clr (np array): Specifies a separate color for each unique event.
        ylabels (list): Y labels for axis 1 (event rasters) and axis 2 (event PSTH).
        fig (subfigure or None): If not None (default), plot scatter in a given subfigure (ex: fig = fig.subfigures(2,1)).

    Returns:
        Plot of event scatter.
    """
    if ~isinstance(reference, list):
        # If you want to plot events according to a signal reference but did not give list as input, rescued here
        reference = [reference]
    if axes is None:
        # Create axes if not given as input
        fig, axes = plt.subplots(2, 1)
        ax1 = axes[0]
        ax2 = axes[1]
        fig.suptitle(mousename)
    else:
        # Point ax1 and ax2 to axes object passed as input (for including multiple mice in same subplot)
        ax1 = axes[0]
        ax2 = axes[1]

    itrial = 1
    for i, ref_label in enumerate(reference):
        aligned_event, meanpsth, sempsth, psthtime = align_events_to_reference(eventlog, eventlabel,
                                                                               ref_label, window, binsize, resolution)
        ax1.scatter(np.concatenate(aligned_event) / 1000, np.concatenate(
            [np.ones(np.shape(event_ts), dtype=int) * (i + itrial) for i, event_ts in enumerate(aligned_event)]),
                    c=clr[i], s=0.5, edgecolor=None)
        ax2.fill_between(psthtime / 1000, meanpsth + sempsth, meanpsth - sempsth, alpha=0.3, facecolor=clr[i],
                         linewidth=0)
        ax2.plot(psthtime / 1000, meanpsth, color=clr[i])
        itrial = itrial + len(aligned_event)
    ax1.plot([0, 0], [0, itrial], 'k:', linewidth=0.35)  # Plot vertical dotted black line at reference time
    # Specify visual parameters for plots
    ax2ylim = [np.floor(ax2.get_ylim()[0]), np.ceil(ax2.get_ylim()[1])]
    ax2.plot([0, 0], ax2ylim, 'k:', linewidth=0.35)
    ax1.set_xlim(window[0] / 1000, window[1] / 1000)
    ax2.set_xlim(window[0] / 1000, window[1] / 1000)
    ax1.set_ylim(0.5, itrial + 0.5)
    ax2.set_ylim(ax2ylim[0], ax2ylim[1])
    ax2.set_xlabel('Time (s)')
    ax1.set_ylabel(ylabels[0])
    ax2.set_ylabel(ylabels[1])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    return fig, axes


def plot_signal_persession(signal, timestamp, eventlog, reference, window, resolution, clr, ylabels, mousename,
                           axes=None, fig=None, baselinewindow=None, orderby=None, behav_params=None, analysis_params=None):
    """Plot PSTH for given signal. TODO(annie-taylor): documentation
    TODO(annie-taylor): modify plotting module to accept event_dict as input rather than event log
    TODO(annie-taylor): resolve mapping issue b/t event_dict key and integer label

    Args:
        signal (np array): Signal you want to align.
        timestamp (np array): Sample timestamps corresponding to signal.
        eventlog (np array): Contains label (column 0), timestamp (column 1), and reward magnitude (column 2) of each behavioral event in session.
        reference (np array): Here, reference should not be an array of timestamps, but an array of labels for reference events OR
        an array of arrays of timestamps for each reference event. (ex: [CS+ label, CS- label] OR [[CS+ timestamps], [CS- timestamps]])
        window (int): Time window around each instance of reference event (in ms).
        resolution (float or None): If not None (default), sets st. dev. for Gaussian kernel (sigma=resolution*binsize).
        clr (np array): Specifies a separate color for each unique event (ex: CS+ and CS-)
        ylabels (list): Y labels for axis 1 (original signal aligned to reference event) and axis 2 (event PSTH).
        baselinewindow (np array or None): For 1d array, sets same baseline window for all events. 2d array specifies different window for each reference time. If None, does not normalize.
        fig (subfigure or None): If not None (default), plot PSTH in a given subfigure (ex: fig = fig.subfigures(2,1)).

    Returns:
        Plot of signal PSTH.
    """
    if ~isinstance(reference, list):
        # If you want to plot events according to a signal reference but did not give list as input, rescued here
        reference = [reference]
    if axes is None:
        # Create axes if not given as input
        fig, axes = plt.subplots(2, 1)
        ax1 = axes[0]
        ax2 = axes[1]
        fig.suptitle(mousename)
    else:
        # Point ax1 and ax2 to axes object passed as input (for including multiple mice in same subplot)
        ax1 = axes[0]
        ax2 = axes[1]
    itrial = 1
    # plot PSTH of each reference (ex: CS+ and CS-)

    for i, ref_label in enumerate(reference):
        aligned_signal, meanpsth, sempsth, psthtime = align_signal_to_reference(signal, timestamp, eventlog, ref_label,
                                                                                window, resolution, baselinewindow=baselinewindow)

        # If orderby is not None, then reorder aligned signal by relevant event
        if orderby == 'ibi':  # This might need revision b/c might only make sense in the context of a specific 'reference'
            lickbout_threshold = analysis_params['lickbout_threshold']
            event_dict = beh.behaviorevents_todict(eventlog)
            ilis = beh.findilis(event_dict['lick_start'])
            ibis = beh.findibis(ilis, lickbout_threshold)
            #TODO(annie-taylor): revise statement below to generalize
            event_ts = eventlog[eventlog[:, 0] == ref_label, 1]
            ibi_subset, _ = beh.ixinearevent(ibis[:, 0], ibis[:, 1], event_ts, order='preceding')
            ordered_idx = np.argsort(ibi_subset)
            aligned_signal = aligned_signal[ordered_idx, :]
        elif orderby == 'iri':
            solenoidthreshold = 1 * behav_params['max_solenoid_opentime']
            event_dict = beh.behaviorevents_todict(eventlog)
            iris = beh.findiris(event_dict, solenoidthreshold, behav_params)
            # TODO(annie-taylor): revise statement below to generalize
            event_ts = eventlog[eventlog[:, 0] == ref_label, 1]
            iri_subset, _ = beh.ixinearevent(iris[:, 0], iris[:, 1], event_ts, order='preceding')
            ordered_idx = np.argsort(iri_subset)
            aligned_signal = aligned_signal[ordered_idx, :]
        dx = (psthtime[1] - psthtime[0]) / 2
        im = ax1.imshow(aligned_signal, extent=[(window[0] - dx) / 1000, (window[-1] + dx) / 1000, itrial - 0.5,
                                               np.shape(aligned_signal)[0] + itrial + 0.5],
                        aspect='auto')
        ax2.fill_between(psthtime / 1000, meanpsth + sempsth, meanpsth - sempsth, alpha=0.3, facecolor=clr[i],
                         linewidth=0)
        ax2.plot(psthtime / 1000, meanpsth, color=clr[i])
        itrial = itrial + len(aligned_signal)
    ax1.plot([0, 0], [0, itrial], 'k:', linewidth=0.35)  # Plot vertical dotted black line at reference time
    # Specify visual parameters for plots
    ax2ylim = [np.floor(ax2.get_ylim()[0]), np.ceil(ax2.get_ylim()[1])]
    ax2.plot([0, 0], ax2ylim, 'k:', linewidth=0.35)
    ax1.set_xlim(window[0] / 1000, window[1] / 1000)
    ax2.set_xlim(window[0] / 1000, window[1] / 1000)
    ax1.set_ylim(0.5, itrial + 0.5)
    ax2.set_ylim(ax2ylim[0], ax2ylim[1])
    ax2.set_xlabel('Time (s)')
    ax1.set_ylabel(ylabels[0])
    ax2.set_ylabel(ylabels[1])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    return fig, axes


def cumulative_analysis(signal, xmaxwrtchangetrial):
    """Perform cumulative analysis i.e. find critical trial at which behavior appears to have been learned by.
    TODO(annie-taylor): does this belong in this module?

    Args:
        signal (np array): Cue response (i.e. df/f at cue time) for each trial in chronological order.
        xmaxwrtchangetrial : If not NaN, only do analysis in window of [-x x*xmaxwrtchangtrial] from changetrial.
        The exact value of abruptness depends on the ratio of trial numbers b/w before and after change trial,
        so to compare abruptness across different animals, xmaxwrtchangetrial needs to be same.

    Returns:
        abruptness, changetrial, cumsignal, signalx
    """
    signalx = np.arange(1, len(signal) + 1) / (len(signal) + 1)  # Normalize x-axis (maximum is 1)
    cumsignal = np.cumsum(signal) / np.sum(signal)  # Cumulative sum of signal
    # Find distance of each point from the diagonal line
    distance = [norm(np.cross(np.subtract([1, 1], [0, 0]), np.subtract([x, y], [1, 1]))) / norm(np.subtract([1, 1], [0, 0]))
         for x, y in zip(signalx, cumsignal)]
    abruptness = max(distance)  # Abruptness of change = point with max distance from the diagonal
    changetrial = distance.index(abruptness)  # Identify the trial where the distance is maximum
    # If xmaxwrtchangetrial is not nan, calculate abruptness again using [-changetrial changetrial*(xmaxwrtchangetrial-1)] wrt changetrial
    if ~np.isnan(xmaxwrtchangetrial):
        cumsignal = np.cumsum(signal[:round(changetrial * xmaxwrtchangetrial)]) / np.sum(
            signal[:round(changetrial * xmaxwrtchangetrial)])
        signalx = np.arange(1, round(changetrial * xmaxwrtchangetrial) + 1) / (
                    round(changetrial * xmaxwrtchangetrial) + 1)
        d = [
            norm(np.cross(np.subtract([1, 1], [0, 0]), np.subtract([x, y], [1, 1]))) / norm(np.subtract([1, 1], [0, 0]))
            for x, y in zip(signalx, cumsignal)]
        abruptness = max(d)
    return abruptness, changetrial, cumsignal, signalx


def plotcorrelation_allmice(rhos, pvals, title, filename=None, show=False):
    mouselist = rhos.keys()

    fig, axs = plt.subplots(1, 2)
    for mouse_idx, mouse in enumerate(mouselist):
        fig, axs = plotcorrelation_permouse(rhos[mouse], pvals[mouse], mouse, axs=axs,
                                            fig=fig)
    # Set axis labels, titles
    axs[0].set_title('rho')
    axs[0].set_xlabel('days')
    axs[1].set_title('p-value')
    axs[1].set_xlabel('days')
    # Set figure title
    fig.suptitle(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)

    # Save file if indicated
    if filename is not None:
        plt.savefig('figures/' + filename, bbox_inches='tight')
    # Display if indicated
    if show:
        plt.show()
    return fig, axs


def plotcorrelation_permouse(rhos, pvals, mousename, title=None, filename=None, show=False, axs=None, fig=None):
    """Plot correlation analysis between specified behavioral variable and photoemtry data for listed sessions.
    TODO(annie-taylor): update documentation!!!
    Args:
        photometryfiles (dictionary): Dictionary mapping the day of a particular session to the name of the pickle file with corresponding photometry data.
        eventlogs (dictionary): Dictionary mapping the day of a particular session to the eventlog with corresponding behavioral data.
        daylist (list): List of all days with sessions to be included in correlation analysis.
        corrfunction (function): Specific function to be used for correlation analysis (i.e. IRI versus ILI). TODO(@annie-taylor) this will need to change when you consolidate correlation functions.
        title (string): Title for plot that is generated.
        filename (string or None): If a string is given, this will be the filename of the saved figure. If None (default) figure will not be saved.
        show (boolean): If true, plot will be shown when functions is called. Default is False.
    """


    if axs is None:
        fig, axs = plt.subplots(1, 2)

    axs[0].scatter(list(rhos.keys()), list(rhos.values()), label=mousename)
    axs[1].scatter(list(pvals.keys()), list(pvals.values()), label=mousename)

    if title is not None:  # All plot settings defined here if not being used in another function
        # Set axis labels, titles
        axs[0].set_title('rho')
        axs[0].set_xlabel('days')
        axs[1].set_title('p-value')
        axs[1].set_xlabel('days')
        # Set figure title
        fig.suptitle(title)
        plt.legend()

    # Save file if indicated
    if filename is not None:
        plt.savefig('figures/' + filename, bbox_inches='tight')
    # Display if indicated
    if show:
        plt.show()
    return fig, axs
