# -*- coding: utf-8 -*-
"""Data IO functions module.

This module contains a set of functions for importing and manipulating data.
"""

import os
import re
import numpy as np
from scipy.io import loadmat, matlab
import h5py
import json
from scipy.signal import butter, filtfilt
import pickle
from pynwb import NWBHDF5IO, load_namespaces
from dandi.dandiapi import DandiAPIClient
import csv
import gspread
import pandas as pd


def photometrypicklefiles(directory, mousename, foldername, daylist):
    """Return filepaths for all .p files with time synchronized...

    Args:
        directory (str): String with directory containing all data.
        mouselist (str list): Array with folder names for each mouse.
        foldername (str): Folder name for the specific behavior being analyzed.
        daylist (int list): List of specific dates being analyzed.
    Returns:
        photometryfiles (dict): Maps mousename to list of pickle files with time synced photometry data for given mouse.
    """
    photometryfiles = {}
    for id, day in enumerate(daylist):
        day_key = 'Day' + str(day)
        photometryfiles[day_key], _ = findfiles(os.path.join(directory, mousename, foldername), ['.p'], mousename, [day])
    return photometryfiles

def findday(file):
    """Returns the date (day in month) from a given filename.

    Args:
        file (str): Filename.

    Returns:
        If day is in filename, return numerical date. Otherwise return 0.
    """
    if 'Day' in file:
        return int(re.split('Day|_', os.path.basename(os.path.dirname(file)))[1])
    else:
        return 0


def findfiles(directory, fileformat, mousename=[], daylist=[]):
    """Find all files with fileformat under directory if daylist is specified, only find files in certain days ex)
    daylist = [3,5]: search files in directory/mousename/Day3, directory/mousename/Day5 if daylist is empty,
    search all files in directory.

    Args:
        directory (str): String with directory containing all data.
        fileformat (str list): File format being searched. ex: '.mat'
        mousename (str): Name of mouse being analyzed.
        daylist (int list): List of specific dates being analyzed.

    Returns:
        files (str list): List of files.
        days (int list): List of dates corresponding each file.
    """

    # find files
    files = [os.path.join(root, name)
             for root, dirs, files in os.walk(directory)
             for name in files if os.path.splitext(name)[-1] in fileformat]

    # if mousename is empty, just find all files with fileformat under directory. In this case you don't have list of days
    if len(mousename) > 0:
        # find date of each file
        files = [file for file in files if mousename in file.split('\\')[-1]]
        files = sorted(files, key=findday)
        days = [findday(f) for f in files]
        files = [x for x, y in zip(files, days) if y > 0]
        days = [x for x in days if x > 0]
    else:
        days = None

    # remove files/days that are not in daylist
    if len(daylist) > 0:
        indaylist = [i for i, v in enumerate(days) if v in daylist]
        files = [files[i] for i in indaylist]
        days = [days[i] for i in indaylist]

    return files, days


def _check_vars(d):
    """ Checks if entries in dictionary are mat-objects. If yes, todict is called to change them to nested dictionaries"""
    #TODO(annie-taylor): update documentation
    for key in d:
        if isinstance(d[key], matlab.mio5_params.mat_struct):
            d[key] = _todict(d[key])
        elif isinstance(d[key], np.ndarray):
            d[key] = _toarray(d[key])
    return d


def _todict(matobj):
    """A recursive function which constructs from matobjects nested dictionaries"""
    #TODO(annie-taylor): update documentation
    d = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, matlab.mio5_params.mat_struct):
            d[strg] = _todict(elem)
        elif isinstance(elem, np.ndarray): \
                d[strg] = _toarray(elem)
        else:
            d[strg] = elem
    return d


def _toarray(ndarray):
    """A recursive function which constructs ndarray from cellarrays (which are loaded as numpy ndarrays), recursing
    into the elements if they contain matobjects."""
    #TODO(annie-taylor): update documentation
    if ndarray.dtype != 'float64':
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem, matlab.mio5_params.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif isinstance(sub_elem, np.ndarray):
                elem_list.append(_toarray(sub_elem))
            else:
                elem_list.append(sub_elem)
        return np.array(elem_list)
    else:
        return ndarray


