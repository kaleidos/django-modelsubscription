Welcome to django-viter's documentation!
========================================

django-modelsubscriptio allows you to subscribe users or emails to your Django
models modify events

Installation
------------

::

    pip install django-modelsubscription
    

Configuration
-------------

Add ``modelsubscription`` and ``django.contrib.sites`` to your ``INSTALLED_APPS``

::

    INSTALLED_APPS = (
        'django.contrib.sites',
        'modelsubscription'
    )
    
   
Usage
-----

Add to your subscritable models the mixin modelsubscription.models.SubscriptableMixin as parent class

::

    from modelsubscription.models import SubscriptableMixin
    from django.db import models

    class MyModel(models.Model, SubscriptableMixin):
        ...

To subscribe an user to an object use :attr:`modelsubscription.modelsSubscriptableMixin.subscribe_user`

::
    obj = MyModel.objects.get(pk=1)
    obj.subscribe_user(request.user, 'email')


To subscribe an email to an object use :attr:`modelsubscription.modelsSubscriptableMixin.subscribe_email`

::
    obj = MyModel.objects.get(pk=1)
    obj.subscribe_email('foo@bar.com', 'email')

To unsubscribe an user to an object use :attr:`modelsubscription.modelsSubscriptableMixin.unsubscribe_user`

::
    obj = MyModel.objects.get(pk=1)
    # Unsuscribe one type of subscription
    obj.unsubscribe_user(request.user, 'email')

    # Unsuscribe to all types of subscriptiosn
    obj.unsubscribe_user(request.user)

To unsubscribe an email to an object use :attr:`modelsubscription.modelsSubscriptableMixin.unsubscribe_email`

::
    obj = MyModel.objects.get(pk=1)
    # Unsuscribe one type of subscription
    obj.unsubscribe_email('foo@bar.com', 'email')

    # Unsuscribe to all types of subscriptiosn
    obj.unsubscribe_email('foo@bar.com')

To run the subscription handlers you can do it automatically saving the object if :attr:`settings.SUBSCRIPTION_RUN_ON_CHANGE` is True

::

    obj = MyModel.objects.get(pk=1)
    obj.save()
    
To run the subscription handlers you can do it manually running 

::

    obj = MyModel.objects.get(pk=1)
    # for all subscriptions
    for subscription in obj.subscriptions.all():
        subscription.run(obj)
        
    # for one subscriptions
    obj.subscriptions.all()[1].run(obj)
    
    
By default :attr:`modelsubscription.handlers.emailhandler` will render ``modelsubscription/email/subject.txt``
and ``modelsubscription/email/body.txt`` for the email.

Settings
--------

There are a couple of editable settings

.. attribute:: SUBSCRIPTION_EMAIL_FROM

    :Default: :class:`settings.DEFAULT_FROM_EMAIL`
    :type: str
    
    The email address used to send subscription messages from.
    
.. attribute:: SUBSCRIPTION_RUN_ON_CHANGE
    
    :Default: :class:`True`
    :type: boolean
    
    Run automatically the subscriptions handlers on subscriptable objects save.
    
.. attribute:: SUBSCRIPTION_TYPES
    
    :Default: `{ 'email': {'handlers': 'modelsubscription.handlers.emailhandler.EmailHandler', 'extra_args': {}}, 'db': {'handler': 'modelsubscription.handlers.dbhandler.DbHandler', 'extra_args': {}} }`
    :type: dict
    
    Dictionary defining the subscription types
    
API
---

.. toctree::
    :maxdepth: 3
    
    viter

Made by `Kaleidos <http://www.kaleidos.net/>`_. 
