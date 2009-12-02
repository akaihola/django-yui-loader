import re

def fix_test_urls(s):
    """
    To make the tests work when run inside another project, this
    function is used to normalize URLs when comparing output.
    """
    from django.conf import settings
    return re.sub(r'(^|(?<=="))%s' % settings.YUI_INCLUDE_BASE,
                  'YUI_INCLUDE_BASE/', s)
