from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
import h5py
import pandas as pd

import pytest
from unittest.mock import Mock
from scipy.interpolate import interp1d

from .. import em_bright, categorize, utils
from ..data import EOS_MAX_MASS



@pytest.mark.parametrize(
    'posteriors, dtype, result, result_eos',
     [[[(1.4, 1.4, 0.0, 0.0, 100.0),
       (2.0, 0.5, 0.99, 0.99, 150.0)],
      [('mass_1', '<f8'), ('mass_2', '<f8'), ('a_1', '<f8'),
       ('a_2', '<f8'), ('luminosity_distance', '<f8')],
      (1.0, 1.0, 0.0), (1.0, 1.0, 0.0)],
     [('ra', '<f8'), ('dec', '<f8'), ('luminosity_distance', '<f8'),
      ('time', '<f8'), ('mass_1', '<f8'), ('mass_2', '<f8'),
      ('spin_1z', '<f8'), ('spin_2z', '<f8')],
     (1.0, 1.0, 0.5), (1.0, 0.5, 0.5)]]
)
def test_source_classification_pe(posteriors, dtype, result, result_eos):
    """Test em_bright classification from posterior
    samples - both aligned and precessing cases.
    """
    with NamedTemporaryFile() as f:
        filename = f.name
        with h5py.File(f, 'w') as tmp_h5:
            data = np.array(
                posteriors,
                dtype=dtype
            )
            tmp_h5.create_dataset(
                'posterior_samples',
                data=data
            )
        r = em_bright.source_classification_pe(filename)
        r_eos = em_bright.source_classification_pe(filename, num_eos_draws=5,
                                                   eos_seed=0)

    print(r)
    print(r_eos)

    #assert r == result
    assert r_eos == result_eos

