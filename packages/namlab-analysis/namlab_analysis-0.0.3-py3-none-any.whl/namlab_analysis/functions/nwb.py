# -*- coding: utf-8 -*-
"""NWB formatting functions module.

This module contains a set of functions for NWB formatting.
"""

from datetime import datetime
import numpy as np
from dateutil import tz
from pynwb import NWBFile, NWBHDF5IO, ProcessingModule, get_manager, TimeSeries
from pynwb.file import Subject
from pynwb.core import DynamicTableRegion
from pynwb.ophys import RoiResponseSeries, DfOverF, TwoPhotonSeries, OpticalChannel
from pynwb.ogen import OptogeneticStimulusSite
from ndx_photometry import FibersTable, ExcitationSourcesTable, FiberPhotometry,\
    PhotodetectorsTable, FluorophoresTable, MultiCommandedVoltage
from ndx_events import AnnotatedEventsTable, LabeledEvents, TTLs
from hdmf.backends.hdf5 import H5DataIO
import os
from . import data_io as dataio
from . import photometry as photometry
import suite2p.io as io
import h5py
import pandas

manager = get_manager()

def generateNWB(animalname, behaviorfile, day, surgerylog):
    """ Function to generate a nwb file using raw behavior mat file.

    Args:
        animalname (str): Animal name.
        behaviorfile (str): Full path of behavior mat file.
        day (str): Session date ('Day #').
        surgerylog (panda dataframe): Surgery log. Needs to be read as panda dataframe outside this function.

    Returns:
        nwbfile (nwb): NWB file.
    """

    # load info from surgery log
    surgerylog_idx = [i for i, x in enumerate(surgerylog['Animal ID'] == animalname) if x][0]
    serial_number = int(surgerylog['Serial number'][surgerylog_idx])  # animal id
    DOB = surgerylog['DOB'][surgerylog_idx].split('/')  # DOB
    DOB = datetime(int(DOB[-1]), int(DOB[0]), int(DOB[1]))
    sex = surgerylog['Sex'][surgerylog_idx]
    genotype = surgerylog['Genotype'][surgerylog_idx]

    # find time when behavior mat file was saved
    file_create_time = os.path.split(behaviorfile)[-1].split(animalname+'_')[1].split('_')[1]
    file_create_time = datetime(int('20' + file_create_time[:2]), int(file_create_time[2:4]),
                                int(file_create_time[4:6]), int(file_create_time[7:9]),
                                int(file_create_time[9:11]), int(file_create_time[11:13]),
                                tzinfo=tz.gettz('US/Pacific'))

    # Create nwb file
    nwbfile = NWBFile(
        session_description=os.path.basename(behaviorfile).split(animalname+'_')[-1].split('_')[0],  # task mode (e.g., randomrewards, cues, ...)
        identifier=animalname,  # animal name
        session_start_time=file_create_time,  # time when mat file was saved
        session_id='Day'+str(day),  # session number ('Day')
        lab='Namboodiri lab',
        institution='University of California, San Francisco'
    )

    # Add subject module
    nwbfile.subject = Subject(
        subject_id=animalname,  # animal name
        age='P' + str(file_create_time.date() - DOB.date()) + 'D',  # age at the session
        description='#' + str(serial_number),  # serial number at surgery log
        species='Mus musculus',
        sex=sex,
        genotype=genotype
    )

    nwbfile = addBeh(nwbfile, behaviorfile)

    return nwbfile


