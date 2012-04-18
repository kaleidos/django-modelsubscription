class SubscriptionHandlerBase(object):
    @classmethod
    def run(self, subscription, obj, *args):
        raise NotImplementedError
