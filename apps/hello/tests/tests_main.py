from django.core.urlresolvers import reverse_lazy

from .tests import BaseTestCase
from ..models import Bio


class HelloTests(BaseTestCase):

    def test_main_page(self):
        """
        Test main page (opened, template, context)
        """
        bio = Bio.objects.first()
        url = reverse_lazy('hello:main')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Bio.objects.count(), 1)
        self.assertEqual(resp.context['bio'], bio)
        self.assertTemplateUsed(resp, 'main.html')
        self.assertContains(resp, bio.first_name)
        self.assertContains(resp, bio.last_name)
        self.assertContains(resp, bio.date_of_birth.strftime('r'))
        self.assertContains(resp, bio.email)
        self.assertContains(resp, bio.jabber)
        self.assertContains(resp, bio.skype)

    def test_main_page_more_one_bio(self):
        """
        Test main page if more than two objects in bio model
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
        self.assertContains(resp, bio.first_name)
        self.assertNotContains(resp, 'test_first_name')
        self.assertNotContains(resp, 'test_last_name')
        self.assertNotContains(resp, 'January 01, 2000')
        self.assertNotContains(resp, 'test@example.com')
        self.assertNotContains(resp, 'test')
        self.assertTemplateUsed(resp, 'main.html')

    def test_main_page_not_bio(self):
        """
        If not objects in bio model
        """
        Bio.objects.all().delete()
        url = reverse_lazy('hello:main')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Bio.objects.count(), 0)
        self.assertEqual(resp.context['bio'], None)
        self.assertTemplateUsed(resp, 'main.html')
