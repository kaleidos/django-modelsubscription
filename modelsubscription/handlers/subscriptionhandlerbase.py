class SubscriptionHandlerBase(object):
    '''Abstract class for Subscription Handlers'''

    @classmethod
    def run(self, subscription, obj, *args):
        '''Abstract method'''
        raise NotImplementedError
