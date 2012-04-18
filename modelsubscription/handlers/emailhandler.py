from .subscriptionhandlerbase import SubscriptionHandlerBase
from django.core.mail import send_mail
from .. import settings

class EmailHandler(SubscriptionHandlerBase):
    @classmethod
    def run(self, subscription, obj, *args):
        if subscription.email:
            dst_mail = subscription.email
        else:
            dst_mail = subscription.user.email
        send_mail(
                'Object %s updated' % str(obj),
                'The object %s has been updated.' % (str(obj)),
                settings.SUBSCRIPTION_EMAIL_FROM,
                [subscription.email],
                fail_silently=True
        )
