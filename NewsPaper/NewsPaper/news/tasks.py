# D6
import datetime

from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from datetime import timedelta, date
# D7
from celery import shared_task


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
    msg.send()


# D7 start
@shared_task
# D7 end
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


# D7 start
@shared_task
# D7 end
def notify_subscribers_weekly():
    template = 'subcat/weekly_digest.html'
    week = 7
    week_sec = week*24*60*60
    print(week)
    posts = Post.objects.all()
    posts_list = []
    cat_list = set()
    sub_list = set()

    # Находим все новости недельные
    for post in posts:
        interval_week = date.today() - post.date.date()
        if interval_week.total_seconds() < week_sec:
            posts_list.append(post)
            # Находим категории
            for category in post.category.all():
                if get_subscribers(category):
                    sub_list.update(get_subscribers(category))
                    cat_list.add(category)
    # print(posts_list)
    print(f'cat_list - {cat_list}')
    print(f'sub_list - {sub_list}')
    for user_email in sub_list:
        post_object = []
        category_set = set()

        for post in posts_list:
            for category in post.category.all():
                if get_subscribers(category):
                    for user in category.subscribers.all():
                        if user.email == user_email:
                            post_object.append(post)
                            category_set.add(category)
                            print(f"Done {category} + {user.id}")

        category_object = list(category_set)

        send_emails(
            post_object,
            category_object=category_object,
            email_subject="Новости за неделю по вашей подписке",
            template=template,
            user_emails=[user_email, ])
            # subscription = post.category.all().values('subscribers').filter(subscribers__email=user_email)
        # print(subscription)
    # Определяем все категории, нужны для
    # нахождения почтовых подписок на категорию
