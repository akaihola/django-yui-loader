from django.test import TestCase
from django.conf import settings

from yui_loader.middleware import YUIIncludeMiddleware

class ResponseMock(dict):
    def __init__(self, content_type, content):
        super(ResponseMock, self).__init__({'Content-Type': content_type})
        self.content = content

class MiddlewareTestCase(TestCase):

    def test_return_original_response_object(self):
        m = YUIIncludeMiddleware()
        original_response = ResponseMock('text/html', '<!-- YUI_init -->')
        modified_response = m.process_response(None, original_response)
        self.assertEqual(id(original_response), id(modified_response))

    def assertProcessesContentType(self, content_type, should_process=True):
        m = YUIIncludeMiddleware()
        original_content = '<!-- YUI_include dom --><!-- YUI_init -->'
        ctx = {'base': settings.YUI_INCLUDE_BASE}
        if should_process:
            expected_content = (
                '<script type="text/javascript"'
                ' src="%(base)syahoo/yahoo-min.js"></script>\n'
                '<script type="text/javascript"'
                ' src="%(base)sdom/dom-min.js"></script>' % ctx)
        else:
            expected_content = original_content
        response = ResponseMock(content_type, original_content)
        m.process_response(None, response)
        self.assertEqual(response.content, expected_content)

    def test_ignore_images(self):
        self.assertProcessesContentType('application/png', False)

    def test_modify_html(self):
        self.assertProcessesContentType('text/html')

    def test_modify_xhtml(self):
        self.assertProcessesContentType('application/xhtml+xml')

    def test_ignores_unnecessary_init(self):
        m = YUIIncludeMiddleware()
        original_content = '<!-- YUI_init -->'
        response = ResponseMock('text/html', original_content)
        m.process_response(None, response)
        self.assertEqual(response.content, original_content)

    def test_warns_about_missing_init(self):
        m = YUIIncludeMiddleware()
        original_content = '<!-- YUI_include dom -->'
        expected_content = '<p>0 YUI init tags found,at least one expected</p>'
        response = ResponseMock('text/html', original_content)
        m.process_response(None, response)
        self.assertEqual(response.content, expected_content)