def load_mat(filename):
    """This function should be called instead of direct scipy.io.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects

    Args:
        filename (str): Full path of mat file.

    Returns:
        data (dictionary): Dictionary of variables in mat file.
        Key corresponds to the original variable name in mat file.
    """

    data = loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_vars(data)


def ish5dataset(item):
    """Check if the given item is in HDF5 format. Function from doric.

    Args:
        item: any variable you want to know if it's format is HDF5

    Returns:
        boolean: 1 if item is HDF5, 0 if not.
    """
    return isinstance(item, h5py.Dataset)


def h5getDatasetR(item, leading=''):
    """Read data from HDF5 file. Function from doric.

     Args:
          item (h5fp file object w/ r mode): This can work as like a Python dictionary - you can access to its data using key.
          leading (str): leading string that you want to put before your key in the name (e.g., filepath)

    Returns:
        boolean: 1 if item is HDF5, 0 if not.

    """

    r = []
    for key in item:
        # First have to check if the next layer is a dataset or not
        firstkey = list(item[key].keys())[0]
        if ish5dataset(item[key][firstkey]):
            r = r + [{'Name': leading + '_' + key, 'Data':
                [{'Name': k, 'Data': np.array(item[key][k]),
                  'DataInfo': {atrib: item[key][k].attrs[atrib] for atrib in item[key][k].attrs}} for k in
                 item[key]]}]
        else:
            r = r + h5getDatasetR(item[key], leading + '_' + key)

    return r

def ExtractDataAcquisition(filename, version):
    """Main function that reads data from '.doric' file. Modified function provided by doric.

    Args:
        filename (str): Full file path of '.doric' file
        version (int): 5 or 6. Version number of Doric Neuroscience Studio. Key is different depending on version.

    Returns:
        The acquired data of '.doric' file, which includes time stamps, fluorescence signals (from 405 and 470nm), and
        TTL signals (from TTL 1 and TTL 2).
    """

    with h5py.File(filename, 'r') as h:
        if version == 5:
            return h5getDatasetR(h['Traces'])
        elif version == 6:
            return h5getDatasetR(h['DataAcquisition'])


def load_doric(filename, version, datanames, datanames_new):
    """Function to read doric data file (.doric) and save it in a namlab_analysis format.

    Args:
        filename (str): Full file path of '.doric' file
        version (int): 5 or 6. Version number of Doric Neuroscience Studio. Key is different depending on version.
        datanames (str list): Default data names in raw '.doric' file
        datanames_new (str list): The new data names. This should be the same across different photometry systems
            (doric and pyphotometry), so that we can easily access to the data using the same fundtion regardless of the
            data acquisition system.

    Returns:
        data (dict): Dictionary that stores all acquired data from doric. Keys are the datanames_new.
    """
    # TODO(HuijeongJeong): develop for version 6

    # Read doric data as a list of dictionary. Each dictionary contains default data name ('Name') in raw '.doric' file,
    # and corresponding data ('Data'). datanames should be a subset of Name of dictionaries.
    doricfile = [data["Data"][0] for data in ExtractDataAcquisition(filename, version)]

    # save data in a pretty form with datanames_new
    data = {}
    # save time
    if version == 5:
        data['time'] = [data["Data"] for data in doricfile if data["Name"] == 'Console_time(s)'][0].tolist()
    # save other data
    for i, v in enumerate(datanames):
        if version == 5:
            data[datanames_new[i]] = [data["Data"] for data in doricfile if data["Name"] == v][0].tolist()

    return data


