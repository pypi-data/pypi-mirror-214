"""Utilities for loading waveform data from various formats, as well
as outputting model predictions to various formats."""
from pathlib import Path
from typing import Callable, Union
import csv
import base64
import warnings

import lxml.etree as ET
import numpy as np
import wfdb
import pyedflib

_LEADS = [
    'I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'
]

# === EDF === #
def load_edf(record_filename: Path) -> np.ndarray:
    """Load an EDF/EDF+ record."""
    f = pyedflib.EdfReader(str(record_filename.resolve()))
    n = f.signals_in_file
    signal = np.zeros((f.getNSamples()[0], n))
    for i in np.arange(n):
        signal[:, i] = f.readSignal(i)
    return signal

def write_edf(record_filename: Path, signal: np.ndarray, sampling_frequency=500):
    """Write an EDF/EDF+ record."""
    n_samples, n_channels = signal.shape

    # Create an EdfWriter object
    writer = pyedflib.EdfWriter(str(record_filename.resolve()), n_channels, pyedflib.FILETYPE_EDFPLUS)

    # Set the channel headers
    for i, channel_name in enumerate(_LEADS):
        channel_info = {
            'label': channel_name,
            'dimension': 'mV',
            'sample_frequency': sampling_frequency,
            'physical_min': signal[:, i].min(),
            'physical_max': signal[:, i].max(),
        }
        writer.setSignalHeader(i, channel_info)

    # writer.setStartdatetime(None)

    # Write the data
    writer.writeSamples([signal[:, i] for i in range(signal.shape[1])])

    # Close the file
    writer.close()

def load_edf_metadata(record_filename: Path) -> dict:
    """Load an EDF record."""
    # Open EDF file
    f = pyedflib.EdfReader(record_filename)

    # Get the header information
    header = f.getHeader()

    data = {
        'sex': header.get('gender', np.nan),
        # TODO: convert startdate and birthdate keys into an age
        # startdate is a datetime, birthdate is free-text
        'age': header.get('age', np.nan),
        'units': header.get('units', np.nan),
        'sampling_frequency': f.samplefrequency(0),
        # TODO: get dx from annotations
        'dx': np.nan
    }
    return data

def load_edfz_metadata(record_filename: Path) -> dict:
    """Load an EDFZ record."""
    raise NotImplementedError()

def load_edfz(record_name: Path) -> np.ndarray:
    """Load an EDFZ record."""
    # with gzip.open(record_name, 'rb') as f:
    #     signal = f.read()
    # pyedflib expects a filename as input, not a file-like object :(
    raise NotImplementedError()

def write_edfz(record_name: Path) -> np.ndarray:
    """Write an EDFZ record."""
    raise NotImplementedError()

# === WFDB === #

def load_wfdb(record_filename: Path) -> np.ndarray:
    """Load a WFDB record."""
    # As of WFDB 4.1.1, rdrecord expects there to be no extension,
    # so we remove it if it exists
    suffix = record_filename.suffix
    if suffix in ('.dat', '.hea', '.mat'):
        record_filename = record_filename.parent / record_filename.stem

    record = wfdb.rdrecord(record_filename)
    if record.p_signal is None:
        raise ValueError(f'No signal found in {record_filename}')

    return record.p_signal

def write_wfdb(record_filename: Path, signal: np.ndarray, sampling_frequency: int = 500) -> np.ndarray:
    """Load a WFDB record."""
    # As of WFDB 4.1.1, wrsamp expects there to be no extension in record name,
    # so we remove it if it exists
    if record_filename.suffix not in ('.dat', '.hea'):
        warnings.warn(f'Saved WFDB records will use .dat/.hea, not {record_filename.suffix}')

    wfdb.wrsamp(
        record_filename.stem,
        fs=sampling_frequency,
        sig_name=_LEADS,
        p_signal=signal,
        fmt=['16'] * 12,
        units=['mV'] * 12,
        write_dir = record_filename.parent
    )

