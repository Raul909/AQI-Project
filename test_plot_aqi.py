import unittest
from unittest.mock import MagicMock, patch
import sys

class TestPlotAQI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Safely mock pandas and matplotlib for the duration of this class
        cls.mock_pd = MagicMock()
        cls.mock_plt = MagicMock()

        cls.patcher = patch.dict(sys.modules, {
            'pandas': cls.mock_pd,
            'matplotlib': MagicMock(),
            'matplotlib.pyplot': cls.mock_plt
        })
        cls.patcher.start()

        # Import Plot_AQI inside the patched context
        if 'Plot_AQI' in sys.modules:
            import importlib
            import Plot_AQI
            importlib.reload(Plot_AQI)
        else:
            import Plot_AQI
        cls.Plot_AQI = Plot_AQI

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def setUp(self):
        # Reset mocks before each test
        self.mock_pd.reset_mock()
        self.mock_pd.to_numeric.side_effect = None
        self.mock_pd.to_numeric.return_value = MagicMock()
        self.mock_plt.reset_mock()

    def test_calculate_average_numeric(self):
        """Test calculate_average with valid numeric data."""
        mock_df = MagicMock()
        mock_series = MagicMock()
        mock_df.__getitem__.return_value = mock_series

        self.mock_pd.read_csv.return_value = [mock_df]

        mock_numeric_series = MagicMock()
        mock_numeric_series.sum.return_value = 60.0
        self.mock_pd.to_numeric.return_value = mock_numeric_series

        avg = self.Plot_AQI.calculate_average('dummy.csv')

        self.mock_pd.read_csv.assert_called_with('dummy.csv', chunksize=24)
        self.assertEqual(len(avg), 1)
        self.assertEqual(avg[0], 2.5)

    def test_calculate_average_multiple_chunks(self):
        """Test calculate_average with multiple chunks of data."""
        mock_df1 = MagicMock()
        mock_df2 = MagicMock()
        self.mock_pd.read_csv.return_value = [mock_df1, mock_df2]

        mock_numeric_series1 = MagicMock()
        mock_numeric_series1.sum.return_value = 24.0
        mock_numeric_series2 = MagicMock()
        mock_numeric_series2.sum.return_value = 48.0

        self.mock_pd.to_numeric.side_effect = [mock_numeric_series1, mock_numeric_series2]

        avg = self.Plot_AQI.calculate_average('dummy.csv')

        self.assertEqual(len(avg), 2)
        self.assertEqual(avg[0], 1.0)
        self.assertEqual(avg[1], 2.0)

    def test_calculate_average_with_invalid_data(self):
        """Test calculate_average handling invalid data strings."""
        mock_df = MagicMock()
        self.mock_pd.read_csv.return_value = [mock_df]

        mock_numeric_series = MagicMock()
        mock_numeric_series.sum.return_value = 12.0
        self.mock_pd.to_numeric.return_value = mock_numeric_series

        avg = self.Plot_AQI.calculate_average('dummy.csv')

        self.assertEqual(avg[0], 0.5)
        self.mock_pd.to_numeric.assert_called_with(mock_df['PM2.5'], errors='coerce')

    def test_year_functions(self):
        """Test each year-specific function calls calculate_average with correct path."""
        with patch('Plot_AQI.calculate_average') as mock_calc:
            mock_calc.return_value = [10.0]

            # Test 2013
            res = self.Plot_AQI.avg_data_2013()
            mock_calc.assert_called_with('Data/AQI/aqi2013.csv')
            self.assertEqual(res, [10.0])

            # Test 2014
            self.Plot_AQI.avg_data_2014()
            mock_calc.assert_called_with('Data/AQI/aqi2014.csv')

            # Test 2015
            self.Plot_AQI.avg_data_2015()
            mock_calc.assert_called_with('Data/AQI/aqi2015.csv')

            # Test 2016
            self.Plot_AQI.avg_data_2016()
            mock_calc.assert_called_with('Data/AQI/aqi2016.csv')

            # Test 2017
            self.Plot_AQI.avg_data_2017()
            mock_calc.assert_called_with('Data/AQI/aqi2017.csv')

            # Test 2018
            self.Plot_AQI.avg_data_2018()
            mock_calc.assert_called_with('Data/AQI/aqi2018.csv')

if __name__ == '__main__':
    unittest.main()