def import_ppd(file_path, low_pass=20, high_pass=0.01):
    """Function from Pyphotometry. Function to import pyPhotometry binary data files into Python. The high_pass
    and low_pass arguments determine the frequency in Hz of highpass and lowpass filtering applied to the filtered
    analog signals. To disable highpass or lowpass filtering set the respective argument to None.

	Args:
	    file_path (str): Full file path of '.ppd' file
	    low_pass (int or float): Lower limit of bandpass filter
	    high_pass (int or float): Higher limit of bandpass filter

	Returns:
	    data_dict (dict): A dictionary containing following items:
	    'subject_ID'    - Subject ID
		'date_time'     - Recording start date and time (ISO 8601 format string)
		'mode'          - Acquisition mode
		'sampling_rate' - Sampling rate (Hz)
		'LED_current'   - Current for LEDs 1 and 2 (mA)
		'version'       - Version number of pyPhotometry
		'analog_1'      - Raw analog signal 1 (volts)
		'analog_2'      - Raw analog signal 2 (volts)
		'analog_1_filt' - Filtered analog signal 1 (volts)
		'analog_2_filt' - Filtered analog signal 2 (volts)
		'digital_1'     - Digital signal 1
		'digital_2'     - Digital signal 2
		'pulse_inds_1'  - Locations of rising edges on digital input 1 (samples).
		'pulse_inds_2'  - Locations of rising edges on digital input 2 (samples).
		'pulse_times_1' - Times of rising edges on digital input 1 (ms).
		'pulse_times_2' - Times of rising edges on digital input 2 (ms).
		'time'          - Time of each sample relative to start of recording (ms)
	"""

    with open(file_path, 'rb') as f:
        header_size = int.from_bytes(f.read(2), 'little')
        data_header = f.read(header_size)
        data = np.frombuffer(f.read(), dtype=np.dtype('<u2'))
    # Extract header information
    header_dict = json.loads(data_header)
    volts_per_division = header_dict['volts_per_division']
    sampling_rate = header_dict['sampling_rate']
    # Extract signals.
    analog = data >> 1  # Analog signal is most significant 15 bits.
    digital = ((data & 1) == 1).astype(int)  # Digital signal is least significant bit.
    # Alternating samples are signals 1 and 2.
    analog_1 = analog[::2] * volts_per_division[0]
    analog_2 = analog[1::2] * volts_per_division[1]
    digital_1 = digital[::2]
    digital_2 = digital[1::2]
    time = np.arange(analog_1.shape[0]) * 1000 / sampling_rate  # Time relative to start of recording (ms).

    # Filter signals with specified high and low pass frequencies (Hz).
    if low_pass and high_pass:
        b, a = butter(2, np.array([high_pass, low_pass]) / (0.5 * sampling_rate), 'bandpass')
    elif low_pass:
        b, a = butter(2, low_pass / (0.5 * sampling_rate), 'low')
    elif high_pass:
        b, a = butter(2, high_pass / (0.5 * sampling_rate), 'high')
    if low_pass or high_pass:
        analog_1_filt = filtfilt(b, a, analog_1)
        analog_2_filt = filtfilt(b, a, analog_2)
    else:
        analog_1_filt = analog_2_filt = None
    # Extract rising edges for digital inputs.
    pulse_inds_1 = 1 + np.where(np.diff(digital_1) == 1)[0]
    pulse_inds_2 = 1 + np.where(np.diff(digital_2) == 1)[0]
    pulse_times_1 = pulse_inds_1 * 1000 / sampling_rate
    pulse_times_2 = pulse_inds_2 * 1000 / sampling_rate
    # Return signals + header information as a dictionary.
    data_dict = {'analog_1': analog_1,
                 'analog_2': analog_2,
                 'analog_1_filt': analog_1_filt,
                 'analog_2_filt': analog_2_filt,
                 'digital_1': digital_1,
                 'digital_2': digital_2,
                 'pulse_inds_1': pulse_inds_1,
                 'pulse_inds_2': pulse_inds_2,
                 'pulse_times_1': pulse_times_1,
                 'pulse_times_2': pulse_times_2,
                 'time': time}
    data_dict.update(header_dict)
    return data_dict


