import json

from django.test import TestCase


class BaseTestCase(TestCase):

    def get_ajax(self, *args, **kwargs):
        kwargs.update({'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        return self.client.get(*args, **kwargs)

    def post_ajax(self, *args, **kwargs):
        kwargs.update({'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        return self.client.post(*args, **kwargs)

    def json_response(self, response):
        return json.loads(response.content.decode('utf-8'))
