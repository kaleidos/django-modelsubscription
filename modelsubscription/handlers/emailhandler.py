from .subscriptionhandlerbase import SubscriptionHandlerBase
from django.core.mail import send_mail
from .. import settings
from django.template.loader import get_template
from django.template import Context

class EmailHandler(SubscriptionHandlerBase):
    '''Email Subscription Handler, send an email when is runned'''

    @classmethod
    def run(self, subscription, obj, **kwargs):
        '''
        send an email to the subscription.email or the subscription.user.email

        Generate the email text from the templates
        modelsubscription/email/subject.txt and modelsubscription/email/body.txt with
        \*\*kwargs and invitation in the context.
        '''
        if subscription.email:
            dst_mail = subscription.email
        else:
            dst_mail = subscription.user.email
        context = Context({'obj': obj, 'subscription': subscription })
        context.update(kwargs)
        subject_template = get_template('modelsubscription/email/subject.txt')
        body_template = get_template('modelsubscription/email/body.txt')

        subject = subject_template.render(context)
        subject = ' '.join(subject.split('\n')) # No newlines in subject lines allowed
        subject = subject.strip()

        body = body_template.render(context)

        send_mail(
                subject,
                body,
                settings.SUBSCRIPTION_EMAIL_FROM,
                [dst_mail]
        )