def load_wfdb_metadata(record_filename: Path) -> dict:
    """
    Load metadata from a WFDB (WaveForm DataBase) record file.

    Args:
        record_filename (Path): Path to the WFDB record file.

    Returns:
        dict: A dictionary containing metadata about the record file with the following keys:
            - 'sampling_frequency': Sampling frequency of the record
            - 'units' (str): Units of the record
            - 'age' (int): Age of the patient in years (if available)
            - 'sex' (int): Sex of the patient (male=1, female=0, if available)
            - 'dx' (list of int): Diagnosis codes for the record (if available, otherwise None)
    """
    # As of WFDB 4.1.1, rdrecord expects there to be no extension,
    # so we remove it if it exists
    suffix = record_filename.suffix
    if suffix in ('.dat', '.hea', '.mat'):
        record_filename = record_filename.parent / record_filename.stem

    # only load the header for a record
    record = wfdb.rdheader(record_filename, rd_segments=False)

    data = {
        'sampling_frequency': record.fs,
        'units': record.units,
    }

    # iterate through comments for demographics
    demographic_vars = ['age', 'sex', 'dx']
    for var in demographic_vars:
        data[var] = None
    for line in record.comments:
        for var in demographic_vars:
            if line.lower().strip().startswith(f'{var}:'):
                data[var] = line.split(':')[1].strip()
    
    # parse vars
    if data['age'] is not None:
        try:
            data['age'] = int(data['age'])
        except ValueError:
            data['age'] = None
    if data['sex'] is not None:
        data['sex'] = int(data['sex'].lower().startswith('m'))
    if data['dx'] is not None:
        data['dx'] = [int(x) for x in data['dx'].split(',')]

    return data

# === XML === #
def load_xml(record_filename: Path) -> np.ndarray:
    """Load waveform data from an XML record.
    
    This function assumes the following XML structure is present:
        <Waveform>
            <LeadData>
                <LeadByteCountTotal>1200</LeadByteCountTotal>
                <LeadTimeOffset>0</LeadTimeOffset>
                <LeadSampleCountTotal>600</LeadSampleCountTotal>
                <LeadAmplitudeUnitsPerBit>4.88</LeadAmplitudeUnitsPerBit>
                <LeadAmplitudeUnits>MICROVOLTS</LeadAmplitudeUnits>
                <LeadHighLimit>32767</LeadHighLimit>
                <LeadLowLimit>-32768</LeadLowLimit>
                <LeadID>I</LeadID>
                <LeadOffsetFirstSample>0</LeadOffsetFirstSample>
                <FirstSampleBaseline>0</FirstSampleBaseline>
                <LeadSampleSize>2</LeadSampleSize>
                <LeadOff>FALSE</LeadOff>
                <BaselineSway>FALSE</BaselineSway>
                <LeadDataCRC32>1391929279</LeadDataCRC32>
                <WaveFormData> ... </WaveFormData>
            </LeadData>
            ... (repeats for each lead)
        </Waveform>
    """
    # parse the element tree and navigate to the Waveform record
    etree = ET.parse(record_filename)
    root = etree.getroot()
    waveform = root.find('Waveform')

    # the Waveform tag has multiple LeadData tags, each of which
    # contains a base64-encoded string of the waveform data
    signal = []
    for lead in waveform.iter('LeadData'):
        # lead_name = lead.find('LeadID').text
        sample_size = int(lead.find('LeadSampleSize').text)
        if sample_size > 8:
            raise ValueError(f'byte size expected to be no higher than 8')
        sample_length = int(lead.find('LeadSampleCountTotal').text)

        # extract the string with the waveform data and decode into bytes
        lead_data = lead.find('WaveFormData').text
        lead_data = base64.b64decode(lead_data)

        # assert len(lead_data) == int(lead.find('LeadByteCountTotal').text)

        # iterate through to convert each byte into an integer
        lead_data = [
            int.from_bytes(
                lead_data[i:i+sample_size],
                byteorder='little',
                signed=True
            )
            for i in range(0, len(lead_data), sample_size)
        ]
        assert len(lead_data) == sample_length

        # convert to numpy array
        lead_data = np.array(lead_data, dtype=np.float32)
    
        # convert to physical units
        amplitude_units_per_bit = float(lead.find('LeadAmplitudeUnitsPerBit').text)
        baseline = int(lead.find('FirstSampleBaseline').text)
        lead_data = (lead_data - baseline) * amplitude_units_per_bit

        # check for various units of measure, converting to millivolts as needed
        units = lead.find('LeadAmplitudeUnits').text
        if units == 'MICROVOLTS':
            lead_data /= 1000
        elif units == 'VOLTS':
            lead_data *= 1000
        elif units == 'MILLIVOLTS':
            pass
        else:
            raise ValueError(f'unknown units of measure: {units}')
        signal.append(lead_data)
    
    # stack lead data column-wise
    signal = np.stack(signal, axis=1)
    return signal

