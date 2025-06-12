import unittest
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

def load_all_tests():
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover(start_dir=os.path.dirname(__file__), pattern='test_*.py')
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = load_all_tests()
    runner.run(test_suite)