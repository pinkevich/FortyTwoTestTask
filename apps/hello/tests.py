import json
import ast

from django.test import TestCase
from django.core.urlresolvers import reverse_lazy

from .models import Bio, HttpRequest


class HelloTests(TestCase):

    def get_ajax(self, *args, **kwargs):
        kwargs.update({'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        return self.client.get(*args, **kwargs)

    def post_ajax(self, *args, **kwargs):
        kwargs.update({'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        return self.client.post(*args, **kwargs)

    def json_response(self, response):
        return json.loads(response.content.decode('utf-8'))

    def test_main_page(self):
        """
        test main page (opened, template, context)
        """
        bio = Bio.objects.first()
        url = reverse_lazy('hello:main')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Bio.objects.count(), 1)
        self.assertEqual(resp.context['bio'], bio)
        self.assertTemplateUsed(resp, 'main.html')
        self.assertContains(resp, 'Alexander')
        self.assertContains(resp, 'Pinkevich')
        self.assertContains(resp, 'March 15, 1993')
        self.assertContains(resp, 'my@pinkevich.net')
        self.assertContains(resp, 'pinkevich@jabber.ru')
        self.assertContains(resp, 'pinkevich.net')

    def test_main_page_errors(self):
        """
        test main page if more than two objects in bio model
        and if not objects in bio model
        """
        bio = Bio.objects.first()
        new_bio = Bio.objects.create(first_name='test_first_name',
                                     last_name='test_last_name',
                                     date_of_birth='2000-01-01',
                                     email='test@example.com',
                                     jabber='test', skype='test')
        url = reverse_lazy('hello:main')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Bio.objects.count(), 2)
        self.assertEqual(resp.context['bio'], bio)
        self.assertNotEqual(resp.context['bio'], new_bio)
        self.assertContains(resp, 'Alexander')
        self.assertNotContains(resp, 'test_first_name')
        self.assertNotContains(resp, 'test_last_name')
        self.assertNotContains(resp, 'January 01, 2000')
        self.assertNotContains(resp, 'test@example.com')
        self.assertNotContains(resp, 'test')
        self.assertTemplateUsed(resp, 'main.html')

        Bio.objects.all().delete()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Bio.objects.count(), 0)
        self.assertEqual(resp.context['bio'], None)
        self.assertNotContains(resp, 'Alexander')
        self.assertNotContains(resp, 'test_first_name')
        self.assertTemplateUsed(resp, 'main.html')

    def test_requests_page(self):
        """
        test view new http requests
        """
        url = reverse_lazy('hello:requests')
        main_url = reverse_lazy('hello:main')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'requests.html')
        self.assertEqual(HttpRequest.objects.filter(is_read=False).count(), 0)

        for num in range(1, 11):
            main_resp = self.client.get(main_url)
            self.assertEqual(main_resp.status_code, 200)
            self.assertEqual(
                HttpRequest.objects.filter(is_read=False).count(), num
            )

        resp = self.get_ajax(url)
        response = self.json_response(resp)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(response), 10)
        for num, resp in enumerate(response, start=1):
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

        # Retry the mark "is read"
        first = HttpRequest.objects.last()
        resp = self.post_ajax(url, {'request_pk': first.pk})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.json_response(resp), {'success': False})