def write_xml(record_filename: Path, signal: np.ndarray, sampling_frequency: int = 500) -> None:

    """Write waveform data to an XML record. Assumes the signal is stored
    as 16-bit integers in millivolts.
    
    This function writes the waveform data to an XML file with the following structure:
        <Waveform>
            <LeadData>
                <LeadByteCountTotal>1200</LeadByteCountTotal>
                <LeadTimeOffset>0</LeadTimeOffset>
                <LeadSampleCountTotal>600</LeadSampleCountTotal>
                <LeadAmplitudeUnitsPerBit>4.88</LeadAmplitudeUnitsPerBit>
                <LeadAmplitudeUnits>MICROVOLTS</LeadAmplitudeUnits>
                <LeadHighLimit>32767</LeadHighLimit>
                <LeadLowLimit>-32768</LeadLowLimit>
                <LeadID>I</LeadID>
                <LeadOffsetFirstSample>0</LeadOffsetFirstSample>
                <FirstSampleBaseline>0</FirstSampleBaseline>
                <LeadSampleSize>2</LeadSampleSize>
                <LeadOff>FALSE</LeadOff>
                <BaselineSway>FALSE</BaselineSway>
                <LeadDataCRC32>1391929279</LeadDataCRC32>
                <WaveFormData> ... </WaveFormData>
            </LeadData>
            ... (repeats for each lead)
        </Waveform>
    """
    # calculate an ideal amplitude units per bit
    leadwise_min = np.min(signal, axis=0)
    leadwise_max = np.max(signal, axis=0)

    digital_min, digital_max = -32768, 32767

    # calculate the amplitude units per bit for each lead
    # broadcasting digital scalars across each lead
    amplitude_units_per_bit = (leadwise_max - leadwise_min) / (digital_max - digital_min)
    baseline = digital_min - leadwise_min / amplitude_units_per_bit

    # adjust baseline to be an integer
    baseline = np.floor(baseline).astype(np.int16)

    # convert the signal from physical units (floating point) to integer
    # using the amplitude units per bit and baseline
    signal = np.floor(signal / amplitude_units_per_bit + baseline)

    # ensure we don't underflow
    # -> can happen close to the negative range
    signal = np.clip(signal, digital_min, digital_max).astype(np.int16)

    root = ET.Element('RestingECG')
    waveform = ET.SubElement(root, 'Waveform')

    # waveform properties
    ET.SubElement(waveform, 'WaveformType').text = 'Median'
    ET.SubElement(waveform, 'WaveformStartTime').text = '0'
    ET.SubElement(waveform, 'NumberofLeads').text = str(signal.shape[1])
    ET.SubElement(waveform, 'SampleType').text = 'CONTINUOUS_SAMPLES'
    ET.SubElement(waveform, 'SampleBase').text = str(sampling_frequency)
    ET.SubElement(waveform, 'SampleExponent').text = '0'
    ET.SubElement(waveform, 'HighPassFilter').text = '5'
    ET.SubElement(waveform, 'LowPassFilter').text = '100'
    ET.SubElement(waveform, 'ACFilter').text = '60'

    for i in range(signal.shape[1]):
        lead = ET.SubElement(waveform, 'LeadData')
        ET.SubElement(lead, 'LeadByteCountTotal').text = str(signal.shape[0] * 2)
        ET.SubElement(lead, 'LeadTimeOffset').text = '0'
        ET.SubElement(lead, 'LeadSampleCountTotal').text = str(signal.shape[0])
        ET.SubElement(lead, 'LeadAmplitudeUnitsPerBit').text = str(amplitude_units_per_bit[i])
        ET.SubElement(lead, 'LeadAmplitudeUnits').text = 'MILLIVOLTS'
        ET.SubElement(lead, 'LeadHighLimit').text = str(digital_max)
        ET.SubElement(lead, 'LeadLowLimit').text = str(digital_min)
        ET.SubElement(lead, 'LeadID').text = _LEADS[i]
        ET.SubElement(lead, 'LeadOffsetFirstSample').text = '0'
        ET.SubElement(lead, 'FirstSampleBaseline').text = str(baseline[i])
        # encoding as 16-bit integers, so 2 bytes per sample
        ET.SubElement(lead, 'LeadSampleSize').text = '2'
        ET.SubElement(lead, 'LeadOff').text = 'FALSE'
        ET.SubElement(lead, 'BaselineSway').text = 'FALSE'
        ET.SubElement(lead, 'LeadDataCRC32').text = 'TODO'

        # convert to integer and bytes
        lead_bytes = np.ascontiguousarray(signal[:, i], dtype='<i2').tobytes()
        
        # encode to base64 and add to XML
        b64_lead_data = base64.b64encode(lead_bytes).decode()
        ET.SubElement(lead, 'WaveFormData').text = b64_lead_data
        
    # write the XML file
    tree = ET.ElementTree(root)
    tree.write(str(record_filename), encoding='utf-8', xml_declaration=True)

