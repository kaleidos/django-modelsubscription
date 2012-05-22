from .subscriptionhandlerbase import SubscriptionHandlerBase
import json

class DbHandler(SubscriptionHandlerBase):
    '''DB Subscription Handler, store data in a django model when is runned'''

    @classmethod
    def run(self, subscription, obj, **kwargs):
        '''
        Store in the SubscriptionEvent model a reference to the
        subscription, the object, and a json of the kwargs
        '''
        SubscriptionEvent.objects.create(subscription=subscription, obj=obj, kwargs=json.dumps(kwargs))
