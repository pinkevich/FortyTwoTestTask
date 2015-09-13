from django.test import TestCase
from django.core.urlresolvers import reverse_lazy

from .models import Bio


class HelloTests(TestCase):

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
