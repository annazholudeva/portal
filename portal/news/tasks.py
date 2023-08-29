from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category
from news.signals import send_notification
from portal import settings


@shared_task
def new_post_for_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'news_create':
        categories = instance.category.all()
        subscribers_emails = []
        subscribers = []

        for cat in categories:
            subscribers += cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk(), instance.title(), subscribers_emails)


@shared_task
def weekly_news():
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    posts = Post.objects.filter(date__gte=week_ago)
    categories = set(posts.values_list('category__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'posts_created_week_ago.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject="Новости, которые вы могли пропустить",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
