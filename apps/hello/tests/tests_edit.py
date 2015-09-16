from django.core.urlresolvers import reverse_lazy
from django.conf.global_settings import LOGIN_URL

from .tests import BaseTestCase
from ..models import Bio


class EditTests(BaseTestCase):

    def setUp(self):
        self.edit_url = reverse_lazy('hello:edit')
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)

    @property
    def bio(self):
        return Bio.objects.first()

    def get_post_data(self, name=None, photo=None):
        data = {
            'first_name': name or self.bio.first_name,
            'last_name': name or self.bio.last_name,
            'date_of_birth': self.bio.date_of_birth,
            'email': self.bio.email,
        }
        if photo:
            data.update({'photo': photo})
        return data

    def test_open_edit_page(self):
        """
        Test open edit page as authenticated
        """
        resp = self.client.get(self.edit_url)
        form = resp.context['form']
        self.assertTrue(form)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'edit.html')
        self.assertEqual(form.instance, self.bio)
        self.assertContains(resp, self.bio.first_name)
        self.assertContains(resp, self.bio.last_name)
        self.assertContains(resp, self.bio.date_of_birth)
        self.assertContains(resp, self.bio.email)
        self.assertContains(resp, self.bio.jabber)
        self.assertContains(resp, self.bio.skype)

    def test_open_edit_page_error_login(self):
        """
        Test open edit page as not authenticated
        """
        self.client.logout()
        resp = self.client.get(self.edit_url)
        self.assertRedirects(resp, '{0}?next={1}'.format(LOGIN_URL,
                                                         self.edit_url))

    def test_save_bio_success(self):
        """
        Test success save/update bio info using ajax
        """
        resp = self.json_response(
            self.post_ajax(self.edit_url, self.get_post_data('test'))
        )
        self.assertTrue(resp['success'])
        self.assertEqual(self.bio.first_name, 'test')
        self.assertEqual(self.bio.last_name, 'test')
        self.assertFalse(self.bio.photo)

    def test_save_bio_errors(self):
        """
        Test errors save/update bio info using ajax (pass {})
        """
        resp = self.json_response(self.post_ajax(self.edit_url, {}))
        self.assertTrue(resp['errors'])
        self.assertFalse(resp['success'])
        for field in resp['errors'].values():
            self.assertEqual(field, ['This field is required.'])

    def test_save_bio_photo_success(self):
        """
        Test success save/update bio photo using ajax
        """
        photo = self.create_test_photo()
        resp = self.json_response(
            self.post_ajax(self.edit_url, self.get_post_data(photo=photo))
        )
        self.assertTrue(resp['success'])
        self.assertTrue(self.bio.photo)

    def test_save_bio_photo_errors(self):
        """
        Test errors save/update bio photo using ajax
        """
        photo = open('requirements.txt', 'r')
        resp = self.json_response(
            self.post_ajax(self.edit_url, self.get_post_data(photo=photo))
        )
        self.assertEqual(resp['errors']['photo'],
                         ['Upload a valid image. The file you uploaded '
                          'was either not an image or a corrupted image.'])
        self.assertFalse(resp['success'])
