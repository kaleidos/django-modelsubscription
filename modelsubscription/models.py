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
    '''
    Subscription objects store subscription from user or email to objects

    Every subscription have a type with his own handler
    '''
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    # Email for anonymous subscription, and user for registered user subscription
    email = models.EmailField(db_index=True, null=True, blank=True)
    user = models.ForeignKey(User, related_name='subscribed_models', db_index=True, null=True, blank=True)
    typ = models.SlugField(max_length=30, choices=SUBSCRIPTION_TYPE_CHOICES)

    def run(self, obj, **kwargs):
        '''Run the handler of the subscription type for the obj param'''
        if self.typ in SUBSCRIPTION_TYPES.keys():
            handler = subscriptionhandlers[self.typ]
            extra_args = SUBSCRIPTION_TYPES[self.typ]['extra_args']
            extra_args.update(kwargs)
            handler.run(self, obj, **extra_args)

class SubscriptionEvent(models.Model):
    '''
    Model to store events when dbhandler is runned
    '''
    subscription = models.ForeignKey(Subscription, null=False, blank=False)
    kwargs = models.TextField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class SubscriptableMixin(models.Model):
    '''
    Subscriptable Mixin to aggregate subscription funcionality to a any model
    '''
    subscriptions = generic.GenericRelation(Subscription)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        '''
        Save the object, and run the subscriptions if
        SUBSCRIPTION_RUN_ON_CHANGE is set to True
        '''
        super(SubscriptableMixin, self).save(*args, **kwargs)
        if SUBSCRIPTION_RUN_ON_CHANGE:
            for subscription in self.subscriptions.all():
                subscription.run(self)

    def subscribe_user(self, user, typ):
        '''Create a subscription of the typ type to this object for a user'''
        (subscription, created) = Subscription.objects.get_or_create(
                user=user,
                typ=typ,
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.pk
        )
        if created:
            return 'new'
        else:
            return 'already'

    def subscribe_email(self, email, typ):
        '''Create a subscription of the typ type to this object for a email'''
        (subscription, created) = Subscription.objects.get_or_create(
                email=email,
                typ=typ,
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.pk
        )
        if created:
            return 'new'
        else:
            return 'already'

    def unsubscribe_user(self, user, typ=None):
        '''
        Remove a subscription of the typ type to this object for a user

        If typ is None, remove all subscriptions of this user
        '''
        if typ != None:
            self.subscriptions.filter(user=user, typ=typ).delete()
        else:
            self.subscriptions.filter(user=user).delete()
        return True

    def unsubscribe_email(self, email, typ=None):
        '''
        Remove a subscription of the typ type to this object for a email

        If typ is None, remove all subscriptions of this email
        '''
        if typ != None:
            self.subscriptions.filter(email=email, typ=typ).delete()
        else:
            self.subscriptions.filter(email=email).delete()
        return True
