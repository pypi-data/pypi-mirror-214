import os
import pytest
import numpy as np

from ecghelper.io import (
    load_xml, load_wfdb, load_edf,
    write_xml, write_wfdb, write_edf
)

@pytest.mark.parametrize("ext,fcns", [(".xml", (load_xml, write_xml)), (".hea", (load_wfdb, write_wfdb)), (".edf", (load_edf, write_edf))])
def test_readwrite(data_path, tmp_path, ext, fcns):
    """Tests that we can read and write signals without changing the data."""
    load_fcn, write_fcn = fcns
    signal = load_fcn(data_path / f"A0001{ext}")
    assert signal.shape[0] > 0
    assert signal.shape[1] == 12

    # units should be between -2 and 5 millivolts
    assert signal.min() > -2
    assert signal.max() < 5

    # EDF precision is 8 chars
    signal = np.around(signal, 5)
    output_file = tmp_path / f'A0001{ext}'
    write_fcn(output_file, signal, 500)
    assert os.path.exists(output_file)

    # re-load, compare to original signal
    signal_reloaded = load_fcn(output_file)
    assert signal_reloaded.shape == signal.shape

    # assert approximately equal
    assert (abs(signal_reloaded - signal) < 0.01).all()
