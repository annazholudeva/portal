from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from portal.news.models import PostCategory
from portal.portal import settings


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


@receiver(m2m_changed, sender=PostCategory)
def notify_subscriber(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers += cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk(), instance.title(), subscribers_emails)
