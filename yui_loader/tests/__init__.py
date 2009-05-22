import doctest

def suite():
    suite = doctest.DocFileSuite(
        'test_loader.py',
        'test_views.py',)
    return suite
