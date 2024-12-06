import unittest

import os
import sys
import glob

import numpy as np
import soundfile

sys.path.append('.')
sys.path.append('sdk_python3')
import phoneshift

# import matplotlib
# import matplotlib.pyplot as plt
# plt.ion()

class TestModule(unittest.TestCase):

    # Extra-testing functions

    # def assert_diff_maxabs_bounded(self, ref, test, threshold=phoneshift.float32.eps):
    #     self.assertEqual(len(ref), len(test))

    #     diff = ref - test
    #     diff_idx = np.where(abs(diff)>threshold)[0]
    #     if len(diff_idx)>0:
    #         for n in diff_idx:
    #             print(f'ref[{n}]={ref[n]} test[{n}]={test[n]} err={diff[n]} ({phoneshift.lin2db(diff[n])}dB) > {threshold} ({phoneshift.lin2db(threshold)}dB)')

    #         return False

    #     return True


    # Tests

    def test_misc(self):
        self.assertTrue(len(phoneshift.__version__)>0)
        self.assertTrue(len(phoneshift.info)>0)

        self.assertEqual(phoneshift.lin2db(2.0), +6.020600318908691)
        self.assertEqual(phoneshift.lin2db(0.5), -6.020600318908691)

    def test_float(self):
        self.assertEqual(phoneshift.float32.size, 4)
        self.assertTrue(phoneshift.float32.eps<1e-6)
        self.assertTrue(phoneshift.lin2db(phoneshift.float32.min)<-750)
        self.assertTrue(phoneshift.lin2db(phoneshift.float32.max)>+750)

        self.assertEqual(phoneshift.float64.size, 8)
        self.assertTrue(phoneshift.float64.eps<1e-15)
        self.assertTrue(phoneshift.float64.min<1e-300)
        self.assertTrue(phoneshift.float64.max>1e+300)

    # def filepaths_to_process(self):
    #     fpaths = glob.glob(f'../phoneshift/test_data/wav/*.wav')
    #     assert len(fpaths) > 0
    #     return fpaths

    # def dir_refs(self):
    #     return '../phoneshift/sdk_python3/test_data/refs'

    # def dir_output(self):
    #     return 'test_data/sdk_python3'

    # def test_ola_smoke(self):
    #     for fpath_in in self.filepaths_to_process():
    #         wav, fs = soundfile.read(fpath_in, dtype='float32')
    #         for first_frame_at_t0 in [True, False]:
    #             for timestep in [int(fs*0.01), int(fs*0.05)]:
    #                 for winlen in [int(fs*0.10), int(fs*0.20)]:
    #                     syn = phoneshift.ola(wav, fs, first_frame_at_t0=first_frame_at_t0, timestep=timestep, winlen=winlen)

    # def test_transform_resynth(self):
    #     wav, fs = np.ones(44100), 44100
    #     syn = phoneshift.transform(wav, fs)
    #     self.assertTrue(len(syn) == len(wav))

    # def test_ola_resynth(self):
    #     wav, fs = np.ones(44100), 44100
    #     syn = phoneshift.ola(wav, fs)
    #     self.assertTrue(len(syn) == len(wav))

    #     # for fpath_in in self.filepaths_to_process():
    #     #     wav, fs = soundfile.read(fpath_in, dtype='float32')
    #     #     syn = phoneshift.ola(wav, fs)
    #     #     self.assertTrue(self.assert_diff_maxabs_bounded(wav, syn, phoneshift.db2lin(-140.0)))

if __name__ == '__main__':
    unittest.main()
