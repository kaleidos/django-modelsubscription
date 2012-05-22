from django.conf import settings

SUBSCRIPTION_EMAIL_FROM = getattr(settings, 'SUBSCRIPTION_EMAIL_FROM', '')
SUBSCRIPTION_RUN_ON_CHANGE = getattr(settings, 'SUBSCRIPTION_RUN_ON_CHANGE', True)
SUBSCRIPTION_TYPES = getattr(
    settings,
    'SUBSCRIPTION_TYPES',
    {
        'email': {'handler': 'modelsubscription.handlers.emailhandler.EmailHandler', 'extra_args': {}},
        'db': {'handler': 'modelsubscription.handlers.dbhandler.DbHandler', 'extra_args': {}},
    }
)