def addBeh(nwbfile, behaviorfile):
    """ Function to add eventlog and params from matlab event file in the NWB file. Timestamps in seconds.

        Args:
            nwbfile (nwb): NWB file w/o behavior data.
            behaviorfile (str): Full path of behavior mat file.

        Returns:
            nwbfile (nwb): New NWB file w/ behavior data.
    """

    # Code for each event type in eventlog
    eventcode = {
        0: 'session end time',
        1: 'Lick1 onset', 2: 'Lick1 offset', 3: 'Lick2 onset', 4: 'Lick2 offset', 5: 'Lick3 onset', 6: 'Lick3 offset',
        7: 'Background solenoid', 8: 'Fixed solenoid 1', 9: 'Fixed solenoid 2', 10: 'Fixed solenoid 3',
        11: 'Fixed solenoid 4', 12: 'Lick retract solenoid 1', 13: 'Lick retract solenoid 2',
        14: 'Vacuum (trial end)',
        15: 'sound 1', 16: 'sound 2', 17: 'sound 3', 18: 'sound 4',
        21: 'light 1', 22: 'light 2', 23: 'light 3', 24: 'light 4',
        30: 'frame',
        31: 'laser',
        35: 'lick retract solenoid 1 and 2'}

    # make event code as a form of label for LabeldEvents object
    labels = [''] * (max(eventcode) + 1)
    for ie in eventcode.keys():
        labels[ie] = eventcode[ie]

    # load behavior mat data
    behdata = dataio.load_mat(behaviorfile)

    # Find event types that were logged in the session
    unique_eventcodes = np.unique(behdata['eventlog'][:, 0])

    # create a new LabeledEvents and TTLs type to hold eventlog recorded from arduino
    # eventCode: first column of raw eventlog from matlab behavior file
    # eventFlag: third column of raw eventlog from matlab behavior file
    event_code = LabeledEvents(
        name='eventCode',
        description='the first column of raw eventlog, which indicates code of each event',
        timestamps=(behdata['eventlog'][:, 1] / 1000).tolist(),  # units: s
        data=behdata['eventlog'][:, 0].tolist(), # units: s
        labels=labels
    )
    event_flag = TTLs(
        name='eventFlag',
        description='the third column of raw eventlog, which indicates either solenoid omission or cue identity in '
                    'sequential conditioning task; solenoid omission: 0=solenoid open, 1=no solenoid open; '
                    'cue identity: 0=first cue, 1= second cue.',
        timestamps=(behdata['eventlog'][:,1]/1000).tolist(), # unit: s
        data=behdata['eventlog'][:,2].tolist(),
    )

    # Generate a new AnnotatedEventsTable to hold task parameters
    # each row of the table represents a single task parameter
    parameters = AnnotatedEventsTable(
        name='taskParameters',
        description='Task parameters.'
    )

    # Add a task parameter (row) to the AnnotatedEventsTable instance
    # This table does not have event_times. Ignore the event_times column
    for ip in behdata['params'].keys():
        parameters.add_event_type(
            label=ip,  # parameter name
            event_description=str(behdata['params'][ip]),  # parameter values
            event_times=[] # unused
        )

    # add eventlog (eventCode, eventFlag) and parameters(taskParameters) to acquisition module
    nwbfile.add_acquisition(event_code)
    nwbfile.add_acquisition(event_flag)
    nwbfile.add_acquisition(parameters)

    return nwbfile

