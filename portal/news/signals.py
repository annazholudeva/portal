from django.core.mail import EmailMultiAlternatives, mail_managers
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post


# from portal import settings


def send_notification(preview, pk, title, subscribers):
    html_content = render_to_string(
        'notification_created.html',
        {
            'message': preview,
            'link': f'{settings.STATIC_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscriber(sender, instance, **kwargs):
    if kwargs['action'] == 'news_create':
        categories = instance.category.all()
        subscribers_emails = []
        subscribers = []

        for cat in categories:
            subscribers += cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk(), instance.title(), subscribers_emails)
