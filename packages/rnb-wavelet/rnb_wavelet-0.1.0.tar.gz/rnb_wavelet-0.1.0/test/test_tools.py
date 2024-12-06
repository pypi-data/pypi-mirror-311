import unittest
import numpy as np
from rnb.utils.tools import compute_spectre_brute

class TestTools(unittest.TestCase):
    def test_some_function(self):
        # Test inputs
        fs = 1000  # Sampling frequency in Hz
        data_epocs = np.random.rand(1, 1024)  # 1 epoch, 1024 time points
        
        # Call the function
        freq, F = compute_spectre_brute(data_epocs, fs)
        
        # Expected outputs
        expected_freq = fs / 2 * np.linspace(0, 1, 1024 // 2 + 1)[1:]  # Skip null frequency
        expected_F_shape = (1, len(expected_freq))  # 1 epoch, matching freq length
        
        # Assertions
        np.testing.assert_array_almost_equal(freq, expected_freq, decimal=5)  # Compare frequency arrays
        self.assertEqual(F.shape, expected_F_shape)  # Compare shape of power spectrum

if __name__ == "__main__":
    unittest.main()
