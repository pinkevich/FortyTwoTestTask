import ast

from django.core.urlresolvers import reverse_lazy

from .tests import BaseTestCase
from ..models import HttpRequest


class HttpRequestTests(BaseTestCase):

    def test_open_requests_page(self):
        """
        Test open requests page and if not new requests
        """
        url = reverse_lazy('hello:requests')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'requests.html')
        self.assertEqual(HttpRequest.objects.filter(is_read=False).count(), 0)
        resp = self.get_ajax(url)
        json_resp = self.json_response(resp)
        self.assertEqual(len(json_resp), 0)

    def test_req_create(self, page='main'):
        """
        Test create new requests and view on page
        """
        url = reverse_lazy('hello:{}'.format(page))
        for num in range(1, 6):
            main_resp = self.client.get(url)
            self.assertEqual(main_resp.status_code, 200)

    def test_req_is_read(self):
        """
        "Click" on requests and mark as "is read".
        Check ajax response and query objects data
        """
        self.test_req_create()
        url = reverse_lazy('hello:requests')
        resp = self.get_ajax(url)
        json_resp = self.json_response(resp)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json_resp), 5)
        for num, resp in enumerate(json_resp, start=1):
            header = ast.literal_eval(resp['fields']['header'])
            self.assertEqual(resp['pk'], num)
            self.assertEqual(resp['fields']['is_read'], False)
            self.assertEqual(resp['fields']['ip'], '127.0.0.1')
            self.assertEqual(resp['fields']['page'], 'http://testserver/')
            self.assertEqual(header['SERVER_NAME'], 'testserver')
            self.assertEqual(header['REQUEST_METHOD'], 'GET')
            self.assertEqual(header['SERVER_PORT'], '80')

            resp = self.post_ajax(url, {'request_pk': num})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.json_response(resp), {'success': True})
        self.assertEqual(HttpRequest.objects.filter(is_read=False).count(), 0)

    def test_req_retry_is_read(self):
        """
        Retry the mark "is read"
        """
        self.test_req_create()
        HttpRequest.objects.update(is_read=True)
        url = reverse_lazy('hello:requests')
        first = HttpRequest.objects.last()
        resp = self.post_ajax(url, {'request_pk': first.pk})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.json_response(resp), {'success': False})

    def test_priority_requests(self):
        """
        Test first view priority page (edit) on requests page
        """
        self.client.login(username='admin', password='admin')

        self.test_req_create()  # first main page
        self.test_req_create('edit')    # two edit page (priority)

        url = reverse_lazy('hello:requests')
        resp = self.get_ajax(url)
        json_resp = self.json_response(resp)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json_resp), 10)
        count = 1
        for resp in json_resp:
            page = ''
            if count > 5:
                page = 'edit/'
            self.assertEqual(resp['fields']['page'],
                             'http://testserver/{}'.format(page))
            count += 1
