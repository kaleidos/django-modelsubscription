Django Model Subscription
=========================

Django Model Subscription enable subscription of user and emails to models changes.

Configuration
=============

Add to every model that you want to be subscribed the SubscriptableMixin as base class::

  class MyModel(SubscriptableMixin, models.Model):
      ...

Configure in your settings.py the SUBSCRIPTION_EMAIL_FROM and the SUBSCRIPTION_TYPES::

  ...
  SUBSCRIPTION_EMAIL_FROM = 'myadminemail@mydomain.com'
  SUBSCRIPTION_TYPES = {
      'email': {'handler': 'modelsubscription.handlers.emailhandler.EmailHandler', 'extra_args': []},
      'myownhandler': {'handler': 'myapp.subscriptionhandlers.MyOwnHandler', 'extra_args': []},
  }
  ...

Create your own handler
-----------------------

You can create your own handler to your subscriptions, for example::

  from modelsubscription.handlers.subscriptionhandlerbase import SubscriptionHandlerBase

  class MyCrazyDestructiveHandler(SubscriptionHandlerBase):
      @classmethod
      def run(self, subscription, obj, *args):
          if subscription.user:
              subscription.user.delete()
              subscription.()