def addPhotometry(nwbfile, photometryfile, behaviorfile, surgerylog, doricversion=5, binsize_dff = 10,
                      excitation=[(470,'doric minicube built-in led'), (405,'doric minicube built-in led')],
                      preprocessed=None):
    """ Function to add photometry data in the NWB file. Currently, it assumes that data was recorded from single area.
    It can be expanded later if needed. Timestamps in seconds.

    Args:
        nwbfile (nwb): NWB file w/o photometry data.
        photometryfile (str): Full path of photometry file (.doric or .ppd).
        behaviorfile (str): Full path of behavior file (.mat).
        surgerylog (panda dataframe): Surgery log. Needs to be read as panda dataframe outside this function.
        doricversion (int): Version number of doric recording software. Version 5 and 6 are slightly different in
            a way of data saving.
        binsize_dff (int): Final bin size of your dff (ms).
        excitation (tuple list): List of excitation sources. tuple = (wavelength (nm), description)
        preprocessed (None or str): If None, preprocess data here. If str, which should be the full path of
            preprocessed data file, load it and save into nwb file. It's not fully developed yet.
        TODO(@HuijeongJeong): needs to develop the algorithm to load the preprocessed data from outside, instead of doing preprocessing inside of this function

    Returns:
        nwbfile (nwb): New NWB file w/ photometry data.
    """

    # default data names in doric and pyphotomtry recording system
    doricdatanames = ['AIn-1 - Dem (AOut-1)', 'AIn-1 - Dem (AOut-2)', 'DI--O-1', 'DI--O-2']
    ppddatanames = ['analog_1', 'analog_2', 'digital_1', 'digital_2']
    # new data names
    datanames_new = ['405', '470', 'ttl1', 'ttl2']

    # get animal name
    animal_name = nwbfile.subject.subject_id

    # read virus and fiber information from the surgery log
    surgerylog_idx = [i for i, x in enumerate(surgerylog['Animal ID'] == animal_name) if x][0]
    virus = surgerylog[[x for x in surgerylog.columns.values if 'photometry virus' in x][0]][surgerylog_idx]
    if virus != virus:
        name_virus = 'nan'
        coordinate_virus = 'nan'
    else:
        name_virus = virus.split(';')[0]
        coordinate_virus = virus.split(';')[1]
    fiber = surgerylog[[x for x in surgerylog.columns.values if 'photometry fiber' in x][0]][surgerylog_idx]
    if fiber != fiber:
        coordinate_fiber = 'nan'
        note_fiber = 'nan'
    else:
        coordinate_fiber = fiber.split(';')[0]
        if len(fiber.split(';')) > 1:   # if there's a note for fiber (like angle, efficiency, etc.), read it
            note_fiber = fiber.split(';')[1]
        else:
            note_fiber = 'nan'

    # create a fluorophore table
    fluorophores_table = FluorophoresTable(
        description='fluorophores'
    )
    fluorophores_table.add_row(
        label=name_virus,
        location=coordinate_virus
    )

    # create a fiber table
    fibers_table = FibersTable(
        description='fibers'
    )

    # create an excitation source table
    excitationsources_table = ExcitationSourcesTable(
        description='excitation sources table')
    for ie in excitation:
        excitationsources_table.add_row(
            peak_wavelength=float(ie[0]),
            source_type=ie[1],
        )

    # create a photodetector table
    photodetectors_table = PhotodetectorsTable(
        description="photodetectors table"
    )
    photodetectors_table.add_row(
        type="doric minicube built-in detector",
    )

    # add the metadata table containing info related to photometry to the metadata section
    nwbfile.add_lab_meta_data(
        FiberPhotometry(
            fibers=fibers_table,
            fluorophores=fluorophores_table,
            excitation_sources=excitationsources_table,
            photodetectors=PhotodetectorsTable(description='photodetectors table'),
            commanded_voltages=MultiCommandedVoltage()
        )
    )

    # Important: we add the fibers to the fibers table AFTER adding the metadata
    # This ensures that we can find this data in their tables of origin
    fibers_table.add_fiber(
        excitation_source=0,  # integers indicated rows of excitation sources table
        photodetector=0,
        fluorophores=[0],  # potentially multiple fluorophores, so list of indices
        location=coordinate_fiber,
        notes=note_fiber
    )

    # create a dynamic table containing a list of fibers that recording came from
    rois = DynamicTableRegion(
        name="rois",
        data=[0],  # potentially multiple fibers
        description="source fibers",
        table=fibers_table
    )

    # load photometry data
    if '.ppd' in photometryfile: # pyphotometry
        photometry_data = dataio.load_ppd(photometryfile, ppddatanames, datanames_new)
    elif '.doric' in photometryfile: # doric
        photometry_data = dataio.load_doric(photometryfile, doricversion, doricdatanames, datanames_new)

    # create raw RoiResponseSeries, save them in acquisition module. It saves 405nm, 470nm, ttl1, and ttl2 data consequently.
    # acquisition module contains raw, 'acquired' data, which should never change.
    for icol in datanames_new:
        photometry_raw = RoiResponseSeries(
            name="photometry_" + icol,
            description="photometry_raw_" + icol,
            data=H5DataIO(photometry_data[icol], compression=True),
            unit='F',
            timestamps=H5DataIO([x/1000 for x in photometry_data['time']], compression=True), # units: s
            rois=rois
        )
        nwbfile.add_acquisition(photometry_raw)

    # set the event code of ttl2 in photometry file depending on task mode
    taskmode = os.path.split(behaviorfile)[-1].split(animal_name + '_')[1].split('_')[0]
    if taskmode in {'randomrewards'}:
        ttl2matindex = [7] # background reward
    else:
        ttl2matindex = [15, 16, 17, 18, 21, 22, 23, 24] # any auditory or visual cues

    # preprocess raw data to sync time stamps across behavior and photometry files, and calculate dff
    if preprocessed==None:
        dff, time = photometry.preprocessing(photometry_data, dataio.load_mat(behaviorfile), binsize_dff, ttl2matindex)
    # this is for later development in case someone wants to save their own already-calculated dff
    # else:

    # create dff RoiResponseSeries
    photometry_dff = RoiResponseSeries(
        name="photometry_dff",
        description="dff",
        data=H5DataIO(dff, compression=True),
        unit='dF/F',
        timestamps=H5DataIO([x/1000 for x in time], compression=True), # units: s
        rois=rois
    )
    dff = DfOverF(roi_response_series=photometry_dff)

    # create ophys_fp processing module and save dff to it.
    # processing module contains processed data (here, dff), which are results of preprocessing algorithms and could change.
    ophys_module = ProcessingModule(
        name='ophys_fp',
        description='fiber photometry processed data'
    )
    ophys_module.add(dff)
    nwbfile.add_processing_module(ophys_module)

    return nwbfile

