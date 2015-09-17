import json
from io import BytesIO
from PIL import Image

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

    def create_test_photo(self, size=(50, 50)):
        file = BytesIO()
        image = Image.new('RGBA', size, color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
