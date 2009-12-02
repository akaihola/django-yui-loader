import doctest
from unittest import defaultTestLoader

def suite():
    suite = doctest.DocFileSuite(
        'test_loader.py',
        'test_views.py')
    suite.addTest(defaultTestLoader.loadTestsFromName(
            'yui_loader.tests.test_middleware'))
    return suite