def addOpto(nwbfile, surgerylog):
    """ Function to add optogenetics related info from surgery log in NWB file. Currently,
    it assumes that opto stimulation was performed in a single area w/ single virus. It can be expanded later if needed.

    Args:
        nwbfile (nwb): NWB file w/o photometry data.
        surgerylog (panda dataframe): Surgery log. Needs to be read as panda dataframe outside this function.

    Returns:
        nwbfile (nwb): New NWB file w/ opto data.
    """

    # get animal name
    animal_name = nwbfile.subject.subject_id

    # read virus and fiber information from the surgery log
    surgerylog_idx = [i for i, x in enumerate(surgerylog['Animal ID'] == animal_name) if x][0]
    optowavelength = surgerylog[[x for x in surgerylog.columns.values if 'Opto wavelength' in x][0]][surgerylog_idx]
    if np.isnan(optowavelength):
        return nwbfile
    virus = surgerylog[[x for x in surgerylog.columns.values if 'Opto virus' in x][0]][surgerylog_idx]
    if virus != virus:
        name_virus = 'nan'
        coordinate_virus = 'nan'
    else:
        name_virus = virus.split(';')[0]
        coordinate_virus = virus.split(';')[1]
    fiber = surgerylog[[x for x in surgerylog.columns.values if 'Opto fiber' in x][0]][surgerylog_idx]
    coordinate_fiber = fiber.split(';')[0]
    if len(fiber.split(';')) > 1:  # if there's a note for fiber (like angle, efficiency, etc.), read it
        note_fiber = fiber.split(';')[1]
    else:
        note_fiber = 'nan'

    # reate optogenetic device (e.g., laser)
    device = nwbfile.create_device(
        name='laser',
        description='laser for optogenetic stimulation'
    )

    # Create OptogeneticStimulusSite. This object saves opto-related info from surgery log.
    ogen_stim_site = OptogeneticStimulusSite(
        name='OptogeneticStimulusSite',
        device=device,
        description='virus: '+name_virus+'; coordinate_virus: '+coordinate_virus+'; note_fiber: '+note_fiber,
        excitation_lambda=optowavelength,
        location=coordinate_fiber
    )

    # add opto info in nwbfile
    nwbfile.add_ogen_site(ogen_stim_site)

    return nwbfile


