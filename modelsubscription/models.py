from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .handlers import subscriptionhandlers
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from .settings import *

SUBSCRIPTION_TYPE_CHOICES = [ (x,x) for x in SUBSCRIPTION_TYPES.keys() ]

class Subscription(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    # Email for anonymous subscription, and user for registered user subscription
    email = models.EmailField(db_index=True, null=True, blank=True)
    user = models.ForeignKey(User, related_name='subscribed_models', db_index=True, null=True, blank=True)
    typ = models.SlugField(max_length=30, choices=SUBSCRIPTION_TYPE_CHOICES)

    def run(self, obj):
        if self.typ in SUBSCRIPTION_TYPES.keys():
            handler = subscriptionhandlers[self.typ]
            extra_args = SUBSCRIPTION_TYPES[self.typ]['extra_args']
            handler.run(self, obj, *extra_args)

class SubscriptableMixin(models.Model):
    subscriptions = generic.GenericRelation(Subscription)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(SubscriptableMixin, self).save(*args, **kwargs)
        for subscription in self.subscriptions.all():
            subscription.run(self)

    def subscribe_user(self, user, typ):
        subscription = Subscription(user=user, typ=typ, content_object=self)
        subscription.save()
        self.subscriptions.add(subscription)

    def subscribe_email(self, email, typ):
        subscription = Subscription(email=email, typ=typ, content_object=self)
        subscription.save()
        self.subscriptions.add(subscription)

    def unsubscribe_user(self, user, typ=None):
        if typ != None:
            self.subscriptions.filter(user=user, typ=typ).delete()
        else:
            self.subscriptions.filter(user=user).delete()

    def unsubscribe_email(self, email, typ=None):
        if typ != None:
            self.subscriptions.filter(email=email, typ=typ).delete()
        else:
            self.subscriptions.filter(email=email).delete()
