# -*- coding=utf-8 -*-



import unittest

from test import TestContent

if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTests([unittest.makeSuite(TestContent), ])

    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite)