def add2P(nwbfile, surgerylog, datadir, save_h5=True):
    """ Function to add 2p data in NWB file. 1) Convert raw tiff files into HDF5 dataset and save them in input nwbfile.
    2) Incorporate suite2p pre-processing results into the input nwbfile. You must run suite2p first before running this,
    and save the suite2p result as nwb format (set 'save_nwb' as 1 in suite2p GUI). The temporary nwb file that was
    automatically generated from suite2p preprocessing will be deleted at the end.

    Args:
        nwbfile (nwb): NWB file w/o 2p data.
        surgerylog (panda dataframe): Surgery log. Needs to be read as panda dataframe outside this function.
        datadir (str): 2p data directory.
        save_h5 (boolean): Whether to save a separate HDF5 file of raw imaging data. If this is False, raw data will be
        only stored inside NWB file.
    Returns:
        nwbfile (nwb): New NWB file w/ 2p data.
    TODO@HuijeongJeong): need to sync timestamp to eventlog later
    """

    # Convert raw tiff files into HDF5 dataset
    #opsfile = os.path.join(datadir, 'suite2p', 'plane0', 'ops.npy')
    #ops = np.load(opsfile, allow_pickle=True).item()
    #fs, _ = io.utils.get_tif_list(ops)
    fs, _ = dataio.findfiles(datadir,['.tif'])
    fs = [x for x in fs if '.ome' in x]
    for ik, file in enumerate(fs):
        # open tiff
        tif, Ltif = io.tiff.open_tiff(file, False)
        im_temp = tif.data()

        # for single-page tiffs, add 1st dim
        if len(im_temp.shape) < 3:
            im_temp = np.expand_dims(im_temp, axis=0)

        # check if uint16
        if im_temp.dtype.type == np.uint16:
            im_temp = (im_temp // 2).astype(np.int16)
        elif im_temp.dtype.type == np.int32:
            im_temp = (im_temp // 2).astype(np.int16)
        elif im_temp.dtype.type != np.int16:
            im_temp = im_temp.astype(np.int16)

        if ik == 0:
            im = im_temp
        else:
            im = np.append(im, im_temp, axis=0)

    # get animal name
    animal_name = nwbfile.subject.subject_id

    # read virus and fiber information from the surgery log
    surgerylog_idx = [i for i, x in enumerate(surgerylog['Animal ID'] == animal_name) if x][0]
    virus = surgerylog[[x for x in surgerylog.columns.values if '2p virus' in x][0]][surgerylog_idx]
    if virus != virus:
        virus = 'nan'
    lens = surgerylog[[x for x in surgerylog.columns.values if '2p lens' in x][0]][surgerylog_idx]
    if lens != lens:
        coordinate_lens = 'nan'
    else:
        coordinate_lens = lens.split(';')[0]

    xmlfile,_ = dataio.findfiles(datadir,['.xml'])
    timestamps = pandas.read_xml(xmlfile[0], xpath='.//Frame')
    timestamps = list(timestamps['absoluteTime'])

    metadata = pandas.read_xml(xmlfile[0], xpath='.//PVStateValue')
    imaging_rate = round(1 / float(metadata[metadata['key'] == 'framePeriod']['value'].iloc[0]), 2)
    device = nwbfile.create_device(
        name="Microscope",
        description="two-photon microscope",
        manufacturer="Bruker",
    )

    metadata = pandas.read_xml(xmlfile[0], xpath='.//IndexedValue')
    pmtgain = round(metadata[metadata['description']=='PMT 2 HV']['value'].iloc[0],3)
    laserpower = round(metadata[metadata['description']=='Pockels']['value'].iloc[0],3)
    excitationwavelength = metadata[metadata['description']=='Excitation 1']['value'].iloc[0]
    optical_channel = OpticalChannel(
        name="OpticalChannel",
        description="green channel",
        emission_lambda=510.0
    )
    imaging_plane = nwbfile.create_imaging_plane(
        name="ImagingPlane",
        optical_channel=optical_channel,
        imaging_rate=imaging_rate,
        description='',
        device=device,
        excitation_lambda=excitationwavelength,
        indicator=virus,
        location=coordinate_lens
    )
    two_p_series = TwoPhotonSeries(
        name="2p",
        data=H5DataIO(im, compression=True),
        imaging_plane=imaging_plane,
        unit='normalized amplitude',
        timestamps=timestamps,
        pmtgain=pmtgain
    )
    nwbfile.add_acquisition(two_p_series)

    # save HDF5 file in data directory. Once you check this HDF5 file is okay, you can erase the original tiff files
    # from your local directory. You may store original tiff files in the server. If saveh5 is true, keep a separate
    # HDF5 file outside the NWB file as well. If not, HDF5 dataset will be stored only in the NWB file, and created HDF5
    # file will be deleted at the end of this code.
    if save_h5:
        dataname = os.path.basename(file).split('-')[0]
        f = h5py.File(os.path.join(os.path.dirname(datadir), dataname + '_raw.h5'), 'w')
        h5 = f.create_dataset('data', data=im)
        f.close()

    # link the nwb file generated from suite2p to the processing module of main nwb file, which was given as an input
    # of the function ('nwbfile')
    #nwbfiledir_suite2p, _ = dataio.findfiles(datadir, ['.nwb'], [], [])
    #io_suite2p = NWBHDF5IO(nwbfiledir_suite2p[0], mode='r', manager=manager)
    #nwbfile_suite2p = io_suite2p.read()
    #io_suite2p.close()
    #ophys_module = nwbfile_suite2p.get_processing_module('ophys')
    #ophys_module_data = ophys_module.data_interfaces
    #ophys_2p_module = ProcessingModule(
        #    name="ophys_2p",
        #    description='2p processed data via suite2p',
        #     data_interfaces=H5DataIO(ophys_module_data,link_data=True)
        # )
    # timeseries = TimeSeries(
        #     name="timestamps",
        #      description="timestamps for external suite2p nwb file",
        #      data=timestamps,
        #      unit='s',
    #       rate=imaging_rate
    #   )
    #   ophys_2p_module.add_data_interface(timeseries)
    #    nwbfile.add_processing_module(ophys_2p_module)

    return nwbfile

def iterate_nwb(animallist, daylist, savedir, datadir_beh, datadir_2p, surgerylogname = 'Namboodiri lab Surgery log'):
    """ Function to iteratively run generateNWB across multiple sessions and animals, so that convert all data into nwb
     files. Each session will have one nwb file containing behavior data and any other recording data. Your data folder
     structure (both datadir_beh and datadir_2p) needs to be 'Animalname/.../DayXX/'. Each Day folder should contain raw
     matlab data file and any other raw recording files (e.g., photometry or 2p data file). Make sure to not use same
     day number multiple times per animal.

    Args:
        animallist (str list): NWB file w/o behavior data.
        daylist (int list): Full path of behavior mat file.
        savedir (str): Directory of your NWB files.
        datadir_beh (str): Directory of raw behavior files and photometry files.
        datadir_2p (str): Directory of raw 2p files.
    """

    # read surgery log from google sheet
    surgerylog = dataio.load_googlesheet(surgerylogname)
    #surgerylog = surgerylog[0] # always read the first sheet
    surgerylog = surgerylog[1]  # always read the first sheet

    for ia in animallist:
        # make new folder w/ animal name in savedir
        if not os.path.exists(os.path.join(savedir, ia)):
            os.mkdir(os.path.join(savedir, ia))

        # find behavior files ('.mat')
        [beh_files, days] = dataio.findfiles(datadir_beh, '.mat', ia, daylist)

        # convert files to nwb file for each session (day)
        for iF, iD in zip(beh_files, days):
            # create nwb file containing behavior data and basic information
            nwbfile = generateNWB(ia, iF, iD, surgerylog)

            # add opto info from surgery log to nwb file
            nwbfile = addOpto(nwbfile, surgerylog)

            # find photometry file ('.ppd' or '.doric')
            photometry_file, _ = dataio.findfiles(os.path.dirname(iF), ['.ppd', '.doric'], ia.split('_')[-1], [])
            if len(photometry_file) >0:
                # if there's more than one photometry in the same folder, ask to select
                if len(photometry_file) > 1:
                    print('List of photometry files:')
                    for ip in photometry_file:
                        print(ip)
                    print('Enter which file do you want to use (e.g., first one=0, second one=1, ...):')
                    x = int(input())
                elif len(photometry_file) == 1:
                    x = 0

                # add photometry related data to nwb file
                nwbfile = addPhotometry(nwbfile, photometry_file[x], iF, surgerylog)

            # find xml file under datadir_2p. This will add raw 2p file to nwb file.
            twophoton_file, _ = dataio.findfiles(os.path.join(datadir_2p,ia), ['.xml'], [], [])
            #twophoton_file = [x for x in twophoton_file if os.path.basename(x)=='ops.npy']
            if len(twophoton_file) > 0:
                # if there's more than one photometry in the same folder, ask to select
                if len(twophoton_file) > 1:
                    print('List of 2p files:')
                    for ip in twophoton_file:
                        print(ip)
                    print('Enter which file do you want to use (e.g., first one=0, second one=1, ...):')
                    x = int(input())
                elif len(twophoton_file) == 1:
                    x = 0

                # add photometry related data to nwb file
                #twophoton_dir = twophoton_file[x].split('\suite2p')[0]
                nwbfile = add2P(nwbfile, surgerylog, os.path.dirname(twophoton_file[0]))

            # write nwb file
            filename = os.path.join(savedir, ia, 'Day'+str(iD),
                                    ia + '_' + iF.split(nwbfile.session_description + '_')[-1].split('-')[0] + '.nwb')
            with NWBHDF5IO(filename, mode='w', manager=manager) as nwbio:
                nwbio.write(nwbfile)


def openNWB(datadir):
    """ Function to open NWB file.

        Args:
            datadir (str): Data directory of NWB file
        Returns:
            nwbfile (NWB): Opened NWB file

    """
    nwbio = NWBHDF5IO(datadir, 'r')
    nwbfile = nwbio.read()
    return nwbfile

def readEvent(nwbfile):
    """ Function to read event-related information from NWB file.

        Args:
            nwbfile (NWB): NWB file
        Returns:
            eventTime (float list): Timestamps of event. This corresponds to the second column of matlab eventlog variable.
            eventCode (int list): Series of event code. This corresponds to the first column of matlab eventlog variable.
            eventFlag (boolean list): Series of event omission (or first cue in sequential conditioning) code. This
            corresponds to the third column of matlab eventlog variable.
            taskParameters (pandas dataframe): Table of task parameters. This corresponds to the matlab params variable.
    """
    eventTime = nwbfile.acquisition['eventCode'].timestamps[:]
    eventCode = nwbfile.acquisition['eventCode'].data[:]
    eventFlag = nwbfile.acquisition['eventFlag'].data[:]
    taskParameters = nwbfile.acquisition['taskParameters'].to_dataframe()
    taskParameters = taskParameters.drop('event_times',axis=1)
    return eventTime, eventCode, eventFlag, taskParameters

def readOphys(nwbfile,type,deconvolved=True):
    """ Function to read ophys data from NWB file.

        Args:
            nwbfile (NWB): NWB file
            type (str: 'photometry' or '2p'): This determines which ophys data type to read.
            deconvolved (boolean): This determines whether to load deconvoluted spikes or fluorescence from 2p data.
            This parameter doesn't play a role for photometry data.
        Returns:
            timestamps (float list): Timestamps of data.
            ophysData (float list or dictionary): Timeseries of data. If there's more than one plane in 2p data, the
            data from each plane is stored in each entry of dictionary.
    """

    if type=='photometry':
        moduleFP = nwbfile.processing['ophys_fp']['DfOverF'].roi_response_series['photometry_dff']
        timestamps = moduleFP.timestamps[:]
        ophysData = moduleFP.data[:]
    elif type=='2p':
        timestamps = nwbfile.acquisition['2p'].timestamps[:]
        iscell = nwbfile.processing['ophys_2p']['ImageSegmentation']['PlaneSegmentation'].iscell[:]
        if deconvolved:
            module2p = nwbfile.processing['ophys_2p']['Deconvolved'].roi_response_series
        else:
            module2p = nwbfile.processing['ophys_2p']['Fluorescence'].roi_response_series
        planes = list(module2p.keys())
        ophysData = {}
        for ip in planes:
            ophysData[ip] = np.swapaxes(module2p[ip].data[:,iscell[:,0]==1],0,1)
        if len(ophysData)==1:
            ophysData = ophysData[ip]
    return timestamps, ophysData

def linkSuite2p_toNWBs(nwbfile_suite2p,datadir,mousename,days):
    """ Function to link one suite2p-generated NWB file containing 2p data from multiple sessions to multiple NWB files
    including behavior data for each session. This is specifically for the tracking cells across multiple sessions. You
    should generate NWB files containing behavior data for each session using iterate_nwb first before running this
    function. Suite2p data is linked to the '2p' processing module of each session NWB file with timestamps. Data with
    NAN timestamp is from other session.

        Args:
            nwbfile_suite2p (NWB): NWB file automatically generated from suite2p.
            datadir (str): Data directory. This should contain Day folders of NWB files containing behavior data (Ex: datadir/Day1, datadir/Day2).
            mousename (str): Name of mouse. Day folders should be under mousename folder. Datadir can include mousename
            folder or not.
            days (int list): List of session numbers (Ex: [1,2] if you run suite2p file includes data from Day1 and Day2)
        """

    io_suite2p = NWBHDF5IO(nwbfile_suite2p, mode='r', manager=manager)
    suite2p_data = io_suite2p.read()
    ophys_module = suite2p_data.get_processing_module('ophys')
    ophys_module_data = ophys_module.data_interfaces

    nwbfiles,_ = dataio.findfiles(datadir,'.nwb',mousename,days)
    ophys_2p_module = ProcessingModule(
        name="ophys_2p1",
        description='2p processed data via suite2p',
        data_interfaces=ophys_module_data,
    )

    startframe = 0
    for ifile in nwbfiles:
        io_nwb = NWBHDF5IO(ifile, mode='r+',manager=manager)
        nwbfile = io_nwb.read()
        nframe = nwbfile.acquisition['2p'].data.shape[0]
        timestamps_raw = nwbfile.acquisition['2p'].timestamps[:]
        imaging_rate = nwbfile.acquisition['2p'].imaging_plane.imaging_rate

        timestamps_new = np.empty((ophys_2p_module['Deconvolved']['plane0'].data.shape[0],))
        timestamps_new[:] = np.nan
        timestamps_new[startframe:startframe+nframe] = timestamps_raw
        timeseries = TimeSeries(
            name="timestamps",
            description="timestamps for external suite2p nwb file",
            data=timestamps_new,
            unit='s',
            rate=imaging_rate
        )
        ophys_2p_module_temp = ophys_2p_module
        ophys_2p_module_temp.add_data_interface(timeseries)
        nwbfile.add_processing_module(ophys_2p_module_temp)
        io_nwb.write(nwbfile)
        io_nwb.close()
    io_suite2p.close()











