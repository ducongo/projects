'''This file was generate with generatorPythonUnitTest.py'''
import mlpython.datasets.store as dataset_store
import os
from nose.tools import *
import utGenerator

def setUp():
    try:
        dataset_store.download('mnist_rotated')
    except:
        print 'Could not download the dataset : ', 'mnist_rotated'
        assert False

def test_mnist_rotatedloadToMemoryTrue():
    utGenerator.run_test('mnist_rotated', True)

def test_mnist_rotatedloadToMemoryFalse():
    utGenerator.run_test('mnist_rotated', False)

def tearDown():
    dataset_store.delete('mnist_rotated')