def load_ppd(filename, datanames, datanames_new):
    """Function to read pyphotometry data file (.ppd) and save it in a namlab_analysis format.

    Args:
        filename (str): Full file path of '.ppd' file
        datanames (str list): Default data names in raw '.ppd' file
        datanames_new (str list): The new data names. This should be the same across different photometry systems
            (doric and pyphotometry), so that we can easily access to the data using the same fundtion regardless of the
            data acquisition system.

    Returns:
        data (dict): Dictionary that stores all acquired data from pyphotometry. Keys are the datanames_new.
    """

    data_temp = import_ppd(filename)

    # save data in a pretty form with datanames_new
    data = {}
    # save time
    data['time'] = data_temp['time'].tolist()
    # save other data
    for i, v in enumerate(datanames):
        data[datanames_new[i]] = data_temp[v].tolist()
    return data


def load_googlesheet(filename, credential_filename='credentials.json'):
    """Function to read data from google spreadsheets and save it in a panda data frame format.

    Args:
        filename (str): File name of google spreadsheets
        credential_filename (str): Credential (.json file) of a google service account to access data in Google APIs.

    Returns:
        data (dict): Dictionary that stores all acquired data from pyphotometry. Keys are the datanames_new.
    """
    gc = gspread.service_account(filename=credential_filename)
    sh = gc.open(filename)
    data = []
    for i, worksheet in enumerate(sh.worksheets()):
        filename = 'temp_' + str(i) + '.csv'
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(worksheet.get_all_values())
        data.append(pd.read_csv(filename, encoding='unicode_escape'))
        os.remove(filename)
    return data


def load_pickle(filename):
    # TODO(annie-taylor): update documentation
    # load pickle file
    objects = []
    with (open(filename, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects


def load_dandi_url(dandiset_id, animalname, daylist=None):
    # TODO(annie-taylor): update documentation
    # load url in dandi server for specific sessions of given animal
    # dandiset_id: dandi set id, which is given by dandi when you upload the data
    # animalname: name of animal, it needs to be the same with one on dandi server
    # daylist: indicator for session (the session name needs to contain 'DayXX')
    # if you don't have daylist, it will give urls for all sessions of given animal
    url = []
    path = []
    with DandiAPIClient.for_dandi_instance("dandi") as client:
        dandiset = client.get_dandiset(dandiset_id, 'draft')
        for asset in dandiset.get_assets_by_glob(animalname):
            url = np.append(url, asset.get_content_url(follow_redirects=1, strip_query=True))
            path = np.append(path, asset.get_metadata().path)

    day = [int(re.split('.nwb|-', x.split('Day')[1])[0]) for x in path]
    if not daylist == None:
        url = [y for x, y in zip(day, url) if x in daylist]
        path = [y for x, y in zip(day, path) if x in daylist]
        day = [x for x in day if x in daylist]

    url = [y for x, y in sorted(zip(day, url))]  # this is url of each session
    path = [y for x, y in
            sorted(zip(day, path))]  # this is file name, which follows this: sub_(animalname)_ses_(sessionname)

    return url, path


def load_nwb(url, namespacepath, varlist):
    # TODO(annie-taylor): update documentation
    # load nwb file using url - this needs to be developed more to be able to load saved nwb file
    # url: dandi server url
    # namespacepath: path for namespace of namboodirilab extension file
    # varlist: the list of variable you want to get
    # (a,XX): variable XX from acquisition field
    # (p,XX): variable XX from processing field
    for ipath in namespacepath:
        load_namespaces(ipath)

    io = NWBHDF5IO(url, mode='r', driver='ros3')
    nwbfile = io.read()

    results = {}
    for i in varlist:
        if i[0] == 'a':  # acquisition
            fields = nwbfile.acquisition[i[1]]._get_fields()
            subnwb = nwbfile.acquisition[i[1]]
        elif i[0] == 'p':  # processing
            fields = nwbfile.processing[i[1]][i[2]]._get_fields()
            subnwb = nwbfile.processing[i[1]][i[2]]
        else:
            fields = nwbfile.i[1]._get_fields()
            subnwb = nwbfile.i[1]
        results[i[-1]] = {}
        for f in fields:
            if not subnwb.fields.get(f) == None:
                results[i[-1]][f] = subnwb.fields.get(f)
                if not np.shape(results[i[-1]][f]) == ():
                    results[i[-1]][f] = results[i[-1]][f][:]
    return results, nwbfile
