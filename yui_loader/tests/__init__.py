import doctest

def suite():
    suite = doctest.DocFileSuite(
        'test_middleware.py',
        'test_views.py',)
    return suite
