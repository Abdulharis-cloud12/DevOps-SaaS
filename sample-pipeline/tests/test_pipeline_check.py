import unittest
from src.pipeline_check import check_pipeline_status


class TestPipelineCheck(unittest.TestCase):

    def test_success_rate(self):
        self.assertEqual(check_pipeline_status(9, 1), 90.0)

    def test_all_successful(self):
        self.assertEqual(check_pipeline_status(10, 0), 100.0)

    def test_no_runs(self):
        self.assertEqual(check_pipeline_status(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
