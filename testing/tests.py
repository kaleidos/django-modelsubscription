from django.test import TestCase
from django.core import mail
from django.core.management import call_command
from django.contrib.auth.models import User

call_command('syncdb', interactive=False)

from .models import TestModel
from modelsubscription.models import Subscription


class SubscriptableMixinTest(TestCase):
    def setUp(self):
        self.user1 = User(username='test1', email='test1@test.com')
        self.user1.save()

        self.user2 = User(username='test2', email='test2@test.com')
        self.user2.save()

        self.test = TestModel()
        self.test.save()

        self.subscription = Subscription(user=self.user1, typ='email', content_object=self.test)
        self.subscription.save()

    def test_post_save(self):
        self.assertEqual(len(mail.outbox), 0)
        self.test.save()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Object TestModel object updated')
        self.assertEqual(mail.outbox[0].body, 'The object TestModel object has been updated.\n')

    def test_subscribe_user(self):
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 0)
        self.test.subscribe_user(self.user2, 'email')
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 1)

    def test_subscribe_email(self):
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 0)
        self.test.subscribe_email('testemail@test.com', 'email')
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 1)

    def test_unsubscribe_user(self):
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 0)
        self.assertEqual(self.test.subscribe_user(self.user2, 'email'), 'new')
        self.assertEqual(self.test.subscribe_user(self.user2, 'db'), 'new')
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 2)
        self.test.unsubscribe_user(self.user2, 'email')
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 1)
        self.test.unsubscribe_user(self.user2, 'db')
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 0)

        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 0)
        self.test.subscribe_user(self.user2, 'email')
        self.test.subscribe_user(self.user2, 'db')
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 2)
        self.test.unsubscribe_user(self.user2)
        self.assertEqual(Subscription.objects.filter(user=self.user2).count(), 0)

    def test_unsubscribe_email(self):
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 0)
        self.test.subscribe_email('testemail@test.com', 'email')
        self.test.subscribe_email('testemail@test.com', 'db')
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 2)
        self.test.unsubscribe_email('testemail@test.com', 'email')
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 1)
        self.test.unsubscribe_email('testemail@test.com', 'db')
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 0)

        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 0)
        self.test.subscribe_email('testemail@test.com', 'email')
        self.test.subscribe_email('testemail@test.com', 'db')
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 2)
        self.test.unsubscribe_email('testemail@test.com')
        self.assertEqual(Subscription.objects.filter(email='testemail@test.com').count(), 0)
