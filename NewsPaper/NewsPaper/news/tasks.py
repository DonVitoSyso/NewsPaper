# D6
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from datetime import timedelta, date


# from django.utils.timezone import datetime, timedelta, timezone, timestamp

def get_subscribers(category):
    user_emails = []
    for user in category.subscribers.all():
        user_emails.append(user.email)
    return user_emails


def send_emails(post_object, *args, **kwargs):
    # print(kwargs['template'])
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},
        # передаем в шаблон любые переменные
    )
    print(f'category: {kwargs["category_object"]}')
    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email='vitosyso@yandex.ru',
        to=kwargs['user_emails']  # отправляем всем из списка
    )
    msg.attach_alternative(html, 'text/html')
    # msg.send()


def new_post_subscription(instance):
    # latest_post = Post.objects.all().order_by('-date')[0]
    template = 'subcat/newpost.html'
    latest_post = instance

    # if not latest_post.isUpdated:
    for category in latest_post.category.all():
        email_subject = f'Новая новость в категории: "{category}"'
        user_emails = get_subscribers(category)
        send_emails(
            latest_post,
            category_object=category,
            email_subject=email_subject,
            template=template,
            user_emails=user_emails)