from .subscriptionhandlerbase import SubscriptionHandlerBase
from django.core.mail import send_mail
from .. import settings
from django.template.loader import get_template
from django.template import Context

class EmailHandler(SubscriptionHandlerBase):
    @classmethod
    def run(self, subscription, obj, *args):
        if subscription.email:
            dst_mail = subscription.email
        else:
            dst_mail = subscription.user.email
        context = Context({'obj': obj,'subscription': subscription })
        subject_template = get_template('modelsubscription/email_subject.html')
        body_template = get_template('modelsubscription/email_body.html')
        send_mail(
                subject_template.render(context),
                body_template.render(context),
                settings.SUBSCRIPTION_EMAIL_FROM,
                [subscription.email],
                fail_silently=True
        )
