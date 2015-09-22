from io import BytesIO

from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.template import Template, Context, TemplateSyntaxError
from django.contrib.auth.models import User, Permission, Group
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry, ContentType

from south.models import MigrationHistory

from .tests import BaseTestCase
from ..models import History, HttpRequest, Bio


class TagTests(BaseTestCase):

    def render_edit_link_tag(self, obj):
        html = '{% load hello_tags %}' \
               '{% edit_link test %}'
        return Template(html).render(Context({'test': obj}))

    def test_edit_link_tag(self):
        """
        Test success working edit_link tag
        """
        user = User.objects.get(username='admin')
        info = user._meta.app_label, user._meta.model_name
        url = reverse('admin:%s_%s_change' % info, args=(user.pk,))
        rendered = self.render_edit_link_tag(user)
        self.assertEqual(rendered, '<a href="{0}">{1}</a>'.format(url, user))

    def test_edit_link_tag_error(self):
        """
        Test TemplateSyntaxError in edit_link tag
        """
        with self.assertRaises(TemplateSyntaxError):
            rendered = self.render_edit_link_tag(1)
            self.assertRaises(TemplateSyntaxError, rendered)
            rendered = self.render_edit_link_tag('test')
            self.assertRaises(TemplateSyntaxError, rendered)


class CommandTests(BaseTestCase):

    def test_projectmodels(self):
        """
        Test working projectmodels command
        """
        stdout = BytesIO()
        stderr = BytesIO()
        call_command('projectmodels', stdout=stdout, stderr=stderr)
        stdout = stdout.getvalue()
        self.assertIn('Session -', stdout)
        self.assertNotIn('error: ', stdout)
        models = ['Session', 'LogEntry', 'Permission', 'Group',
                  'User', 'ContentType', 'Bio', 'HttpRequest',
                  'History', 'MigrationHistory']
        records = [Session, LogEntry, Permission, Group, User,
                   ContentType, Bio, HttpRequest, History, MigrationHistory]
        records = [num.objects.count() for num in records]
        for out, name, count in zip(stdout.split('\n'), models, records):
            out = out.strip().split()
            self.assertEqual(out[0], name)
            self.assertEqual(out[2], str(count))

        stderr = stderr.getvalue()
        self.assertIn('error: Session -', stderr)
        for err, name, count in zip(stderr.split('\n'), models, records):
            err = err.strip().split()
            self.assertEqual(err[0], 'error:')
            self.assertEqual(err[1], name)
            self.assertEqual(err[3], str(count))


class SignalTests(BaseTestCase):

    def setUp(self):
        History.objects.all().delete()
        self.req = HttpRequest.objects.create(
            ip='127.0.01', page='/', header={})

    def test_history_object_creation(self):
        """
        Test create_or_update_object signal that working
        when creation new object in any models
        """
        h_obj = History.objects.last()
        self.assertEqual(h_obj.model_name, self.req._meta.model_name)
        self.assertEqual(h_obj.model_instance, self.req.__unicode__())
        self.assertEqual(h_obj.action, History.CREATED)

    def test_history_object_editing(self):
        """
        Test create_or_update_object signal that working
        when editing object in any models
        """
        self.req.is_read = True
        self.req.save(update_fields=['is_read'])
        h_obj = History.objects.last()
        self.assertEqual(h_obj.model_name, self.req._meta.model_name)
        self.assertEqual(h_obj.model_instance, self.req.__unicode__())
        self.assertEqual(h_obj.action, History.EDITED)

    def test_history_object_deletion(self):
        """
        Test create_or_update_object signal that working
        when deletion object in any models
        """
        self.req.delete()
        h_obj = History.objects.last()
        self.assertEqual(h_obj.model_name, self.req._meta.model_name)
        self.assertEqual(h_obj.model_instance, self.req.__unicode__())
        self.assertEqual(h_obj.action, History.DELETED)
