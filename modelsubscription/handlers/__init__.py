from .. import settings
from django.utils.importlib import import_module

__all__ = ('subscriptionhandlers',)

subscriptionhandlers = {}
for subscription_type_key, subscription_type_conf in settings.SUBSCRIPTION_TYPES.iteritems():
    module_name = ".".join(subscription_type_conf['handler'].split(".")[0:-1])
    class_name = subscription_type_conf['handler'].split(".")[-1]
    subscriptionhandlers[subscription_type_key] = getattr(import_module(module_name), class_name)()