def load_xml_metadata(record_filename: Path) -> dict:
    """Load metadata from a GE MUSE XML record."""
    etree = ET.parse(record_filename)
    # root is RestingECG tag
    root = etree.getroot()
    demographics = root.find('PatientDemographics')
    data = {}
    data['age'] = demographics.find('PatientAge').text
    data['sex'] = demographics.find('Gender').text
    data['race'] = demographics.find('Race').text

    # TODO: some thought here once the data actually comes in
    dx = root.find('Diagnosis')
    # iterate through the DiagnosisStatement elements under diagnosis
    # and get the StmtText attribute under it
    dx = [x.find('StmtText').text for x in dx.iter('DiagnosisStatement')]

    # TODO: above dx is free text
    # need to convert to a list of codes
    # for now, just return the free text
    data['dx'] = dx
    return data

# === CSV === #

def load_csv(record_name: Path) -> np.ndarray:
    """Load a CSV record.
    
    CSV must have a header row and 12 columns. Each column should be
    a lead of the ECG. If there are 13 columns, the first column is assumed
    to be a time/sample number column and discarded.
    """
    with open(record_name, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = np.array(list(reader), dtype=np.float32)

    if len(header) == 13:
        header = header[1:]
        data = data[:, 1:]
    elif len(header) != 12:
        raise ValueError('CSV must have 12 or 13 columns')
    
    return data


# === Record Loading === #
# The following functions are used to load records from various formats.

load_functions = {
    "wfdb": (load_wfdb, load_wfdb_metadata),
    "edf": (load_edf, load_edf_metadata),
    "edfz": (load_edfz, load_edfz_metadata),
    "xml": (load_xml, load_xml_metadata),
}

def get_file_function(format: str) -> tuple[Callable, Callable]:
    if format in load_functions:
        return load_functions[format]
    else:
        raise ValueError(f"Unsupported file format: {format}")

def load_record(record_filename: Union[str, Path], format: str = "wfdb") -> np.ndarray:
    """Load a record from a file."""
    load_func, _ = get_file_function(format)
    return load_func(Path(record_filename))

def load_metadata(record_filename: Union[str, Path], format: str = "wfdb") -> dict:
    """Load metadata from a file."""
    _, load_metadata_func = get_file_function(format)
    return load_metadata_func(Path(record_filename))
